# My Network Has Commitment Issues: AI Debugged Its Feelings

**<a href="https://seckc.org/" target="_blank">SecKC</a> Talk - September 2026**

Networks promise reliability but ghost you at 3 AM. I got tired of reading logs, so I taught AI to be my troubleshooting partner. This is the SecKC cut: less incident response, more architecture — mapping what you actually have, finding what breaks the most when it fails, and getting the diagram to write itself.

This repo has everything from the talk.

**<a href="https://skyefugate.github.io/2026-09-SecKC-AI-Talk/" target="_blank">→ Live site with the interactive diagrams</a>**

## What's Here

**Slides (PDF)** — The full deck: [`docs/slides/slides.pdf`](docs/slides/slides.pdf).

**Demos** — Three demos, each generated live on stage from one prompt:

1. **<a href="https://skyefugate.github.io/2026-09-SecKC-AI-Talk/demos/network-map.html" target="_blank">Network Mapping & Discovery</a>** — "Discover this AWS environment and show me the paths and dependencies that matter." Inventory, route intent, and dependencies in one interactive map. Nobody drew this.

2. **<a href="https://skyefugate.github.io/2026-09-SecKC-AI-Talk/demos/blast-radius.html" target="_blank">Architecture Review</a>** — "Which failure points create the largest blast radius?" Ranked failure points, request path propagation, and the AZ concentration nobody had noticed.

3. **Architecture Documentation** *(live, in this repo)* — "Write a script that runs on GitHub Actions that as I push an IaC change it will update my architecture documentation." The CloudFormation template is committed at [`iac/vpc-baseline/`](iac/vpc-baseline/). The workflow and the Mermaid diagram are not — writing them is the demo.

All three prompts, verbatim, are in **[prompts/demo-prompts.md](prompts/demo-prompts.md)**.

## Prompts, Persona, and Skills

The actual configuration behind the demos:

- **[GLaDOS.json](prompts/GLaDOS.json)** — The agent definition. The persona is one line. That is not a typo, and it's the most useful thing in this repo.
- **[NETWORK_AGENT.md](prompts/NETWORK_AGENT.md)** — Prompting structure: Identity → Mission → Guardrails → Output
- **[f5-virtual-server-discovery](prompts/skills/f5-virtual-server-discovery.md)** — Skill structure: Trigger → Procedure → Resources → Result

Prompting is how I want you to *think*. Skills are how I want you to *do a thing*. MCP is how you *reach* the world. Keep those three separate and none of them has to be enormous. See **[prompts/](prompts/)**.

## The Point

Your network is a set of highways built decades apart. Some segments predate you and everything still runs on them. Practice drifts from design — diagrams lie, configs drift, and undocumented changes live in prod forever. The signals are great for incident response and useless for understanding ordinary behavior, because there are too many of them. And validating the network against spec is so tedious that nobody does it.

AI reads faster than you, never gets bored, and will happily do the tedious pass you keep postponing.

It is not a replacement for expertise — you drive the outcome. It is not magic; it needs good data and good prompts. It is not psychic, and if you don't tell it, it will gaslight it. And it is absolutely not safe without review: word something badly and it will execute it with enthusiasm.

## Safety, Because It Matters

AI tools act with **your** permissions, which makes you accountable for what you approve. Treat it like any teammate with root access.

If you let it log in as admin, and ask it to troubleshoot a routing issue, and it suggests deleting an ARP entry, and you hit *Yes*?

You deleted the ARP entry.

Please be responsible <3

## How to Take This Home

- Your routers and firewalls are just fancy boxes. Put their configs in GitHub.
- Document your cloud environments as IaC.
- Connect your AI tooling to your environment — and if you did the two things above, the safest and easiest way is to point it at your as-code documents rather than at the live gear.
- Give it a read-only account and let it fly during an outage.

## Want More?

I wrote a <a href="https://skye.fugate.dev/blog/posts/my-network-has-commitment-issues" target="_blank">full blog post</a> about this with the practical how-to guide, real examples, and lessons learned (including the time AI `rm -rf`'d my data directory).

The December 2025 SecDSM version of this talk — C2 detection, Linux compromise analysis, and flow log forensics — is at <a href="https://github.com/skyefugate/2025-12-SecDSM-AI-Talk" target="_blank">2025-12-SecDSM-AI-Talk</a>.

## Questions?

Hit me up. I'm happy to talk about AI, networking, or why your diagram is wrong.

Oh, and remember: **Be polite to AI. You never know what's coming.**

## License

This work is licensed under [CC BY 4.0](LICENSE). Use it, remix it, share it — just give credit and link back to <a href="https://skye.fugate.dev" target="_blank">skye.fugate.dev</a>.
