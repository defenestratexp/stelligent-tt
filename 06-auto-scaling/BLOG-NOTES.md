# Blog Notes: Module 06, Auto Scaling

## Working title

Launch configurations are gone: updating Auto Scaling groups with launch
templates in 2026

## Hook

The classic Auto Scaling tutorial starts with a launch configuration, or with
`create-auto-scaling-group --instance-id`, which quietly creates one for you.
In an AWS account opened after October 1, 2024, neither works: launch
configurations can't be created by any method, console, CLI or
CloudFormation. The replacement, the launch template, is versioned, and that
changes how you roll a change out to a group. This post starts from the
failing command, rebuilds the group on a launch template with Amazon Linux
2023, and then compares the ways to get a new template version onto running
instances, including the Instance Refresh update policy CloudFormation now
supports.

## Key points

1. **The dates.** No new instance types in launch configurations since
   2023-01-01; no console creation for accounts made after 2023-06-01; no
   creation at all for accounts made after 2024-10-01. "Create ASG from
   instance" is a launch configuration in disguise; the replacement is
   `get-launch-template-data` then `create-launch-template`.
1. **Versions are the point.** A template change creates a new version, not a
   new resource. Reference `LatestVersionNumber` in CloudFormation, not
   `$Latest`, or the stack update never touches the group. Existing
   instances keep running the old version until something replaces them.
1. **Four ways to roll out a version:** let instances age out,
   `AutoScalingReplacingUpdate` (new group), `AutoScalingRollingUpdate`
   (terminate-then-launch, `cfn-signal` driven), and Instance Refresh, by
   hand or through the `AutoScalingInstanceRefresh` update policy
   (launch-before-terminate via the instance maintenance policy, checkpoints,
   skip matching, alarm-based rollback). Table of which honours what.
1. **`cfn-signal` on AL2023, done right.** Install `aws-cfn-bootstrap` with
   `dnf`, signal the ASG's logical ID, send a failure signal on error, and
   match the `CreationPolicy` count to desired capacity. Then note that
   Instance Refresh ignores signals: readiness comes from health checks and
   lifecycle hooks.
1. **What launch templates unlock:** mixed instances groups with Spot
   (`price-capacity-optimized`, capacity rebalancing, attribute-based
   selection) and warm pools. Neither was available with launch
   configurations. Warm pools and Spot don't mix.

## Gotchas readers will hit

- `$Latest` in a CloudFormation `LaunchTemplate` property hides template
  changes from the stack update; the group keeps old instances.
- Changing t3 to t4g without switching the AMI parameter to `-arm64` fails;
  one launch template can't serve both architectures without per-override
  templates.
- `AutoScalingRollingUpdate` doesn't honour the instance maintenance policy
  and can drop capacity; `AutoScalingInstanceRefresh` can't be combined with
  it on the same group.
- Change the `UpdatePolicy` in its own stack update: a rollback uses the old
  policy.
- A `CreationPolicy` only applies at create time; you have to recreate the
  stack to test it.
- Warm pool instances are stopped as soon as they launch, mid user data, and
  user data doesn't run again on the warm start. Use a lifecycle hook (and
  think about who completes it the second time).
- A 1-minute alarm period without detailed monitoring sees no data most of
  the time; launch templates default to basic monitoring, launch
  configurations defaulted to detailed.
- Stressing a t3/t4g to trigger scaling spends CPU credits; long runs in
  unlimited mode cost extra.
- Terminating a group's instances by hand just makes it launch new ones.
  Delete the group.

<!-- VERIFY: capture the exact create-auto-scaling-group --instance-id error in a post-2024-10-01 account while doing Lab 6.1.1. -->

## Exam objectives

- SAA-C03 Domain 2 (2.1 scalable architectures, 2.2 highly available
  architectures), Domain 3 (3.2 high-performing and elastic compute) and
  Domain 4 (4.2 cost-optimized compute: Spot, scaling strategies)
- SOA-C03 Domain 2: Reliability and Business Continuity (2.1 scalability and
  elasticity); Domain 3: Deployment, Provisioning, and Automation (3.1
  CloudFormation and deployment strategies)
