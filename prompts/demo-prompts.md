# The demo prompts

Verbatim, including the bits that are not grammatical. These are what was typed on
stage — no hidden setup turn, no pre-warmed context.

The first three end with an explicit output format. That clause is doing a lot of
work: without it you get prose, and prose does not project well to a room of 300
people. The fourth does not need it, because the output contract is baked into the
persona instead — which is the trade-off worth understanding.

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

## Demo 4 — Investigating a 1.7 GB packet capture

*A capture that size is not something you open in Wireshark and scroll. It is
something you ask a question of.*

This one is not a one-liner, and it is the exception that proves the rule. The
prompt is short because the *persona* is long — the whole investigative method
lives in [`THREAT_HUNTER.md`](THREAT_HUNTER.md), so the turn itself is just the
evidence pointer:

```
Please find your evidence located at:
capture.pcap
```

**Watch for:** it never dumps the packets. The persona forbids it explicitly —
targeted `tshark` with timeouts, statistical summaries, extracted indicators. A
1.7 GB file will not fit in a context window and an agent that tries to inline it
burns your budget and tells you nothing.

**Persona:** [`THREAT_HUNTER.md`](THREAT_HUNTER.md) — carried over unchanged from
the [December 2025 SecDSM talk](https://github.com/skyefugate/2025-12-SecDSM-AI-Talk),
where it ran against VPC flow logs instead.

Note the shape of that file: Identity → Mission → Critical Performance Rules →
Objectives → Approach → Deliverable Format → Rules of Engagement → Voice. The
longest sections are the *output contract* and the *don't-do-this* list. That is
where persona length earns its keep — not in explaining what a TCP handshake is,
but in pinning down what a finding has to look like before you will accept it.

The GLaDOS persona is one line because the network demos delegate procedure to
skills. This one is 140 lines because forensic judgment *is* the procedure, and
there is no tool call that encodes "decide what matters in a packet capture."
