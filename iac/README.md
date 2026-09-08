# Infrastructure as code

One CloudFormation stack lives here: [`vpc-baseline/`](vpc-baseline/).

52 resources describing an ordinary three-tier, three-AZ, dual-stack environment.
Public edge behind an ALB, an autoscaled application tier, an isolated Postgres data
tier with an optional read replica. Nothing exotic, because the point is not the
architecture — the point is that the architecture is *readable by a machine*.

Addressing is documentation-range only (`10.20.64.0/18`). No secrets: the database
password is managed by Secrets Manager, and instance access is Session Manager only.
There is no inbound SSH anywhere in the file.

## Why this exists

Demo 3 of the talk is this prompt, run live against this repository:

> Hi GLaDOS, write a script that runs on GitHub Actions that as I push an IaC
> change it will update my architecture documentation. Express this as a living
> README doc using Mermaid in the folder of our IaC template in this repo.

So `vpc-baseline/README.md` is **intentionally missing**, and so is the workflow
that generates it. Those two files are the deliverable. If they were already
committed, the demo would be a magic trick with the rabbit visible in the hat.

If you are reading this after the talk and those files exist now: that is what got
written on stage.

## Things in the template worth diagramming

The layout is deliberately boring, but several decisions are load-bearing and should
show up clearly in any diagram worth having:

- **One NAT gateway** in AZ `a`, shared by all three application subnets. Cheapest
  option, and a real single point of failure for IPv4 egress. Left in on purpose.
- **Asymmetric egress.** IPv4 leaves through the NAT; IPv6 leaves through an
  egress-only internet gateway. Same traffic, two different failure domains.
- **S3 over a gateway endpoint**, not the NAT — and the endpoint is IPv4-only while
  the load balancer is dual-stack.
- **No default route on the data tier.** Isolation by routing, not by security group
  alone.
- **`EnableReadReplica`** is the single biggest blast-radius toggle in the file. Turn
  it off and every read lands on the primary.
- **Health checking is chained**: ALB → target group → ASG (`HealthCheckType: ELB`).
  A bad `/healthz` does not just fail a check, it replaces instances.
- **`app.<env>.internal` is an alias to the ALB**, so DNS follows the load balancer
  rather than any instance.

A generated diagram that misses the NAT concentration is not a useful diagram.

## Deploying it

You do not need to deploy anything to follow the talk. If you want to:

```bash
aws cloudformation deploy \
  --template-file iac/vpc-baseline/template.yaml \
  --stack-name acme-use2-baseline \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides EnvironmentName=acme-use2
```

Validate or lint without deploying, which is what CI does:

```bash
aws cloudformation validate-template \
  --template-body file://iac/vpc-baseline/template.yaml

cfn-lint iac/vpc-baseline/template.yaml
```

Two things to know before you run it. It creates a Multi-AZ RDS instance and a NAT
gateway, neither of which is free. And `DbPrimary` sets `DeletionProtection: true`
with a `Snapshot` deletion policy, so deleting the stack will not delete the
database until you clear that flag yourself — deliberate, and mildly annoying, which
is the correct trade for a production pattern.

Read it before you run it. That is the entire moral of the talk.
