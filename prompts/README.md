# Prompts, persona, and skills

The split that makes this work:

| | Answers | Lives in |
|---|---|---|
| **Prompting** | How I want you to *think* | agent definition / `NETWORK_AGENT.md` |
| **Skills** | How I want you to *do a thing* | `SKILL.md` per procedure |
| **MCP** | How you *reach* the world | server config |

Prompting is judgment. Skills are procedure. MCP is access. Conflating them is how
you end up with a 900-line prompt that still cannot log into a switch.

## The agent

[`GLaDOS.json`](GLaDOS.json) is the real definition, with two work-specific MCP
servers removed and nothing else changed. Brace yourself:

```
"prompt": "You are GLaDOS from Portal. Be helpful but with a subtle
           sarcastic edge. Focus on getting things done efficiently."
```

That is the whole persona. One line.

This surprises people who expect the intelligence to live in the prompt. It does
not. It lives in the **skills** the agent can reach and the **access** it has. The
persona is tone, plus a nudge toward brevity. Everything that makes the demos work
is in the other two columns of that table.

The useful part of the file is `resources`:

```json
"resources": ["skill://~/.agents/skills/**/SKILL.md"]
```

Every skill on disk is discoverable. The agent picks the relevant one from the
task — you say "check route table `rtb-0abc123`", it selects the AWS CLI skill, runs
`aws ec2 describe-route-tables`, and hands back the routes.

### Read the `allowedTools` list before you copy this

That block pre-approves `execute_bash`, `fs_write`, and `use_aws`. The description
field says "auto-approves all tools for maximum efficiency", which is an honest
label for a loaded gun. It is set that way because standing on stage clicking
*Allow* forty times is worse television than the alternative.

Do not copy that setting into anything that touches production you care about. AI
tools act with *your* permissions, which makes you accountable for what you approve
— and pre-approval is still approval, just earlier and with less attention.

## Structure

Both file types follow a fixed shape. That consistency is what makes them
composable.

**Prompting** — `Identity → Mission → Guardrails → Output`
See [`NETWORK_AGENT.md`](NETWORK_AGENT.md).

**Skills** — `Trigger → Procedure → Resources → Result`
See [`skills/f5-virtual-server-discovery.md`](skills/f5-virtual-server-discovery.md).

Guardrails are the section people skip and then regret.

## The demo prompts

All four, verbatim, in [`demo-prompts.md`](demo-prompts.md). The first three are
deliberately short: if your prompt needs to be long, the thing you actually need is
a skill.

The fourth is the counter-example. [`THREAT_HUNTER.md`](THREAT_HUNTER.md) is 140
lines, and the prompt that invokes it is a filename. Forensic judgment cannot be
factored out into a skill — there is no tool call for "decide what matters in a
1.7 GB packet capture" — so it lives in the persona, and the persona spends most of
its length on the output contract and the list of things not to do.
