# Infrastructure as Code

This folder contains the CloudFormation environment used in the talk demos.

- [`vpc-baseline/`](vpc-baseline/) — a simple three-tier AWS environment
- [`template.yaml`](vpc-baseline/template.yaml) — the source of truth
- [`README.md`](vpc-baseline/README.md) — architecture documentation generated from the template

## Demo

The idea is simple:

**IaC changes → GitHub Actions runs → architecture documentation updates automatically.**

The generated documentation uses Mermaid so the diagram lives alongside the code, can be reviewed in Git, and stays tied to the infrastructure it describes.

The environment is intentionally ordinary. The interesting part is not the AWS architecture.

It's that the architecture can document itself.
