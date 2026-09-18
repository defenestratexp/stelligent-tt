# Blog notes: Topic 21, DNS and Edge

## Working title

Serve a private S3 bucket to the world: Route 53, CloudFront with Origin
Access Control, and AWS WAF, most of it without owning a domain

## Hook

Old tutorials put a website in S3 by making the bucket public and turning
on static website hosting. In 2026 that fails out of the box: Block Public
Access is on for every new bucket, and website endpoints are HTTP only
anyway. The current pattern keeps the bucket private, puts CloudFront in
front with Origin Access Control so only your distribution can read it,
filters traffic with AWS WAF at the edge, and uses Route 53 to point names
at it and fail over when a health check breaks. The surprising part for a
learner: almost all of it can be practised without buying a domain, thanks
to private hosted zones, the default `cloudfront.net` name, and Route 53's
DNS test API.

## Key points

1. **Delegation is everything in DNS.** A public hosted zone answers the
   internet only after its parent delegates to it. A private zone answers
   only inside associated VPCs, via the VPC Resolver at VPC base + 2. Use
   `.internal` (reserved by ICANN in 2024) for private names.
2. **Alias records are Route 53's escape hatch.** They work at the zone
   apex where a `CNAME` can't, take their TTL from the target, and are free
   to query for AWS targets. You can't alias to CloudFront from a private
   zone.
3. **OAC, not OAI, and not a website endpoint.** Bucket fully private,
   `BucketOwnerEnforced`, a bucket policy for `cloudfront.amazonaws.com`
   conditioned on `AWS:SourceArn`. Direct S3 requests return `403`; the
   distribution returns `200`.
4. **Routing policies can be tested without traffic.** `test-dns-answer`
   with `--edns0-client-subnet-ip` and addresses from AWS's own
   `ip-ranges.json` shows latency and geolocation answers from "Europe" or
   "Australia" while you sit at your desk.
5. **A health check you can break.** Point it at `/health.html` behind a
   `CachingDisabled` behavior, delete the object, and watch failover. A
   cached health path, or an `HTTP` check that sees a `301` redirect, will
   report healthy forever.
6. **WAF for CloudFront lives in `us-east-1`.** Scope `CLOUDFRONT`,
   attached through the distribution's `WebACLId`. Start managed rule
   groups in Count, read the logs (`aws-waf-logs-` prefix), then block.
   Add a rate-based rule with a custom `429`.

## Gotchas readers will hit

- Three things must be in `us-east-1` even though the lab lives in
  `us-east-2`: the ACM certificate for CloudFront, the WAF web ACL (and its
  log group), and CloudWatch alarms on Route 53 health check metrics.
  Public DNS query logs too. One CloudFormation stack can't span them.
- Hosted zone charges aren't prorated: $0.50 for any month a zone exists
  past its first 12 hours.
- Domain registrations are non-refundable and auto-renew by default.
- `test-dns-answer` doesn't work on private zones; you need something
  inside the VPC (the module's helper instance with Session Manager).
- S3 returns `403`, not `404`, for missing objects when CloudFront has no
  `s3:ListBucket`; map it with a custom error response rather than
  granting list access.
- `CachingOptimized` has a 24-hour default TTL and a 1-second minimum that
  overrides `no-cache` from the origin. Use invalidations or hashed file
  names.
- An alias record to CloudFront needs a matching alternate domain name on
  the distribution, can't use `EvaluateTargetHealth`, and can't be the
  target of both primary and secondary failover records.
- Route 53 treats `3xx` as healthy, and HTTPS health checks don't validate
  certificates.
- Flat-rate CloudFront plans (including the $0 Free plan) are tempting for
  a lab, but a distribution on a plan can't be deleted until the plan is
  cancelled, the web ACL can't be detached, and Free Tier accounts aren't
  eligible.
- Deleting a distribution means disabling it first and waiting for
  propagation; cleanup takes a quarter of an hour or more.
- Deleting a zone while a parent still delegates to it leaves a dangling
  `NS` record, a subdomain-takeover risk.

## Exam objectives supported

- SAA-C03 Domain 1 (Task 1.2: WAF, Shield), Domain 2 (Task 2.2: Route 53
  failover), Domain 3 (Task 3.4: CloudFront, Route 53 routing)
- SOA-C03 Domain 5: Networking and Content Delivery (Tasks 5.2 and 5.3:
  routing policies, query logging, CloudFront caching issues, WAF and
  CloudFront logs)
- SCS-C03 Domain 3: Infrastructure Security (Task 3.1: edge security
  controls, rate limiting, OWASP Top 10 protections)
- CLF-C02 Domain 3: global infrastructure and content delivery

## Material to capture while doing the labs

- `curl -I` of the S3 REST URL (`403`) next to the CloudFront URL (`200`).
- The `x-cache: Miss from cloudfront` → `Hit from cloudfront` sequence,
  and the stale page before an invalidation.
- A 50-call `test-dns-answer` tally for the 80/20 weighted records.
- Timeline of the failover test: object deleted, checkers unhealthy,
  answer switched, alarm fired, recovery.
- A WAF log record for a counted XSS request and the same request blocked.
- A diagram: viewer → Route 53 → CloudFront edge (WAF, Shield) → OAC →
  private S3 bucket, with the `us-east-1` pieces marked.
