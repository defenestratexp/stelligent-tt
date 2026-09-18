# Topic 21: DNS and Edge

<!-- TOC -->

- [Topic 21: DNS and Edge](#topic-21-dns-and-edge)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Guidance](#guidance)
  - [Conventions](#conventions)
  - [Lesson 21.1: Hosted zones and records](#lesson-211-hosted-zones-and-records)
    - [Principle 21.1](#principle-211)
    - [Practice 21.1](#practice-211)
      - [Lab 21.1.1: A private hosted zone](#lab-2111-a-private-hosted-zone)
      - [Lab 21.1.2: Alias records and the zone apex](#lab-2112-alias-records-and-the-zone-apex)
      - [Lab 21.1.3: A public hosted zone](#lab-2113-a-public-hosted-zone)
      - [Lab 21.1.4: Resolver query logging](#lab-2114-resolver-query-logging)
    - [Retrospective 21.1](#retrospective-211)
  - [Lesson 21.2: CloudFront in front of a private bucket](#lesson-212-cloudfront-in-front-of-a-private-bucket)
    - [Principle 21.2](#principle-212)
    - [Practice 21.2](#practice-212)
      - [Lab 21.2.1: The origin bucket](#lab-2121-the-origin-bucket)
      - [Lab 21.2.2: A distribution with Origin Access Control](#lab-2122-a-distribution-with-origin-access-control)
      - [Lab 21.2.3: Caching and invalidation](#lab-2123-caching-and-invalidation)
      - [Lab 21.2.4: Error pages and security headers](#lab-2124-error-pages-and-security-headers)
      - [Lab 21.2.5: A custom domain (real domain only)](#lab-2125-a-custom-domain-real-domain-only)
    - [Retrospective 21.2](#retrospective-212)
  - [Lesson 21.3: Routing policies and health checks](#lesson-213-routing-policies-and-health-checks)
    - [Principle 21.3](#principle-213)
    - [Practice 21.3](#practice-213)
      - [Lab 21.3.1: Weighted routing](#lab-2131-weighted-routing)
      - [Lab 21.3.2: Latency and geolocation routing](#lab-2132-latency-and-geolocation-routing)
      - [Lab 21.3.3: A health check you can break](#lab-2133-a-health-check-you-can-break)
      - [Lab 21.3.4: Failover routing](#lab-2134-failover-routing)
      - [Lab 21.3.5: Calculated health checks (optional)](#lab-2135-calculated-health-checks-optional)
    - [Retrospective 21.3](#retrospective-213)
  - [Lesson 21.4: AWS WAF at the edge](#lesson-214-aws-waf-at-the-edge)
    - [Principle 21.4](#principle-214)
    - [Practice 21.4](#practice-214)
      - [Lab 21.4.1: A web ACL in us-east-1](#lab-2141-a-web-acl-in-us-east-1)
      - [Lab 21.4.2: Count, log, then block](#lab-2142-count-log-then-block)
      - [Lab 21.4.3: Rules you write](#lab-2143-rules-you-write)
      - [Lab 21.4.4: Clean up the module](#lab-2144-clean-up-the-module)
    - [Retrospective 21.4](#retrospective-214)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- **New module.** The 2022 course never taught DNS or content delivery. It
  mentioned CloudFront only in passing, and Route 53 and AWS WAF not at
  all. Module 02 now stops at "keep the bucket private" and points here for
  the way public content is served today: CloudFront in front of a private
  bucket with Origin Access Control (OAC).
- Route 53 routing policies, health checks and DNS failover are core
  SAA-C03 material, and "Networking and Content Delivery" is a whole domain
  (18%) of the CloudOps exam (SOA-C03). Edge protection with AWS WAF is a
  task statement in SCS-C03.
- OAC replaces origin access identity (OAI), which AWS now labels legacy.
  OAC works with SSE-KMS, with every Region and with `PUT`/`DELETE`.
- AWS WAF labs use the current (v2) API. The WAF console now calls a web ACL
  a *protection pack (web ACL)*; the API, CLI and CloudFormation still say
  web ACL.
- Two newer pricing facts the labs work around: CloudFront **flat-rate
  pricing plans** (November 2025, including a $0 Free plan) and the
  renaming of Route 53 Resolver to **Route 53 VPC Resolver** when Route 53
  Global Resolver was introduced.
- **No domain required** for most of the module. Private hosted zones,
  the CloudFront default `*.cloudfront.net` domain, Route 53's DNS test
  API and WAF all work without one. Only Lab 21.2.5 (custom domain and ACM
  certificate) and real-world delegation need a domain you own.

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| CLF-C02 | Domain 3: Cloud Technology and Services (global infrastructure, network and content delivery services) |
| SAA-C03 | Domain 1: Design Secure Architectures (Task 1.2: secure workloads and applications, including AWS WAF and Shield) |
| SAA-C03 | Domain 2: Design Resilient Architectures (Task 2.2: highly available and fault-tolerant architectures, Route 53 failover) |
| SAA-C03 | Domain 3: Design High-Performing Architectures (Task 3.4: high-performing network architectures, CloudFront and Route 53) |
| SOA-C03 | Domain 5: Networking and Content Delivery (Task 5.2: domains, DNS and content delivery; Task 5.3: CloudFront caching issues, WAF and CloudFront logs) |
| SOA-C03 | Domain 2: Reliability and Business Continuity (health checks and failover) |
| SCS-C03 | Domain 3: Infrastructure Security (Task 3.1: security controls for network edge services) |

## Cost and cleanup

- **Hosted zones:** $0.50 per hosted zone per month. The charge is **not
  prorated**: a zone that exists past 12 hours costs the full $0.50 for
  that month. A zone deleted within 12 hours of creation isn't charged.
  This module creates two zones (one private, one public), so about $1.
- **DNS queries:** $0.40 per million for standard queries, which in these
  labs rounds to zero. Queries for alias records that point at AWS
  resources such as CloudFront are free.
- **Health checks:** $0.50 per month for an AWS endpoint, $0.75 for a
  non-AWS endpoint, plus $1 or $2 per month for each optional feature
  (HTTPS, string matching, fast interval, latency measurement). Health
  check charges are prorated. Route 53 currently lets any customer run up
  to 50 health checks for AWS endpoints in the same account at no charge.
  <!-- VERIFY: whether the no-charge offer covers optional features, and
  whether a CloudFront distribution in the same account counts as an "AWS
  endpoint" for pricing. -->
- **Domain registration is optional and not refundable.** If you register
  a domain for Lab 21.2.5, you pay for a full year up front, and deleting
  the registration early doesn't refund it. Prices depend on the
  top-level domain. Registering also creates a public hosted zone ($0.50
  per month) for you.
- **CloudFront** (pay-as-you-go) has an always-free allowance of 1 TB of
  data transfer out, 10 million requests and 2 million CloudFront Function
  invocations a month. The first 1,000 invalidation paths a month are
  free. Origin fetches from S3 are free. A lab distribution costs nothing
  in practice.
- **CloudFront flat-rate plans** are *not* used in the labs. A distribution
  on a plan can't be deleted until the plan is cancelled, and a paid plan
  keeps billing until the end of the billing cycle. See the Retrospective
  of Lesson 21.4.
- **AWS WAF:** $5.00 per web ACL per month plus $1.00 per rule or rule
  group per month, prorated hourly, plus $0.60 per million requests. A web
  ACL with four rules left up for a day costs about $0.30. Bot Control,
  Fraud Control and CAPTCHA cost extra; the labs don't use them.
- **Small charges:** the test instance in Lesson 21.1 (a `t4g.nano` and its
  public IPv4 address, about a cent an hour together), CloudWatch Logs
  ingestion for query logs and WAF logs (pennies), and a CloudWatch alarm
  ($0.10 per month, prorated).
- **Slow to delete:** a CloudFront distribution must be disabled before it
  can be deleted, and each change takes minutes to reach every edge
  location. Plan 15–30 minutes for cleanup.
- **Cleanup:** Lab 21.1.1 ends by deleting the test instance.
  [Lab 21.4.4](#lab-2144-clean-up-the-module) removes everything else,
  in both `us-east-2` and `us-east-1`.

## Guidance

- Explore the official docs! See the
  [Route 53 Developer Guide](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html),
  [CloudFront Developer Guide](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html)
  and
  [AWS WAF Developer Guide](https://docs.aws.amazon.com/waf/latest/developerguide/what-is-aws-waf.html),
  the CLI references for
  [route53](https://docs.aws.amazon.com/cli/latest/reference/route53/index.html),
  [cloudfront](https://docs.aws.amazon.com/cli/latest/reference/cloudfront/index.html)
  and
  [wafv2](https://docs.aws.amazon.com/cli/latest/reference/wafv2/index.html),
  and the CloudFormation reference for
  [AWS::Route53::RecordSet](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-route53-recordset.html),
  [AWS::CloudFront::Distribution](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-cloudfront-distribution.html)
  and
  [AWS::WAFv2::WebACL](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-wafv2-webacl.html).

- Avoid using other sites like stackoverflow.com for answers \-- part
  of the skill set you're building is finding answers straight from
  the source, AWS. Many CloudFront tutorials still use OAI, S3 website
  endpoints and the legacy `ForwardedValues` cache settings. Don't copy
  them.

- Explore your curiosity. Try to understand why things work the way
  they do. Read more of the documentation than just what you need to
  find the answers.

- You'll want `dig` (from `bind-utils` or `dnsutils`) and `curl` on your
  workstation. Both are in most Linux distributions and in macOS.

## Conventions

- **Profile and Region.** Use the `lab` profile from module 19. Its Region,
  `us-east-2`, is where the buckets, stacks and test instance live.
- **Global and `us-east-1` services.** This module has more of them than any
  other, so each lab says which applies:
  - Route 53 and CloudFront are **global**. Their APIs work from your
    `us-east-2` profile without `--region`.
  - An **ACM certificate for CloudFront** must be requested in `us-east-1`.
  - A **WAF web ACL for CloudFront** has scope `CLOUDFRONT` and must be
    created and managed in `us-east-1`, from the CLI with
    `--scope CLOUDFRONT --region us-east-1`.
  - **Route 53 health check metrics** are only in CloudWatch in
    `us-east-1`, so alarms on them live there too.
  - **Public DNS query logs** go to a log group in `us-east-1`.

  Labs that are about these Regions pass `--region` explicitly. The region
  guardrail SCP from module 19 allows both `us-east-2` and `us-east-1`, so
  nothing here should be denied by it.
- **Names.** `<you>` is your identifier. The private zone is
  `<you>.lab.internal`. The public zone is called `<zone>` below: either
  `lab.<your-domain>` if you own a domain, or `<you>.example.com` if you
  don't (see Lab 21.1.3).
- **Addresses.** Where a record needs an IP address that nobody will
  connect to, use the documentation ranges `192.0.2.0/24`,
  `198.51.100.0/24` and `203.0.113.0/24`. Don't point records at addresses
  you don't control.
- **Templates.** CloudFormation in YAML for zones, records, health checks,
  the distribution and the web ACL; the CLI for inspecting, testing and
  one-off changes. Keep templates in this directory. Two files are
  provided:
  - [dns-test-instance.yaml](dns-test-instance.yaml) is a complete helper
    (not the subject of any lab) that gives you a machine inside the VPC.
  - [edge-site-starter.yaml](edge-site-starter.yaml) is a starter with the
    origin bucket and `TODO(student)` markers for everything you add.

## Lesson 21.1: Hosted zones and records

### Principle 21.1

*A hosted zone answers authoritatively only for names that are delegated to
it. A public zone answers the internet once its parent points at it; a
private zone answers only inside the VPCs you associate with it.*

### Practice 21.1

DNS is a distributed database with caching. A *hosted zone* is Route 53's
container for the records of one domain (`example.com`) or subdomain
(`lab.example.com`). Whether anyone ever asks that zone a question depends
on delegation: the parent zone must have `NS` records that name the zone's
name servers. A *private* hosted zone skips delegation entirely. The
Route 53 VPC Resolver (the Amazon-provided DNS server at the VPC's base
address plus two) consults it for queries from associated VPCs.

These labs create one zone of each kind, show you the difference between a
`CNAME` and an *alias* record, and turn on query logging so you can watch
queries arrive. Read
[How DNS routes traffic](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/welcome-dns-service.html)
and
[Supported DNS record types](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/ResourceRecordTypes.html)
first.

#### Lab 21.1.1: A private hosted zone

- Read [Working with private hosted
  zones](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-private.html)
  and [Considerations when working with a private hosted
  zone](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zone-private-considerations.html).

- Check that the default VPC in `us-east-2` has both DNS attributes the
  docs require. Use `aws ec2 describe-vpc-attribute` once for each.

- Deploy [dns-test-instance.yaml](dns-test-instance.yaml) into the default
  VPC. Connect with `aws ssm start-session` (module 05 set up the Session
  Manager plugin). Keep the session open; you'll use it in the next labs.

- Write a template, `zones.yaml`, that creates a private hosted zone named
  `<you>.lab.internal` associated with the default VPC. Output its ID.

- Write a second template, `private-records.yaml`, that takes the zone ID
  as a parameter and creates:
  - `app.<you>.lab.internal`, an `A` record with the test instance's
    private IP (pass it in as a parameter);
  - `www.<you>.lab.internal`, a `CNAME` to `app.<you>.lab.internal`;
  - a `TXT` record at `info.<you>.lab.internal` with any text you like.

- From the instance, resolve each name with `dig`. Look at the `SERVER`
  line: which address answered? From your workstation, resolve the same
  names.

- Delete the test instance's stack **at the end of this lesson**, after
  Lab 21.1.4.

##### Question: Why .internal

_In 2024 ICANN reserved the top-level domain `.internal` for private use,
the DNS equivalent of `10.0.0.0/8`. Why is it a better choice for a
private zone than a made-up name like `corp.lab`, or than a subdomain of a
real domain you don't control?_

##### Question: Who answered

_Which IP address answered the instance's queries, and how does it relate
to the VPC's CIDR block? What did your workstation get for the same names,
and which server told it so?_

##### Question: Overlapping names

_If you created a private zone named `example.com` in this VPC, what would
the instance get when it looked up `www.example.com`, the real public
website? Read the "overlapping namespaces" section and explain why. How
could that break something in a real VPC?_

#### Lab 21.1.2: Alias records and the zone apex

An *alias* record is a Route 53 extension to DNS. It looks like an `A` or
`AAAA` record to the client, but Route 53 fills in the answer from an AWS
resource or from another record in the same zone. Read [Choosing between
alias and non-alias
records](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-choosing-alias-non-alias.html).

- In `private-records.yaml`, add an `A` alias record at the **zone apex**
  (`<you>.lab.internal` itself) that points at `app.<you>.lab.internal`.
  Resolve it from the instance.

- Now try to create a `CNAME` at the apex instead, with
  `aws route53 change-resource-record-sets` and a small JSON change batch.
  Save the exact error.

- Compare the TTLs `dig` shows for `www` (your `CNAME`) and for the apex
  alias. Where does the alias record's TTL come from?

##### Question: Apex CNAME

_Why doesn't DNS allow a `CNAME` at the zone apex? Which records must
always exist at the apex? How does an alias record get around the rule?_

##### Question: Alias or CNAME

_Name two things an alias record can do that a `CNAME` can't, and one
thing a `CNAME` can do that an alias record can't._

#### Lab 21.1.3: A public hosted zone

Every public zone gets four name servers and an `SOA` record. Nobody on
the internet asks those name servers anything until the parent zone
delegates to them.

- Decide your `<zone>`:
  - **You own a domain** (at Route 53 or any registrar): use a subdomain
    such as `lab.<your-domain>`, so nothing you do here can break the
    domain's real records.
  - **You don't:** use `<you>.example.com`. `example.com` is reserved for
    documentation and will never be delegated to you, so this zone is
    reachable only by asking its name servers directly or through the
    Route 53 test API. That is enough for every lab except 21.2.5.
    <!-- VERIFY: that Route 53 accepts CreateHostedZone for a subdomain of
    example.com, and that Route 53 name servers answer direct queries for a
    zone that hasn't been delegated. -->

- Add the public zone to `zones.yaml` and output its ID and name servers
  (the `NameServers` attribute).

- Add a `TXT` record at `hello.<zone>`. Query it three ways and compare:
  - `dig @<one-of-your-name-servers> hello.<zone> TXT`
  - `aws route53 test-dns-answer`
    ([docs](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-test.html))
  - plain `dig hello.<zone> TXT` through your normal resolver

- **Real domain only:** delegate the subdomain. In the parent zone (where
  the domain's DNS is hosted), add an `NS` record for `lab.<your-domain>`
  with your zone's four name servers. Read [Routing traffic for
  subdomains](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-routing-traffic-for-subdomains.html).
  Repeat the plain `dig`, then run `dig +trace hello.<zone> TXT` and read
  the delegation chain from the root down.

##### Question: Delegation

_Before delegation, plain `dig` returned nothing useful for your zone.
Why? After delegation (if you did it), how long could an old negative
answer stay cached, and which record in which zone controls that?_

##### Question: The test API

_`test-dns-answer` doesn't work for private hosted zones. Read its API
reference and explain why that follows from how private zones work. Which
Region's resolver does it pretend to be if you don't pass `--resolver-ip`?_

#### Lab 21.1.4: Resolver query logging

Route 53 can log DNS queries in two places: *public DNS query logging* for
queries that reach a public zone's name servers (log group in
`us-east-1`), and *VPC Resolver query logging* for queries that resources
in a VPC send to the VPC Resolver. The second works without a domain.

- Read [Resolver query
  logging](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver-query-logs.html).

- Create a CloudWatch Logs log group in `us-east-2` named with your
  identifier, with a one-day retention.

- Create a Resolver query logging configuration that sends to it
  (`aws route53resolver create-resolver-query-log-config`) and associate
  it with the default VPC.

- From the test instance, look up your private names, a public name such
  as `aws.amazon.com`, and a name that doesn't exist. Then read the log
  with `aws logs tail`.

- Disassociate and delete the query logging configuration, then delete the
  test instance's stack. Keep the log group until Lab 21.4.4 if you want
  to look at it again; it has a one-day retention.

##### Question: What the log shows

_Find the entry for the name that doesn't exist. What `rcode` did it get?
Which fields would let you find the instance that made a query in a VPC
with hundreds of instances?_

##### Question: Two kinds of query log

_Which of the two logging features would show you queries from the
internet for `hello.<zone>`, and which would show a Lambda function in a
VPC looking up a partner's API? Why does one of them need a log group in
`us-east-1`?_

### Retrospective 21.1

#### Question: Split-view DNS

_Read "Split-view DNS" in the private zone considerations. Design
`app.example.com` so that the internet reaches a CloudFront distribution
and instances in your VPC reach a private load balancer. Which zones and
records do you need, and what goes wrong if the private zone lacks a
record the public zone has?_

#### Question: Hybrid DNS

_Read [What is Route 53 VPC
Resolver?](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver.html)
Your company's data center hosts `corp.example.com`, and on-premises
servers need to resolve your private zone. Which endpoint (inbound or
outbound) and which kind of rule solves each direction? Each endpoint
needs at least two IP addresses and costs $0.125 per address per hour.
What does the smallest possible setup for both directions cost per
month?_

#### Task: DNSSEC, on paper

_Read [Configuring DNSSEC signing in Amazon Route
53](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-configuring-dnssec.html).
Don't turn it on. Explain what a KSK is, why Route 53 requires the KMS key
behind it to be in `us-east-1`, and what you'd have to remove, and in what
order, before you could safely delete a signed zone._

## Lesson 21.2: CloudFront in front of a private bucket

### Principle 21.2

*Keep the bucket private and make CloudFront its only reader. The edge is
the one public door, so caching, TLS, headers and filtering all happen
there.*

### Practice 21.2

In module 02 you found that public buckets are blocked by default and that
S3 website endpoints are HTTP only. CloudFront solves both. Viewers connect
to one of hundreds of edge locations over HTTPS. The edge serves cached
copies when it can and fetches from the origin when it can't. With
[Origin Access
Control](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html),
CloudFront signs every origin request with SigV4 as the
`cloudfront.amazonaws.com` service principal, and the bucket policy allows
that principal only on behalf of your distribution.

All of this works on the distribution's default domain name,
`d111111abcdef8.cloudfront.net`, which already has a valid certificate. A
custom domain (Lab 21.2.5) needs a domain you own.

Distributions are created and changed through CloudFormation in
`us-east-2` (the stack's Region; the distribution itself is global). Every
change takes a few minutes to deploy to the edge. Read [Get started with a
CloudFront standard
distribution](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/GettingStarted.SimpleDistribution.html)
before you start, and skim [All distribution settings
reference](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/distribution-web-values-specify.html).

#### Lab 21.2.1: The origin bucket

- Copy [edge-site-starter.yaml](edge-site-starter.yaml) to `edge-site.yaml`
  and deploy it. It creates the bucket with every Block Public Access
  setting on and ACLs disabled, which is what OAC expects.

- Make a small local site directory with `index.html`, `404.html`,
  `health.html` (a one-line page that says `OK`) and a `css/` or `img/`
  file or two. Upload it with `aws s3 sync`.

- Try to fetch `index.html` straight from the bucket's REST endpoint with
  `curl -I`. Keep the output for the next lab.

##### Question: Which endpoint

_The template outputs the bucket's **regional domain name**
(`<bucket>.s3.us-east-2.amazonaws.com`). Why must a CloudFront origin that
uses OAC be this endpoint and not the S3 static website endpoint? What
would you lose, and what would you have to make public, with a website
endpoint?_

#### Lab 21.2.2: A distribution with Origin Access Control

Fill in the first three `TODO(student)` blocks in `edge-site.yaml`:

- An `AWS::CloudFront::OriginAccessControl` for S3 that always signs
  requests with SigV4.

- An `AWS::CloudFront::Distribution` with:
  - one origin, your bucket's regional domain name, with the OAC attached
    (see the S3 origin section of the
    [distribution reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-properties-cloudfront-distribution-origin.html));
  - a default cache behavior that redirects HTTP to HTTPS, allows only
    `GET` and `HEAD`, and uses the managed `CachingOptimized` cache policy
    by ID (from [Use managed cache
    policies](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/using-managed-cache-policies.html));
  - `index.html` as the default root object;
  - HTTP/2 and HTTP/3, IPv6 on, and the cheapest price class.

- An `AWS::S3::BucketPolicy` that allows `s3:GetObject` to the CloudFront
  service principal with a condition on `AWS:SourceArn` equal to your
  distribution's ARN. Build the ARN with `!Sub` and pseudo-parameters; don't
  hard-code your account ID.

- Output the distribution ID and domain name. Deploy, and wait for the
  distribution's status to reach `Deployed`
  (`aws cloudfront wait distribution-deployed`).

- Test:
  - Positive: `curl -I https://<distribution-domain>/` returns `200`.
  - Positive: `curl -I http://<distribution-domain>/` redirects.
  - Negative: the direct S3 request from Lab 21.2.1 still returns `403`.

<!-- VERIFY: that a distribution created with the CLI or CloudFormation is
pay-as-you-go by default, and whether the 2026 console's create flow
defaults to a flat-rate plan. -->

##### Question: Chicken and egg

_The bucket policy needs the distribution's ARN, and the distribution needs
the bucket. Why doesn't that create a circular dependency in your
template? Which resource would you have to change to create one?_

##### Question: Why not OAI

_Your bucket uses SSE-S3. If module 02's customer managed KMS key encrypted
it instead, what else would CloudFront need, and where would you grant it?
Why couldn't the legacy origin access identity do this at all?_

#### Lab 21.2.3: Caching and invalidation

- Request `index.html` several times with `curl -sI`. Watch the `x-cache`,
  `age` and `x-amz-cf-pop` response headers.

- Change `index.html` locally, sync it, and request it again. What do you
  get, and for how long would you keep getting it with `CachingOptimized`'s
  default TTL?

- Create an invalidation for `/index.html` and wait for it to complete.
  Request the page again.

- Add a second cache behavior to the distribution for the path pattern
  `/health*` that uses the managed `CachingDisabled` policy. Lesson 21.3
  health-checks this path, and a health check that reads a cached copy
  would never notice the origin had failed.

- Read [Manage how long content stays in the
  cache](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Expiration.html).

##### Question: Invalidate or version

_Invalidations are free for the first 1,000 paths a month, then cost
$0.005 per path. A path with a wildcard counts as one. Compare invalidating
`/*` after every deploy with putting a content hash in each asset's file
name (`app.3f9c2e.css`). Which one leaves no window where some edges serve
the old file?_

##### Question: What's in the cache key

_`CachingOptimized` leaves query strings out of the cache key. What does
`curl https://<distribution-domain>/index.html?v=2` return after you change
the page but before you invalidate? When would that setting be wrong for
an application?_

#### Lab 21.2.4: Error pages and security headers

- Request a path that doesn't exist. Note the status code.

- Add a custom error response that turns that status into a `404` and
  serves `/404.html`, with a short error-caching TTL. Test again.

- Attach the managed response headers policy `SecurityHeadersPolicy` to
  the default cache behavior. Compare the response headers before and
  after. Read [Understanding response headers
  policies](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/understanding-response-headers-policies.html).

##### Question: 403 for a missing file

_Why did S3 return `403 Forbidden`, not `404 Not Found`, for an object that
doesn't exist? Read the permissions section of the S3
[GetObject](https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html)
API reference. Would you grant CloudFront `s3:ListBucket` to fix it? Why or
why not?_

##### Question: Which headers

_Name each header the security headers policy added and what browser
behavior it changes. Which one would break your site if you later loaded
scripts from another domain?_

#### Lab 21.2.5: A custom domain (real domain only)

*Skip this lab if you don't own a domain. Lab 21.3.4 has a path that works
without it.*

- Read [Use custom URLs by adding alternate domain
  names](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/CNAMEs.html)
  and [Requirements for using SSL/TLS certificates with
  CloudFront](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cnames-and-https-requirements.html).

- Request a public ACM certificate for `www.<zone>` **in `us-east-1`**,
  with DNS validation. The validation `CNAME` goes in your public zone,
  which is delegated (Lab 21.1.3). Wait for the status `ISSUED`.

  A stack in `us-east-2` can't create a certificate in `us-east-1`.
  Either request it with the CLI (`--region us-east-1`) and pass its ARN
  to `edge-site.yaml` as a parameter, or deploy a small certificate stack
  in `us-east-1`.

- Add `www.<zone>` as an alternate domain name (`Aliases`) on the
  distribution, with the certificate, SNI and the current recommended
  minimum TLS security policy.

- In the public zone, create `A` and `AAAA` **alias** records for
  `www.<zone>` that point at the distribution. The alias hosted zone ID for
  every CloudFront distribution is a fixed value; find it in the
  [AliasTarget](https://docs.aws.amazon.com/Route53/latest/APIReference/API_AliasTarget.html)
  reference.

- Test with `curl -v https://www.<zone>/` and read the certificate the
  server presents.

##### Question: Why us-east-1

_Your bucket, stack and distribution configuration live in `us-east-2`.
Why must the certificate be in `us-east-1`? Would an Application Load
Balancer origin's certificate (for the connection from CloudFront to the
origin) have the same rule?_

##### Question: Alias in a private zone

_Try (or look up) creating the same alias record in your private zone.
What happens, and why does that restriction make sense?_

### Retrospective 21.2

#### Question: Other origins

_Read [Restrict access with VPC
origins](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-vpc-origins.html).
How would you put CloudFront in front of the Application Load Balancer from
module 07 so that the load balancer has no public IP address at all? What
did people do before VPC origins, with a custom header and a security group
prefix list, and what was weak about it?_

#### Question: Private content

_OAC stops people bypassing CloudFront to reach the bucket. It doesn't stop
anyone from reading through CloudFront. If only paying customers may
download a file, what would you add? Compare [signed URLs and signed
cookies](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/PrivateContent.html)
with S3 presigned URLs from module 02._

## Lesson 21.3: Routing policies and health checks

### Principle 21.3

*Route 53 can give different answers to different askers, and it can stop
giving answers that point at something broken. Either way, clients act on
the answer only when their cached copy expires.*

### Practice 21.3

A routing policy decides which record, from a set with the same name and
type, Route 53 returns. A health check is an independent probe from
Route 53's checkers around the world; attach it to a record and Route 53
stops returning that record while the check is unhealthy.

Read [Choosing a routing
policy](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html)
first. Every lab in this lesson uses your public zone. Answers that point
at documentation addresses are fine: you're testing what Route 53 *says*,
not connecting to anything. Your tool is `aws route53 test-dns-answer`,
which can pretend to be a resolver anywhere in the world
(`--resolver-ip`) or a client in a particular subnet
(`--edns0-client-subnet-ip`). Read [How Route 53 uses EDNS0 to estimate the
location of a
user](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy-edns0.html).

Keep these records in one template, `routing.yaml`, that takes the public
zone ID as a parameter.

#### Lab 21.3.1: Weighted routing

- Create two weighted `A` records for `weighted.<zone>`, with different
  set identifiers, pointing at `192.0.2.10` (weight 80) and
  `198.51.100.10` (weight 20). Use a TTL of 60.

- Call `test-dns-answer` 50 times in a shell loop and count the answers.

- Change the second record's weight to `0` and repeat.

##### Question: Weights

_How close were your counts to 80/20? What happens if every record in the
set has weight `0`? When would you deliberately set a weight to `0`?_

##### Question: Canary

_You run the same application in two stacks and want 5% of users on the
new one. Why is weighted DNS a rough tool for that compared with weighted
target groups on an ALB listener? Think about resolvers, caches and TTLs._

#### Lab 21.3.2: Latency and geolocation routing

Latency records need an AWS Region per record, not a resource in that
Region. To simulate clients elsewhere, you need IP addresses that Route 53
places in other parts of the world. AWS publishes its own address ranges,
tagged by Region, in
[ip-ranges.json](https://docs.aws.amazon.com/vpc/latest/userguide/aws-ip-ranges.html).

- Create two latency records for `latency.<zone>`, one for `us-east-2`
  (`192.0.2.20`) and one for `eu-west-1` (`198.51.100.20`).

- Download `ip-ranges.json` and pick one address from an `eu-west-1` EC2
  prefix and one from a `us-east-2` prefix. Call `test-dns-answer` with
  each as `--edns0-client-subnet-ip`.

- Create geolocation records for `geo.<zone>`: one for the continent
  Europe, one for the United States, and **no default record**. Test with
  the same two addresses and with an address from an `ap-southeast-2`
  prefix.

- Add a default (`*`) geolocation record and test the third address again.

<!-- VERIFY: that test-dns-answer applies latency and geolocation routing
using the EDNS0 client subnet, and that addresses from ip-ranges.json
geolocate to the expected continent. -->

##### Question: Latency vs geolocation

_Both sent your European address to the European answer. Give one
requirement that only geolocation meets and one that only latency meets._

##### Question: No default

_What did the `ap-southeast-2` address get before you added the default
record: an error, or an answer with no records? Why is a missing default
record a common production outage?_

#### Lab 21.3.3: A health check you can break

The distribution from Lesson 21.2 makes a good health check target:
`/health.html` is served through the `/health*` behavior with caching
disabled, so deleting the object from the bucket makes the check fail
right away.

- Read [How Route 53 determines whether a health check is
  healthy](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-determining-health-of-endpoints.html)
  and [Values that you specify when you create or update health
  checks](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/health-checks-creating-values.html).

- Add an `AWS::Route53::HealthCheck` to `routing.yaml` that monitors the
  distribution's domain name, resource path `/health.html`, standard
  interval, failure threshold 3. Decide whether it should be `HTTP` or
  `HTTPS` (read the question below first), and tag it with your
  identifier.

- Watch it with `aws route53 get-health-check-status`. You'll see one
  entry per checker Region.

- Create a CloudWatch alarm on the check's `HealthCheckStatus` metric (see
  [Monitoring health checks using
  CloudWatch](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/monitoring-health-checks.html)).
  This is a lab about Regions: the metric only exists in `us-east-1`, so
  pass `--region us-east-1`. An SNS email notification is optional.

- Break it: `aws s3 rm` the `health.html` object. Watch the checkers flip,
  then the alarm. Put the object back and watch it recover. Time each
  transition.

##### Question: HTTP or HTTPS

_Your default cache behavior redirects HTTP to HTTPS. Route 53 treats any
`2xx` or `3xx` status as healthy. What would an `HTTP` health check on a
path served by that behavior report if the origin was down? How would you
make an `HTTP` check meaningful, and what does choosing `HTTPS` cost?
(Note that HTTPS health checks don't validate the certificate.)_

##### Question: Timing

_From the moment you deleted the object, how long until Route 53 called the
endpoint unhealthy, and how long until the alarm fired? Work out the best
case from the interval and failure threshold. Why is the real number
different?_

#### Lab 21.3.4: Failover routing

Add a pair of failover records for `app.<zone>` to `routing.yaml`:

- **Primary**, with the health check from Lab 21.3.3 attached:
  - **Real domain and Lab 21.2.5 done:** an `A` alias record to the
    distribution. Add `app.<zone>` to the distribution's alternate domain
    names and certificate first; an alias to CloudFront must match one.
  - **No domain:** a `CNAME` failover record whose value is the
    distribution's `cloudfront.net` name. The DNS answer is what you're
    testing; a browser couldn't use it, because the distribution doesn't
    know the name `app.<zone>`.
- **Secondary**, with no health check: a "maintenance" answer. Use a
  record of the same type: a documentation address for the alias path, or
  `maintenance.<zone>` for the `CNAME` path (with its own record).

Then:

- Test with `test-dns-answer`, delete `health.html` again, wait for the
  check to go unhealthy, and test again. Restore the object.

- Read the note in the
  [AliasTarget](https://docs.aws.amazon.com/Route53/latest/APIReference/API_AliasTarget.html)
  reference about `EvaluateTargetHealth` and CloudFront distributions.

##### Question: Evaluate target health

_Why can't an alias to CloudFront use `EvaluateTargetHealth`, while an alias
to an ALB can? What does `EvaluateTargetHealth` on an ALB alias actually
check?_

##### Question: Failover in a private zone

_Route 53 health checkers run on the internet. How would you fail over
between two private IP addresses in your private zone? (Read [Configuring
failover in a private hosted
zone](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-private-hosted-zones.html).)_

#### Lab 21.3.5: Calculated health checks (optional)

- Create a second endpoint health check against a path that is always
  healthy (for example `/index.html` on the distribution).

- Create a calculated health check that is healthy when at least one of
  the two children is healthy. Break `health.html` and watch the parent.

- Delete both new health checks when you're done.

##### Question: When to calculate

_Give a real situation where a calculated health check is better than
attaching several health checks to several records._

### Retrospective 21.3

#### Question: TTL is the real failover time

_Your failover record has a TTL of 300 seconds. The primary fails. Add up
the worst case before a user who has just resolved the name is sent to the
secondary. Which parts can you shorten, and what does each cost you?_

#### Question: DNS or something else

_DNS failover depends on clients re-resolving. Read about [AWS Global
Accelerator](https://docs.aws.amazon.com/global-accelerator/latest/dg/what-is-global-accelerator.html)
and the routing controls in [Amazon Application Recovery
Controller](https://docs.aws.amazon.com/r53recovery/latest/dg/what-is-route53-recovery.html)
(module 27). When would you choose each over plain Route 53 failover?_

#### Question: The other policies

_This lesson skipped multivalue answer, IP-based and geoproximity routing.
For each, write one sentence on when you'd use it. Which of them can't be
used in a private hosted zone?_

## Lesson 21.4: AWS WAF at the edge

### Principle 21.4

*Filter requests at the edge, before they cost you anything. Start every
rule in Count mode, read the logs, then block, and prove each rule with a
request that should pass and one that shouldn't.*

### Practice 21.4

AWS WAF evaluates each request against a *web ACL*: an ordered list of
rules, each with an action (Allow, Block, Count, CAPTCHA or Challenge), and
a default action for requests no rule decides. Rules can be your own or
*managed rule groups* maintained by AWS or by vendors. Each rule costs
*web ACL capacity units* (WCUs); a web ACL includes 1,500 before extra
charges apply.

For CloudFront, the web ACL is a global resource with scope `CLOUDFRONT`,
and you create and manage it **in `us-east-1`**. You attach it by setting
the distribution's `WebACLId` to the web ACL's ARN, not with
`wafv2 associate-web-acl` (which is for regional resources such as ALBs and
API Gateway). AWS Shield Standard already protects every distribution
against common network and transport layer DDoS attacks at no charge.

Read [How AWS WAF
works](https://docs.aws.amazon.com/waf/latest/developerguide/how-aws-waf-works.html)
and [Using AWS WAF with Amazon
CloudFront](https://docs.aws.amazon.com/waf/latest/developerguide/cloudfront-features.html).

#### Lab 21.4.1: A web ACL in us-east-1

- Write `waf.yaml` with an `AWS::WAFv2::WebACL`:
  - scope `CLOUDFRONT`, default action Allow, CloudWatch metrics and
    sampled requests turned on (`VisibilityConfig`) for the web ACL and
    every rule;
  - two AWS managed rule groups: the core rule set and the known bad inputs
    rule group (find their names in the
    [AWS Managed Rules
    list](https://docs.aws.amazon.com/waf/latest/developerguide/aws-managed-rule-groups-list.html)),
    each with its **override action set to Count** for now;
  - an output with the web ACL's ARN.

- This is a lab about Regions: deploy the stack with `--region us-east-1`.

- Complete the parameter `TODO(student)` in `edge-site.yaml`: take the web
  ACL ARN as an optional parameter and set the distribution's `WebACLId`
  when it's given. Update the `us-east-2` stack with the ARN.

- List the web ACLs with
  `aws wafv2 list-web-acls --scope CLOUDFRONT --region us-east-1`, then run
  the same command without `--region`. Explain the difference.

##### Question: Two Regions, one site

_Your distribution's stack is in `us-east-2` and its web ACL's stack is in
`us-east-1`. Why can't one stack create both? What breaks if someone
deletes the `us-east-1` stack while the distribution still references it?_

##### Question: Capacity

_How many WCUs do your two managed rule groups use? Find out with
`aws wafv2 describe-managed-rule-group` or `check-capacity`. How much room
is left before you'd pay for extra capacity?_

#### Lab 21.4.2: Count, log, then block

- Create a CloudWatch Logs log group named `aws-waf-logs-<you>` in
  `us-east-1`, with a one-day retention. The prefix is required; read
  [Sending web ACL traffic logs to CloudWatch
  Logs](https://docs.aws.amazon.com/waf/latest/developerguide/logging-cw-logs.html).
  Turn on logging for the web ACL (`aws wafv2 put-logging-configuration`,
  `--region us-east-1`).

- Send three requests to your distribution with `curl`:
  - a normal page request;
  - a request with a cross-site scripting payload in the query string,
    such as `?q=<script>alert(1)</script>` (URL-encode it);
  - a request with a Log4j-style lookup string, such as
    `${jndi:ldap://example.com/a}`, in a header.

- All three still return `200`. Find them in the log with `aws logs tail
  --region us-east-1` and in `aws wafv2 get-sampled-requests`. Which rules
  matched, and where does the log record a match that only counted?

- Change both managed rule groups' override action to none (use the rule
  group's own actions), update the stack, and repeat the requests. The
  second and third should now be blocked.

##### Question: Why count first

_On a real site, what would you look for in a week of Count-mode logs
before switching a managed rule group to block? How do you exclude one
rule inside a managed group that blocks legitimate traffic without turning
off the whole group?_

##### Question: Where to look

_A user reports a `403` from your site. How do you tell whether it came
from WAF, from CloudFront, or from S3 through OAC? Name the log or response
detail for each._

#### Lab 21.4.3: Rules you write

Add two rules of your own to `waf.yaml`, both starting in Count:

- **A rate-based rule** that blocks a single client IP making more than a
  small number of requests in a one-minute evaluation window. Read
  [Rate-based rule high-level
  settings](https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-statement-type-rate-based-high-level-settings.html)
  for the lowest limit allowed. Give its Block action a custom response
  with status `429`.

- **A path rule** that blocks any request whose URI path starts with
  `/admin`, with a custom `403` response body.

Test each one:

- Positive: normal page requests still return `200`.
- Negative: `/admin/anything` returns your custom `403`.
- Negative: a `curl` loop that sends a few hundred requests starts getting
  `429`. It can take a minute or more to kick in; read [Rate-based rule
  caveats](https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-statement-type-rate-based-caveats.html).

Switch both rules to enforce only after you've seen them match in Count.

##### Question: Rule order

_Your rate-based rule is evaluated after the managed rule groups. A client
sends a flood of requests, half of which the core rule set blocks. Do the
blocked ones count toward the rate limit? Would you put the rate-based
rule first or last, and why?_

##### Question: Aggregation keys

_Many users behind one corporate NAT share an IP address. What other
aggregation keys could a rate-based rule use, and what are the risks of
keying on a header the client controls?_

#### Lab 21.4.4: Clean up the module

Work in this order. Some steps depend on earlier ones.

- **Detach WAF:** update `edge-site.yaml` with an empty web ACL parameter
  and wait for the distribution to deploy.

- **Delete in `us-east-1`** (`--region us-east-1` on each command): the
  web ACL's logging configuration, the `waf.yaml` stack, the
  `aws-waf-logs-<you>` log group, the health check alarm, any SNS topic you
  made for it, and the ACM certificate if you requested one (only after
  nothing uses it).

- **Delete routing:** the `routing.yaml` stack (records and health checks)
  and any calculated health checks you created by hand. Confirm with
  `aws route53 list-health-checks` that none of yours remain.

- **Delete the site:** empty the bucket, then delete the `edge-site.yaml`
  stack. CloudFormation disables the distribution and deletes it; this
  takes a while.
  <!-- VERIFY: that deleting a stack disables and then deletes an enabled
  AWS::CloudFront::Distribution without manual steps. -->

- **Delete the zones:** the `private-records.yaml` stack, any records you
  added by hand (the apex `CNAME` attempt should have failed; check),
  then the `zones.yaml` stack. A hosted zone can't be deleted while it
  holds records other than its own `NS` and `SOA`.

- **Real domain only:** remove the delegation `NS` record for
  `lab.<your-domain>` from the parent zone. A delegation to deleted name
  servers is a dangling record that someone else could take over.

- **Leftovers:** the Resolver query log group in `us-east-2` and the test
  instance stack, if they still exist.

- **Confirm** with `aws route53 list-hosted-zones`,
  `aws cloudfront list-distributions`,
  `aws wafv2 list-web-acls --scope CLOUDFRONT --region us-east-1`, and
  `aws cloudformation list-stacks` in both Regions.

- **A registered domain** keeps renewing (and charging) every year until
  you turn off automatic renewal. Decide whether to keep it. Its hosted
  zone costs $0.50 a month for as long as it exists.

### Retrospective 21.4

#### Question: Shield Advanced

_Shield Advanced costs $3,000 a month with a one-year commitment. What does
it add over Shield Standard and WAF, and who is it for?_

#### Question: Flat-rate plans

_Read [CloudFront flat-rate pricing
plans](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/flat-rate-pricing-plan.html).
The Free plan costs $0 a month and covers the distribution, a web ACL and
its rules, and an attached Route 53 zone, within usage allowances. Why did
this module use pay-as-you-go anyway? Consider: what must stay associated
with a distribution on a plan, what the docs say about deleting such a
distribution, which WAF features aren't supported, and which accounts
aren't eligible. For a real personal website, would you choose the Free
plan?_

#### Question: Defense in depth

_List every layer between an attacker on the internet and an object in your
bucket: DNS, Shield, WAF, CloudFront, OAC, the bucket policy, Block Public
Access, encryption. For each, name one attack it stops that the layers
after it wouldn't._

## Further Reading

- [Amazon Route 53 Developer
  Guide: DNS failover configurations](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-configuring.html),
  including active-active and active-passive designs with complex trees of
  records.
- [Traffic flow](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/traffic-flow.html)
  for versioned, visual routing policies (with its own charges).
- [Route 53 Resolver DNS
  Firewall](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver-dns-firewall.html):
  block lookups of known-bad domains from your VPCs. SOA-C03 lists it
  alongside AWS WAF, Shield and Network Firewall.
- [CloudFront Functions and
  Lambda@Edge](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/edge-functions.html):
  run code at the edge, for example to rewrite `/about/` to
  `/about/index.html` for a static site.
- [CloudFront standard
  logging](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/AccessLogs.html)
  and [real-time
  logs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/real-time-logs.html).
- [Using AWS WAF to control
  access](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/distribution-web-awswaf.html)
  from the CloudFront side, including one-click protection.
- [AWS Best Practices for DDoS
  Resiliency](https://docs.aws.amazon.com/whitepapers/latest/aws-best-practices-ddos-resiliency/aws-best-practices-ddos-resiliency.html)
  (whitepaper).
