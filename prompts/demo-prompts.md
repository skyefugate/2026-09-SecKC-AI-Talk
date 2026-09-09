# The demo prompts

Verbatim, including the bits that are not grammatical. These are what was typed on
stage — no hidden setup turn, no pre-warmed context.

Each one ends with an explicit output format. That clause is doing a lot of work:
without it you get prose, and prose does not project well to a room of 300 people.

---

## Demo 1 — Network Mapping & Discovery

*Network folks get pulled into new issues all the time. We need a way to quickly
view the network.*

```
Hi GLaDOS, discover this AWS environment and show me the paths and dependencies
that matter. Express this output as a HTML/CSS interactive diagram.
```

**Watch for:** the map should connect inventory to route intent and show our
dependencies.

**Result:** [network-map.html](../docs/demos/network-map.html) &middot;
[hosted](https://skyefugate.github.io/2026-09-SecKC-AI-Talk/demos/network-map.html)

Note what is *not* in the prompt: no list of services to check, no regions, no
resource types. "The paths and dependencies that matter" is the entire spec.
Deciding what matters is the judgment you are delegating.

---

## Demo 2 — Architecture Reviews

*As we look to update our networks, we look to redesign our architectures. AI can
be a GREAT sounding board here.*

```
Hi GLaDOS, Review the architecture in this AWS environment. Which failure points
create the largest blast radius? Express this output as a HTML/CSS interactive
diagram.
```

**Watch for:** quick and easy to understand failure points.

**Result:** [blast-radius.html](../docs/demos/blast-radius.html) &middot;
[hosted](https://skyefugate.github.io/2026-09-SecKC-AI-Talk/demos/blast-radius.html)

"Largest blast radius" forces ranking, and ranking forces the model to commit to an
opinion instead of listing everything it found. Ask for a list, get a list. Ask for
an order, get an argument you can push back on.

---

## Demo 3 — Extra credit: Architecture DOCUMENTATION

*When was the last time you updated your diagram when we put a band-aid fix in?
Right… mhmm? For environments managed as code we can automagically generate them.*

```
Hi GLaDOS, write a script that runs on GitHub Actions that as I push an IaC change
it will update my architecture documentation. Express this as a living README doc
using Mermaid in the folder of our IaC template in this repo.
```

**Watch for:** a quick and easy to understand architectural diagram.

**Target:** [`iac/vpc-baseline/`](../iac/vpc-baseline/)

This one runs live against this repository. The template is committed; the generator,
the workflow, and the Mermaid README are what get written on stage. They are in the
repo now so you can read them afterwards — see [`iac/README.md`](../iac/README.md).

The result is deliberately small: one ~100-line Python script, a 25-line workflow, and
one diagram. It reads `Ref` and `Fn::GetAtt` and nothing else. It is not a
CloudFormation evaluator, and it does not need to be — the point is that the diagram
changes when the infrastructure changes, not that the tool is clever.

Mermaid rather than an image on purpose — it renders natively on GitHub, it diffs
as text, and a diagram that lives in a pull request is a diagram that gets
reviewed.

---

## Why they are all this short

The prompts are short because the agent is not short on context. It has skills for
procedure and MCP servers for access. Prompt length is a symptom: if you find
yourself writing paragraph six of instructions, stop and write a skill instead.

And every one of these ran with real permissions against a real account. Read what it proposes before you approve it. If you let it log in as admin
and it suggests deleting an ARP entry and you hit yes, you deleted the ARP entry.
