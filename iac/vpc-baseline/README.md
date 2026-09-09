# Vpc Baseline — Architecture

Generated from [`template.yaml`](template.yaml) by [`scripts/generate-architecture.py`](../../scripts/generate-architecture.py). Do not edit by hand.

This performs lightweight dependency discovery rather than implementing a CloudFormation evaluator. CloudFormation already understands CloudFormation; the diagram only needs to know what leans on what.

```mermaid
flowchart LR
    Internet([Internet])
    InternetGateway["InternetGateway<br>Internet Gateway"]
    EgressOnlyIgw["EgressOnlyIgw<br>Egress-Only IGW"]
    NatGateway["NatGateway<br>NAT Gateway"]
    PublicRouteTable["PublicRouteTable<br>Route Table"]
    AppRouteTable["AppRouteTable<br>Route Table"]
    DataRouteTable["DataRouteTable<br>Route Table"]
    S3Endpoint["S3Endpoint<br>VPC Endpoint"]
    EdgeSecurityGroup["EdgeSecurityGroup<br>Security Group"]
    AppSecurityGroup["AppSecurityGroup<br>Security Group"]
    DataSecurityGroup["DataSecurityGroup<br>Security Group"]
    EdgeLoadBalancer["EdgeLoadBalancer<br>Load Balancer"]
    AppTargetGroup["AppTargetGroup<br>Target Group"]
    AppAutoScalingGroup["AppAutoScalingGroup<br>Application"]
    DbPrimary["DbPrimary<br>Database"]
    DbReadReplica["DbReadReplica<br>Database"]
    AppRouteTable --> EgressOnlyIgw
    AppRouteTable --> NatGateway
    AppRouteTable --> S3Endpoint
    AppSecurityGroup --> AppAutoScalingGroup
    AppSecurityGroup --> DataSecurityGroup
    AppTargetGroup --> AppAutoScalingGroup
    DataRouteTable --> S3Endpoint
    DataSecurityGroup --> DbPrimary
    DbPrimary --> DbReadReplica
    EdgeLoadBalancer --> AppTargetGroup
    EdgeSecurityGroup --> AppSecurityGroup
    EdgeSecurityGroup --> EdgeLoadBalancer
    PublicRouteTable --> InternetGateway
    Internet --> InternetGateway
    Internet --> EgressOnlyIgw
    Internet --> EdgeLoadBalancer
```

52 resources in the template.
