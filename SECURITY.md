# Security Policy

## Reporting a Vulnerability

This repo contains educational materials from a security talk: slides, AI prompts, a CloudFormation template, and two static HTML diagrams. There is no running service to exploit.

The one thing here that genuinely matters: the diagrams under `docs/demos/` were generated against a real AWS account and then scrubbed. If you spot **anything** in them that still identifies real infrastructure, that is a real finding and I want to hear about it immediately.

1. **Email me:** skye@fugate.dev
2. **Include:** What you found and where
3. **Response time:** I'll get back to you within 48 hours

For a suspected data leak, please email rather than opening a public issue.

## Scope

**In scope:**
- Any production identifier surviving in the published diagrams — account IDs, resource IDs, hosted zones, namespaces, routable addresses, internal DNS names, or organisation names
- Gaps in `scripts/sanitize.py` that would let such data through
- The CloudFormation template in `iac/` encouraging an insecure pattern
- Prompts that could be misused for malicious purposes
- Misleading security advice in the documentation

**Out of scope:**
- The AI models themselves (I don't control those)
- Third-party tools mentioned in the demos
- The `allowedTools` list in `prompts/GLaDOS.json` — it is deliberately permissive for stage use and is documented as such in `prompts/README.md`. Copying it into production is the hazard, and that warning is the point.
- Theoretical attacks requiring significant modification

## How the diagrams were scrubbed

`scripts/sanitize.py` rewrites every identifier deterministically. Replacements use reserved ranges only:

| Real | Published |
|---|---|
| Account ID | `123456789012` (AWS documentation account) |
| Internal IPv4 | `10.20.0.0/16` |
| Routable IPv4 | `203.0.113.0/24` (RFC 5737) |
| IPv6 | `2001:db8::/32` (RFC 3849) |
| Resource / zone / namespace IDs | Regenerated, same shape and length |
| Organisation and environment names | Generic stand-ins |

The account number and organisation token are supplied via environment variables and are never committed. The script re-audits its own output and can be run standalone:

```bash
python3 scripts/sanitize.py --check docs/demos/*.html
```

This runs in CI on every push. It is not a substitute for someone actually looking, which is why the section above exists.

## Disclosure

If you report something valid, I'll:
- Fix it promptly, and rewrite history if the leak is in a committed file
- Credit you (unless you prefer anonymity)
- Update the materials and note the change

Thanks for helping keep this educational content safe and responsible.
