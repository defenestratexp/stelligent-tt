# Blog Notes: Module 15, Kubernetes on EKS

## Working title

EKS in 2026: what a 2022 tutorial gets wrong, from `--generator` to
`aws-auth`

## Hook

The 2022 version of this module failed on its first Pod: `kubectl run
--generator=run-pod/v1` has been an unknown flag for years. The rest aged
the same way. Its cluster ran four always-on node group instances, relied on an
`aws-auth` ConfigMap that access entries have replaced, and deployed a
React app on Node.js 12. It also quietly defaulted to a Kubernetes version
that would have moved to extended support at six times the price. This
post rebuilds the same labs on an EKS Auto Mode cluster: pinned to a
standard-support version, access managed with access entries, AWS
credentials for Pods through Pod Identity, and a cleanup that finds what
the cluster left behind.

## Key points

1. **kubectl changed under old tutorials.** `kubectl run` only makes Pods,
   `--dry-run` needs `=client` or `=server`, and `--record` gave way to the
   `kubernetes.io/change-cause` annotation plus `kubectl rollout
   history`/`undo`. Show the before and after commands side by side.
1. **Version and support policy are cost settings.** Standard support is
   14 months at $0.10 an hour; extended support is 12 more months at $0.60.
   New clusters default to the `EXTENDED` upgrade policy, and eksctl picks
   its own default version if you don't pin one. Pin the version and set
   `upgradePolicy.supportType: STANDARD`.
1. **Auto Mode moves the node question.** No node groups, no add-ons to
   upgrade, zero nodes until a Pod is pending. You pay a per-instance
   management fee, lose SSH and custom AMIs, and steer instance choice with
   resource requests and NodePools. A NodePool limit is not a cluster-wide
   cost cap while the built-in `general-purpose` pool is enabled.
1. **Two identity systems, both outside the cluster.** Access entries (with
   namespace-scoped access policies) replace `aws-auth` for humans; Pod
   Identity replaces IRSA's per-cluster OIDC trust for workloads, with
   session tags you can use in trust and resource policies.
1. **Load balancers are the cleanup trap.** A `LoadBalancer` Service makes
   an NLB, security groups and ENIs that CloudFormation doesn't own. Delete
   Services and Ingresses first, then the cluster, then check, including
   resources EC2 now hides by default.

## Gotchas readers will hit

- The Auto Mode NLB is **internal** unless the Service has
  `service.beta.kubernetes.io/aws-load-balancer-scheme: internet-facing`;
  the external hostname appears and then never answers.
- Since April 2026, instances, volumes and ENIs created by Auto Mode are
  hidden from the EC2 console and `describe-*` in accounts that had no
  managed instances before. They are still billed. Use
  `--include-managed-resources` or change the account's managed resource
  visibility setting.
- The built-in `general-purpose` NodePool is amd64 only, so an image built
  on an Apple silicon Mac without `--platform linux/amd64` crashes with
  `exec format error`.
- `runAsNonRoot: true` fails with a non-numeric `USER` in the Dockerfile
  (`USER node`); the kubelet can't verify a name. Use `USER 1000:1000`.
- Auto Mode enforces IMDSv2 with a hop limit of 1, so Pods can't fall back
  to the node role. A Pod without a Pod Identity association has no AWS
  credentials at all, which is the point but surprises people.
- Pod Identity credentials are injected when a Pod is created; Pods that
  were running before the association need to be restarted.
- Nodes pull public images through one NAT gateway address, so anonymous
  Docker Hub pulls (100 per six hours per address) run out quickly. Use
  the ECR Public Gallery copies of official images.
- `kubectl scale` then `kubectl apply` of an unchanged file silently puts
  the old replica count back.

<!-- VERIFY: capture the exact kubelet error text for runAsNonRoot with a
named USER, and the Auto Mode NLB behavior without the scheme annotation,
while doing Labs 15.6.1 and 15.6.2. -->

## Exam objectives

- DOP-C02 Domain 1 (Task 1.3 artifacts in ECR; Task 1.4 deployment
  strategies for container environments, rollback, troubleshooting)
- DOP-C02 Domain 3 (Task 3.2 deploying container-based applications on
  EKS) and Domain 6 (Task 6.1 IAM for human and machine identities, ABAC)
- SAP-C02 → C03 Domain 2 (Tasks 2.1 deployment strategy, 2.3 security
  controls, 2.6 cost optimization) and Domain 4 (Task 4.4 modernization)
