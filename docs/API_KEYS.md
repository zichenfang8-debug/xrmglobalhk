# API Keys and Local Secrets

This project uses local environment files for automation credentials. Do not commit real tokens, API keys, client secrets, OAuth secrets, or passwords.

## Cloudflare DNS Automation

Create a Cloudflare API Token with the minimum permissions below:

- Zone -> Zone -> Read
- Zone -> DNS -> Read
- Zone -> DNS -> Edit

Resource scope:

- Include -> Specific Zone -> `xrmglobalhk.com`

Add the token to a local `.env` file in the project root:

```bash
CF_API_TOKEN=
```

The DNS repair script reads secrets in this order:

1. `.env`
2. `.env.local`
3. `.env.production`
4. Process environment
5. `launchctl` environment
6. macOS Keychain

Recommended local setup:

```bash
cp .env.example .env
python3 -m pip install -r requirements.txt
```

Then edit `.env` locally and paste the Cloudflare token after `CF_API_TOKEN=`.

## Safety Rules

- Never commit `.env`.
- Never paste API tokens into chat.
- Never print API tokens in terminal output.
- Use least-privilege tokens.
- Rotate tokens if they are accidentally exposed.
- Keep Cloudflare DNS automation scoped only to the `xrmglobalhk.com` zone.

## Verification Command

After `.env` is configured:

```bash
python3 automation/scripts/fix-cloudflare-n8n-dns.py
```

Successful DNS repair must show `n8n.xrmglobalhk.com` resolving to `178.105.167.227` through Cloudflare authoritative nameservers and public resolvers.
