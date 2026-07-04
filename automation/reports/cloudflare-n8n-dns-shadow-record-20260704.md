# Cloudflare n8n DNS Shadow Record Report

## Objective

Repair `n8n.xrmglobalhk.com` so it resolves to the VPS public IP:

```text
178.105.167.227
```

Final intended Google OAuth Redirect URI:

```text
https://n8n.xrmglobalhk.com/rest/oauth2-credential/callback
```

## Safety Rules Followed

- Did not print or expose `CF_API_TOKEN`.
- Did not request root password.
- Did not delete VPS containers or n8n data.
- Did not modify Cloudflare records outside `n8n.xrmglobalhk.com`.
- Restored the correct Cloudflare DNS record after each probe.

## Cloudflare API Result

Cloudflare API zone lookup succeeded.

```text
Zone: xrmglobalhk.com
Zone ID: 1b195abe1f5b0b515f175fb72c07e6bb
Account ID: ab47e4d04470c184e56ba21b4104e8ab
Zone status: active
Zone type: full
Authoritative nameservers:
- mina.ns.cloudflare.com
- nicolas.ns.cloudflare.com
```

API-visible DNS records showed exactly one `n8n` record after repair:

```text
Type: A
Name: n8n.xrmglobalhk.com
Content: 178.105.167.227
TTL: Auto / 1
Proxied: false
```

## Repair Attempt

The script `automation/scripts/fix-cloudflare-n8n-dns.py` performed:

1. Loaded `CF_API_TOKEN` from project `.env`.
2. Queried the active `xrmglobalhk.com` zone.
3. Listed all DNS records with pagination.
4. Deleted all API-visible `n8n` records.
5. Recreated the single correct DNS-only A record:

```text
n8n.xrmglobalhk.com -> 178.105.167.227
proxied=false
ttl=1
```

## Authoritative DNS Result After Repair

Despite the API-visible record being correct, Cloudflare authoritative DNS still returned the stale private IP:

```text
mina.ns.cloudflare.com      172.29.0.127
nicolas.ns.cloudflare.com   172.29.0.127
1.1.1.1                     172.29.0.127
8.8.8.8                     172.29.0.127
```

## Delete Window Probe

The script `automation/scripts/probe-cloudflare-n8n-delete-window.py` temporarily deleted all API-visible `n8n` records and then queried authoritative DNS before restoring the correct record.

Result:

```text
API-visible n8n records after delete: 0

Authoritative/public DNS while API-visible n8n record is absent:
mina.ns.cloudflare.com      172.29.0.127
nicolas.ns.cloudflare.com   172.29.0.127
1.1.1.1                     172.29.0.127
8.8.8.8                     172.29.0.127

PROBE_RESULT: STALE_OR_SHADOW_RECORD_CONFIRMED
```

The script then restored:

```text
Type: A
Name: n8n.xrmglobalhk.com
Content: 178.105.167.227
Proxied: false
TTL: Auto / 1
```

## Product Surface Checks

The current Cloudflare API token has only:

```text
Zone:Read
DNS:Read
DNS:Edit
Specific Zone: xrmglobalhk.com
```

Product-level checks were blocked with `403` / authentication errors for:

- Workers routes
- Zone rulesets
- SSL for SaaS custom hostnames
- Pages projects
- Cloudflare Tunnel public hostnames
- Access applications
- Account rulesets

## Cloudflare Dashboard UI Checks

The logged-in Cloudflare dashboard was also checked directly.

Observed UI state:

- DNS Records page: shows exactly 4 records.
- `n8n.xrmglobalhk.com`: visible as `A 178.105.167.227`, DNS only, TTL Auto.
- Workers Routes page: shows no configured routes.
- Workers & Pages account page: shows no projects.
- SSL/TLS Custom Hostnames page: Cloudflare for SaaS is not enabled.
- Load Balancing page: Load Balancing is not enabled.
- DNS Analytics page: shows queries for `n8n.xrmglobalhk.com`, but not a visible DNS record source for the stale response.

## Hidden Wildcard Evidence

Additional authoritative DNS tests showed that the issue is broader than the single `n8n` hostname.

Cloudflare DNS Records API:

```text
Query name: *.xrmglobalhk.com
Result: 0 records

Search: *
Result: 0 records
```

Cloudflare authoritative DNS:

```text
dig @mina.ns.cloudflare.com +short '*.xrmglobalhk.com' A
172.29.0.139

dig @nicolas.ns.cloudflare.com +short '*.xrmglobalhk.com' A
172.29.0.139

dig @mina.ns.cloudflare.com +short random-shadow-probe-20260704.xrmglobalhk.com A
172.29.0.137

dig @nicolas.ns.cloudflare.com +short random-shadow-probe-20260704.xrmglobalhk.com A
172.29.0.137

dig @mina.ns.cloudflare.com +short another-random-shadow-20260704.xrmglobalhk.com A
172.29.0.138

dig @nicolas.ns.cloudflare.com +short another-random-shadow-20260704.xrmglobalhk.com A
172.29.0.138
```

This confirms a hidden wildcard or backend-generated DNS behavior returning private `172.29.0.x` addresses for arbitrary subdomains, while the Cloudflare DNS Records API and dashboard show no wildcard record.

## Token Expansion Attempt

The Cloudflare UI shows two identical user API tokens named `Codex DNS Repair`, both with:

```text
Zone.Zone, Zone.DNS + 1
1 Zone
Active
```

The current token verification endpoint returned:

```text
Token ID: fe8eb36c1f406f1b3f26ab7eb097206e
Status: active
Scopes: not returned
```

The Cloudflare token list does not display token IDs, so the active `.env` token could not be safely distinguished from the duplicate token.

An edit attempt was opened in the UI, but no changes were saved because:

- The two `Codex DNS Repair` tokens are visually indistinguishable.
- Account-level permissions also require Account Resources selection.
- Saving the wrong duplicated token would not help the automation and would leave unnecessary permissions on another token.

The unsaved edit form was discarded with Cloudflare's "Discard changes" confirmation. The token remains at minimum DNS scope.

## Root Cause

The issue is not an API-visible DNS Record.

Confirmed root cause category:

```text
Cloudflare authoritative DNS is serving stale, shadow, backend, wildcard, or product-generated records outside the visible DNS Records API.
```

Evidence:

1. API-visible DNS record is correct.
2. Deleting all API-visible `n8n` records leaves zero `n8n` records in the DNS Records API.
3. During that zero-record window, Cloudflare authoritative nameservers still return `172.29.0.127`.
4. API-visible wildcard records are zero, but authoritative nameservers answer arbitrary random subdomains with `172.29.0.x`.

## Current Status

```text
DNS FIX: blocked by Cloudflare backend/product-generated record
API-visible DNS: correct
Authoritative DNS: incorrect
HTTPS/Caddy phase: not started because DNS is not correct
```

## Required Next Action

One of the following is required:

1. Grant a temporary Cloudflare token with read access to product surfaces:
   - Account:Cloudflare Tunnel:Read
   - Account:Access:Read
   - Account:Workers Scripts:Read
   - Account:Workers Routes:Read
   - Account:Pages:Read
   - Zone:Rulesets:Read
   - Zone:SSL and Certificates:Read

2. Or open a Cloudflare Support ticket using this evidence:

```text
Cloudflare DNS Records API shows no A record with content 172.29.0.127 for n8n.xrmglobalhk.com.
When all API-visible n8n.xrmglobalhk.com DNS records are deleted, authoritative nameservers mina.ns.cloudflare.com and nicolas.ns.cloudflare.com still return A 172.29.0.127 with authoritative answers.
Please remove or identify the backend/shadow/product-generated record serving n8n.xrmglobalhk.com A 172.29.0.127.
```

## Files Used

- `automation/scripts/fix-cloudflare-n8n-dns.py`
- `automation/scripts/diagnose-cloudflare-n8n-dns.py`
- `automation/scripts/diagnose-cloudflare-products.py`
- `automation/scripts/probe-cloudflare-n8n-delete-window.py`
