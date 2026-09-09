#!/usr/bin/env python3
"""Draw an architecture diagram from a CloudFormation template.

This does lightweight dependency discovery, not CloudFormation evaluation. It
reads Ref and Fn::GetAtt, keeps the resources an architect would put on a
whiteboard, and collapses the plumbing in between. That is enough to keep a
diagram honest about what depends on what.

    python3 scripts/generate-architecture.py [template.yaml ...]

Writes README.md next to each template. Defaults to iac/*/template.yaml.
"""

import sys
from pathlib import Path

import yaml

# The resources worth drawing, and what to call them. Everything else -- route
# tables, subnet associations, IAM, log groups -- is plumbing: it still carries
# dependencies through the graph, it just does not get a box.
#
# The order matters: it doubles as the left-to-right layout convention, used when
# the template wires two of these together without saying which end is upstream.
INTERESTING = {
    "AWS::EC2::RouteTable": "Route Table",
    "AWS::EC2::InternetGateway": "Internet Gateway",
    "AWS::EC2::EgressOnlyInternetGateway": "Egress-Only IGW",
    "AWS::EC2::NatGateway": "NAT Gateway",
    "AWS::EC2::VPCEndpoint": "VPC Endpoint",
    "AWS::EC2::SecurityGroup": "Security Group",
    "AWS::ElasticLoadBalancingV2::LoadBalancer": "Load Balancer",
    "AWS::ElasticLoadBalancingV2::TargetGroup": "Target Group",
    "AWS::AutoScaling::AutoScalingGroup": "Application",
    "AWS::RDS::DBInstance": "Database",
}


def loader():
    """A YAML loader that tolerates CloudFormation's !Ref / !GetAtt shorthand."""

    class CfnLoader(yaml.SafeLoader):
        pass

    def tag(load, suffix, node):
        name = "Ref" if suffix == "Ref" else "Fn::" + suffix
        if isinstance(node, yaml.ScalarNode):
            value = load.construct_scalar(node)
            if suffix == "GetAtt":
                value = value.split(".")
        elif isinstance(node, yaml.SequenceNode):
            value = load.construct_sequence(node, deep=True)
        else:
            value = load.construct_mapping(node, deep=True)
        return {name: value}

    CfnLoader.add_multi_constructor("!", tag)
    return CfnLoader


def find_refs(node):
    """Every logical ID this chunk of template points at, via Ref or GetAtt."""
    found = set()
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "Ref" and isinstance(value, str):
                found.add(value)
            elif key == "Fn::GetAtt":
                target = (
                    value[0] if isinstance(value, list) else str(value).split(".")[0]
                )
                found.add(target)
            else:
                found |= find_refs(value)
    elif isinstance(node, list):
        for item in node:
            found |= find_refs(item)
    return found


def reach(start, resources, seen):
    """Interesting resources `start` depends on, tunnelling through plumbing."""
    out = set()
    for name in find_refs(resources.get(start, {})):
        if name not in resources or name in seen:
            continue
        seen.add(name)
        if resources[name].get("Type") in INTERESTING:
            out.add(name)
        else:
            out |= reach(name, resources, seen)
    return out


def diagram(resources):
    kept = [n for n, r in resources.items() if r.get("Type") in INTERESTING]
    deps = {n: reach(n, resources, {n}) for n in resources}
    rank = {t: i for i, t in enumerate(INTERESTING)}

    lines = ["flowchart LR", "    Internet([Internet])"]
    for name in kept:
        lines.append(f'    {name}["{name}<br>{INTERESTING[resources[name]["Type"]]}"]')

    # A resource that Refs another one leans on it. Draw the arrow the other way
    # round, so it points along the direction traffic and blast radius travel.
    edges = {(dep, name) for name in kept for dep in deps[name]}

    # Plumbing that wires two of these together -- a route, a listener -- becomes
    # the wire itself. The template does not say which end is upstream, so fall
    # back to the order the types are listed above.
    for name, refs in deps.items():
        if resources[name].get("Type") not in INTERESTING and len(refs) > 1:
            ends = sorted(refs, key=lambda r: rank[resources[r]["Type"]])
            edges |= {(a, b) for i, a in enumerate(ends) for b in ends[i + 1 :]}

    lines += [f"    {a} --> {b}" for a, b in sorted(edges)]
    lines += [
        f"    Internet --> {name}"
        for name in kept
        if resources[name]["Type"].endswith(("InternetGateway", "LoadBalancer"))
    ]
    return "\n".join(lines)


def render(path):
    template = yaml.load(path.read_text(), Loader=loader())
    resources = template.get("Resources", {})
    title = path.parent.name.replace("-", " ").title()
    return (
        f"# {title} — Architecture\n\n"
        f"Generated from [`{path.name}`]({path.name}) by "
        "[`scripts/generate-architecture.py`](../../scripts/generate-architecture.py). "
        "Do not edit by hand.\n\n"
        "This performs lightweight dependency discovery rather than implementing a "
        "CloudFormation evaluator. CloudFormation already understands "
        "CloudFormation; the diagram only needs to know what leans on what.\n\n"
        "```mermaid\n" + diagram(resources) + "\n```\n\n"
        f"{len(resources)} resources in the template.\n"
    )


def main(argv):
    paths = [Path(a) for a in argv] or sorted(Path("iac").glob("*/template.yaml"))
    if not paths:
        sys.exit("no templates found")
    for path in paths:
        out = path.parent / "README.md"
        out.write_text(render(path))
        print(f"wrote {out}")


if __name__ == "__main__":
    main(sys.argv[1:])
