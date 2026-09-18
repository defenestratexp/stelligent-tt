# Blog Notes: Module 04, VPCs

## Working title

Retire the bastion: reaching private EC2 instances in 2026 without SSH keys,
open ports or surprise bills

## Hook

The classic VPC tutorial ends the same way every time: an Elastic IP on an
instance in the public subnet, port 22 open to the world, a `.pem` file on
your laptop, and a NAT gateway so the private instance can install
packages. In 2026 every part of that has a better answer or a price tag.
Session Manager and EC2 Instance Connect Endpoint get you a shell on a
private instance with IAM instead of keys and no inbound rule from the
Internet. Since February 2024 every public IPv4 address costs about $3.60 a
month, and a NAT gateway left running through a month of evening study costs
more than everything else in the lab put together. This post rebuilds the
old two-subnet lab the current way and shows where the money goes.

## Key points

1. **Two ways in, no bastion.** Session Manager works *outbound* (the SSM
   Agent calls Systems Manager on 443, so it needs a NAT gateway, a public
   IP or three interface endpoints). EC2 Instance Connect Endpoint works
   *inbound* (a network interface in your subnet tunnels to the instance's
   private IP on 22, from its own security group only). Delete the NAT
   gateway and only one of them still works; that's the demo.
2. **What a public subnet actually is:** a route to an Internet gateway.
   A public IP alone isn't enough, and neither is the route alone. The
   "can I reach it now?" sequence (no IP, security group, Elastic IP) makes
   that concrete.
3. **The cost of connecting to the Internet.** Public IPv4 at $0.005/hour
   per address, running or idle; NAT gateway at $0.045/hour plus $0.045/GB
   in `us-east-2`; S3 gateway endpoints and Instance Connect Endpoints free.
   One NAT per AZ versus shared, and the new regional NAT gateway mode.
   Public IP insights in the free IPAM tier finds every address you pay for.
4. **Stateless ACLs bite Session Manager.** A network ACL that only allows
   ping in silently breaks Session Manager and the NAT gateway, because the
   replies to their outbound connections arrive on ephemeral ports.
5. **Reachability Analyzer instead of trial and error.** It reads the
   configuration, names the blocking security group, ACL or route, and
   costs $0.10 an analysis. (TCP and UDP only, so it can't answer the ping
   question.)
6. **Plan address space before you peer.** Peering needs non-overlapping
   CIDRs and isn't transitive; IPAM pools hand out non-overlapping blocks
   (Advanced Tier for private IPv4).

## Gotchas readers will hit

- The *minimal* AL2023 AMI doesn't ship the SSM Agent or EC2 Instance
  Connect. Use the standard `al2023-ami-kernel-default` parameter.
- `aws ssm start-session` needs the Session Manager plugin installed
  locally; the error doesn't say so clearly.
- An instance with the right role but no route out never shows up in
  `describe-instance-information`, which is the quickest "does it have
  egress?" test there is.
- Only one EC2 Instance Connect Endpoint per VPC and five per region; the
  endpoint's security group needs an *outbound* 22 rule, and the instance's
  security group must reference it.
- Disassociating an Elastic IP doesn't stop its charge; releasing it does.
  Stopping an instance doesn't stop the charge on an attached Elastic IP.
- Network ACLs can't reference prefix lists, so an S3 gateway endpoint
  behind a strict ACL needs S3's CIDR ranges or a broad egress rule.
- A bucket policy `Deny` on `aws:SourceVpce` also blocks you from your
  laptop and CloudFormation unless you exempt your role.
- IPAM's Free Tier doesn't manage private IPv4 pools; the pool lab needs the
  Advanced Tier (cheap, but billed per active IP until you delete it).

## Exam objectives

- SAA-C03 Domain 1 (1.2 secure workloads: VPC security components, network
  segmentation), Domain 3 (3.4 network architectures) and Domain 4 (4.4
  cost-optimized network architectures: NAT gateway per AZ vs shared, VPC
  endpoints)
- SOA-C03 Domain 5: Networking and Content Delivery (5.1.1 configure a VPC,
  5.1.2 private connectivity, 5.1.4 network cost, 5.3.1 troubleshoot VPC
  configurations)
- SCS-C03 Domain 3: Infrastructure Security
