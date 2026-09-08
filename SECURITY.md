# Security Policy

## Reporting a Vulnerability

This repo contains educational materials from a security talk: slides, AI prompts, a CloudFormation template, and two static HTML diagrams. There's no running code or services to exploit.

If you find something concerning in the prompts or materials:

1. **Email me:** skye@fugate.dev
2. **Include:** What you found and why it's a concern
3. **Response time:** I'll get back to you within 48 hours

## Scope

**In scope:**
- Prompts that could be misused for malicious purposes
- Sensitive information accidentally included in materials
- The CloudFormation template in `iac/` encouraging an insecure pattern
- Misleading security advice in documentation

**Out of scope:**
- The AI models themselves (I don't control those)
- Third-party tools mentioned in demos
- The `allowedTools` list in `prompts/GLaDOS.json` — it's deliberately permissive for stage use and documented as such in `prompts/README.md`. Copying it into production is the hazard, and that warning is the point.
- Theoretical attacks that require significant modification

## Disclosure

If you report something valid, I'll:
- Fix it promptly
- Credit you (unless you prefer anonymity)
- Update materials and notify anyone who downloaded them

Thanks for helping keep this educational content safe and responsible.
