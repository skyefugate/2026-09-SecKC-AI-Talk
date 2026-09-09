# My Network Has Commitment Issues: AI Debugged Its Feelings

**SecKC • September 2026**

A talk about using AI for network discovery, architecture review, living documentation, and packet analysis.

[**→ Interactive demos**](https://skyefugate.github.io/2026-09-SecKC-AI-Talk/)  
[**→ Slides**](docs/slides/slides.pdf)

![Title card reading "My Artisanal AI Slopitecture", trademark, asterisk. Footnote: patent NOT pending. Behind it, Tony Stark waving a holographic globe around his workshop.](docs/assets/img/slopitecture.jpg)

## Demos

1. **Network Mapping & Discovery**  
   Discover an AWS environment and map the paths and dependencies that matter.

2. **Architecture Review**  
   Find the failure points with the largest blast radius.

3. **Living Architecture Documentation**  
   Change the IaC, let GitHub Actions regenerate the architecture diagram.

4. **PCAP Threat Hunting**  
   Give a [threat-hunter persona](prompts/THREAT_HUNTER.md) a packet capture and let it investigate the traffic.

All demo prompts are in [**prompts/demo-prompts.md**](prompts/demo-prompts.md).

## My Setup

![Architecture diagram: the Kiro CLI drives an agent called GLaDOS. GLaDOS branches to two groups. Skills covers web design, routing and switching, and API interaction. MCPs covers the AWS command line, Bash, and GitHub via the gh CLI. A worked example runs alongside: asking to check route table rtb-0abc123, GLaDOS selecting the AWS command line, running aws ec2 describe-route-tables with that ID, and getting back two active routes.](docs/assets/img/my-setup.png)

- [**GLaDOS.json**](prompts/GLaDOS.json) — persona
- [**NETWORK_AGENT.md**](prompts/NETWORK_AGENT.md) — how I want the agent to think
- [**Skills**](prompts/skills/) — how I want it to do specific things
- MCP / CLI tools — access to the real world

**Prompts tell it how to think. Skills tell it how to do things. Tools let it reach things.**

## The Point

Networks are messy. Diagrams drift. Configs accumulate history. Telemetry piles up.

AI is very good at doing the tedious first pass.

Give it good context. Give it the minimum access it needs. Review what it proposes.

If you approve a bad command, congratulations:

**you ran the bad command.**

## More

[**Full blog post**](https://skye.fugate.dev/blog/posts/my-network-has-commitment-issues)  
[**2025 SecDSM version**](https://github.com/skyefugate/2025-12-SecDSM-AI-Talk)

## License

[**CC BY 4.0**](LICENSE)

Steal this responsibly.
