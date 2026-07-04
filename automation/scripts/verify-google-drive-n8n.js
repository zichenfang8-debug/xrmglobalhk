#!/usr/bin/env node

const { spawnSync } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");

const workspace = process.cwd();
const credentialId = process.env.N8N_GOOGLE_DRIVE_CREDENTIAL_ID || "48NFhX6TRjXw7ITP";
const reportPath = path.join(workspace, "automation/reports/google-drive-n8n-claude-verification.md");
const nodePath = "/Users/zichenfang/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin";
const n8nUserFolder = path.join(workspace, ".n8n-local");
const n8nBin = path.join(workspace, ".n8n-local/runtime/node_modules/.bin/n8n");

function runN8nExport() {
  const result = spawnSync(n8nBin, ["export:credentials", "--id", credentialId, "--decrypted"], {
    cwd: workspace,
    encoding: "utf8",
    env: {
      ...process.env,
      PATH: `${nodePath}:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin`,
      N8N_USER_FOLDER: n8nUserFolder,
    },
  });

  if (result.status !== 0) {
    throw new Error(`n8n credential export failed: ${(result.stderr || result.stdout).trim()}`);
  }

  const raw = result.stdout.trim();
  const firstJson = raw.indexOf("[") >= 0 ? raw.slice(raw.indexOf("[")) : raw.slice(raw.indexOf("{"));
  return JSON.parse(firstJson);
}

function getCredentialData(exported) {
  const credential = Array.isArray(exported) ? exported[0] : exported;
  if (!credential || !credential.data) throw new Error("No credential data returned by n8n export.");
  return credential.data;
}

async function driveRequest(url, token, options = {}) {
  const response = await fetch(url, {
    ...options,
    headers: {
      Authorization: `Bearer ${token}`,
      ...(options.headers || {}),
    },
  });
  const bodyText = await response.text();
  let body = bodyText;
  try {
    body = bodyText ? JSON.parse(bodyText) : {};
  } catch {
    // Keep text body.
  }
  if (!response.ok) {
    throw new Error(`Google Drive API ${response.status}: ${typeof body === "string" ? body : JSON.stringify(body)}`);
  }
  return body;
}

async function findOrCreateFolder(token, name) {
  const q = encodeURIComponent(`name='${name.replace(/'/g, "\\'")}' and mimeType='application/vnd.google-apps.folder' and trashed=false`);
  const existing = await driveRequest(
    `https://www.googleapis.com/drive/v3/files?q=${q}&fields=files(id,name,webViewLink)&pageSize=10`,
    token,
  );
  if (existing.files?.length) return { ...existing.files[0], created: false };

  const folder = await driveRequest("https://www.googleapis.com/drive/v3/files?fields=id,name,webViewLink", token, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, mimeType: "application/vnd.google-apps.folder" }),
  });
  return { ...folder, created: true };
}

async function uploadTextFile(token, folderId, name, content) {
  const boundary = `n8n_xrm_${Date.now()}`;
  const metadata = { name, parents: [folderId], mimeType: "text/markdown" };
  const body = [
    `--${boundary}`,
    "Content-Type: application/json; charset=UTF-8",
    "",
    JSON.stringify(metadata),
    `--${boundary}`,
    "Content-Type: text/markdown; charset=UTF-8",
    "",
    content,
    `--${boundary}--`,
    "",
  ].join("\r\n");

  return await driveRequest("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id,name,mimeType,webViewLink", token, {
    method: "POST",
    headers: { "Content-Type": `multipart/related; boundary=${boundary}` },
    body,
  });
}

async function readTextFile(token, fileId) {
  return await driveRequest(`https://www.googleapis.com/drive/v3/files/${fileId}?alt=media`, token);
}

async function updateTextFile(token, fileId, content) {
  return await driveRequest(`https://www.googleapis.com/upload/drive/v3/files/${fileId}?uploadType=media&fields=id,name,modifiedTime`, token, {
    method: "PATCH",
    headers: { "Content-Type": "text/markdown; charset=UTF-8" },
    body: content,
  });
}

async function trashFile(token, fileId) {
  return await driveRequest(`https://www.googleapis.com/drive/v3/files/${fileId}?fields=id,name,trashed`, token, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ trashed: true }),
  });
}

function localSummary(content) {
  return [
    "This test note confirms the XRM Nightly AI Workflow intake path.",
    "It should be classified as website-content, ai-infrastructure, and workflow-verification material.",
    `Input length: ${content.length} characters.`,
  ].join(" ");
}

async function claudeSummary(content) {
  const key = process.env.ANTHROPIC_API_KEY || process.env.CLAUDE_API_KEY;
  if (!key) {
    return {
      ok: false,
      status: "Claude API key not configured",
      summary: localSummary(content),
      usedFallback: true,
    };
  }

  const response = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-api-key": key,
      "anthropic-version": "2023-06-01",
    },
    body: JSON.stringify({
      model: process.env.CLAUDE_MODEL || "claude-3-5-sonnet-20241022",
      max_tokens: 300,
      messages: [
        {
          role: "user",
          content: `Summarize and classify this workflow test note in 3 bullets. Do not include sensitive data.\n\n${content}`,
        },
      ],
    }),
  });
  const body = await response.json();
  if (!response.ok) throw new Error(`Claude API ${response.status}: ${JSON.stringify(body)}`);
  return {
    ok: true,
    status: "Claude API call succeeded",
    summary: body.content?.map((item) => item.text).filter(Boolean).join("\n") || "",
    usedFallback: false,
  };
}

async function main() {
  const startedAt = new Date();
  const exported = runN8nExport();
  const credentialData = getCredentialData(exported);
  const token = credentialData.oauthTokenData?.access_token;
  if (!token) throw new Error("n8n Google Drive credential does not contain oauthTokenData.access_token.");

  const folder = await findOrCreateFolder(token, "Incoming Notes");
  const testName = `xrm-n8n-drive-claude-test-${startedAt.toISOString().replace(/[:.]/g, "-")}.md`;
  const originalContent = [
    "# XRM Nightly Workflow Test",
    "",
    "This is a controlled test file for Google Drive to n8n to Claude verification.",
    "Business context: AI infrastructure supply, China procurement partner, website draft generation.",
    "Privacy marker: no hotel client names, no Wang Ge information, no internal contacts, no seals.",
    "",
    `Created at: ${startedAt.toISOString()}`,
  ].join("\n");
  const file = await uploadTextFile(token, folder.id, testName, originalContent);
  const readBack = await readTextFile(token, file.id);
  const updatedContent = `${readBack}\n\nUpdate check: n8n credential read/write verification completed at ${new Date().toISOString()}.\n`;
  const updateResult = await updateTextFile(token, file.id, updatedContent);
  const readUpdated = await readTextFile(token, file.id);
  const aiResult = await claudeSummary(readUpdated);
  const trashResult = await trashFile(token, file.id);

  const report = `# Google Drive to n8n to Claude Verification

Date: ${new Date().toISOString()}

## Workflow Status

Status: ${aiResult.ok ? "Passed with Claude" : "Partially passed - Claude not configured"}

## Test File

- Google Drive folder: Incoming Notes
- Folder ID: ${folder.id}
- Folder created during test: ${folder.created ? "Yes" : "No"}
- Test file name: ${testName}
- Test file ID: ${file.id}
- Test file trashed after verification: ${trashResult.trashed ? "Yes" : "No"}

## Google Drive Read Result

- Create file: Passed
- Read original file: ${readBack.includes("XRM Nightly Workflow Test") ? "Passed" : "Failed"}
- Update file: ${updateResult.id ? "Passed" : "Failed"}
- Read updated file: ${readUpdated.includes("Update check") ? "Passed" : "Failed"}
- Archive/delete test file: ${trashResult.trashed ? "Passed" : "Failed"}

## n8n Credential Result

- Credential ID: ${credentialId}
- Credential type: googleDriveOAuth2Api
- OAuth token present in n8n credential: Yes
- Drive API access through n8n credential token: Passed

## AI Processing Result

- Claude status: ${aiResult.status}
- Fallback summary used: ${aiResult.usedFallback ? "Yes" : "No"}

### Summary

${aiResult.summary}

## Remaining Configuration Issues

${aiResult.ok ? "- None for Google Drive and Claude verification." : "- Claude API key is not configured in the local environment, so the final Claude API call could not be executed. The report includes a deterministic local fallback summary only."}
- GitHub token is not configured locally.
- Cloudflare API token is not configured locally.
- Draft branch commit and Cloudflare preview are pending GitHub/Cloudflare authorization.
`;

  fs.mkdirSync(path.dirname(reportPath), { recursive: true });
  fs.writeFileSync(reportPath, report, "utf8");
  console.log(JSON.stringify({
    ok: true,
    reportPath,
    folderId: folder.id,
    testFileName: testName,
    testFileId: file.id,
    trashed: trashResult.trashed,
    claude: aiResult.status,
  }, null, 2));
}

main().catch((error) => {
  console.error(JSON.stringify({ ok: false, error: error.message }, null, 2));
  process.exit(1);
});
