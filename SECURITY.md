# Security policy

## Scope

safeAI is a self-assessment toolkit. It runs locally: the command-line tool reads and writes files on your machine, and the browser tool (`web/index.html`) keeps answers in your browser and uploads nothing. It makes no network calls.

Reports we want to hear about include:

- A flaw that could cause the tool to execute code, leak answers, or write outside the files you point it at (for example through a crafted assessment file).
- The browser tool sending data anywhere, or loading remote code.
- A control in the framework that gives dangerously wrong advice.

## Reporting

Please use GitHub's **private vulnerability reporting** on this repository (Security tab, "Report a vulnerability"). Do not open a public issue describing a security problem. Include what you found, how to reproduce it, and the version.

If that option does not appear, open a public issue that says only "security report, please contact me" with no technical details, and a maintainer will arrange a private channel.

We will acknowledge a report as soon as we reasonably can. This is a volunteer-maintained project, so we cannot promise a fixed response time.

## Assessment files are sensitive

Your completed assessment describes your organization's weaknesses. Treat it like any other security document: do not commit a real assessment to a public repository, and share reports only with people who should see them.
