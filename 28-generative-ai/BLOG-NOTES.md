# Blog notes: Topic 28, Generative AI on AWS

## Working title

Bedrock for people who have to pay the bill and pass the audit

Alternatives: "Your region SCP just broke Amazon Bedrock (and the one
condition key that fixes it)"; "RAG for pennies: a Bedrock knowledge base
on S3 Vectors instead of a $350-a-month search cluster".

## Hook

The 2022 course had no generative AI, and most Bedrock tutorials written
since are already wrong. Model access requests are gone (every model is on
by default, with a Marketplace subscription on first use). Many models in
`us-east-2` are reachable only through cross-Region inference profiles,
which a standard region-deny SCP quietly blocks. The quick-create vector
store in older walkthroughs bills a minimum of OCUs around the clock, while
S3 Vectors now does the same job for cents. Bedrock Agents closed to new
customers in July 2026 in favour of AgentCore, and Amazon Q Developer's
IDE plugins are heading for end of support with Kiro as their successor.
Meanwhile generative AI has its own certification (AIF-C01), a skill on
Security Specialty, and a place in the CloudOps guide. This module builds a
support-ticket classifier, a RAG assistant, a guardrail and an agent in a
lab account, and then attacks them.

## Key points

1. **A model is an API priced per token, and the path matters.** Converse
   is the one API to learn; usage comes back on every response. A Nova
   Lite call costs about 1/60th of the same call on Claude Sonnet 4.6.
   Cross-Region inference profiles (`us.`, `global.`) are how many models
   reach `us-east-2`, priced by the source Region.
2. **Region guardrails need a Bedrock exception, not a wider allowlist.**
   A geographic profile fails if any destination Region is denied. The fix
   is a `bedrock:InferenceProfileArn` condition in the region-deny SCP,
   limited to the profiles you approve, which also makes the geographic
   versus global data-residency decision explicit.
3. **Prompt engineering is testing.** A labelled ticket set and a small
   script turn "this prompt reads better" into accuracy, tokens and cost per
   1,000 tickets. Temperature 0 isn't fully deterministic, and the injected
   ticket shows why the reply must be validated.
4. **RAG cheaply: S3 Vectors.** A self-managed knowledge base with Titan
   Text Embeddings V2 and an S3 vector index costs cents; the OpenSearch
   Serverless classic minimum costs hundreds of dollars a month.
   Chunking is a create-only choice.
5. **Guardrails are controls to test, not magic.** `ApplyGuardrail` tests
   policies with no model. PII masking, denied topics, prompt-attack
   filtering and contextual grounding each catch different things; IAM
   (`bedrock:GuardrailIdentifier`) and account/organization enforcement
   make them mandatory.
6. **Agents: own the loop, then hand it to a harness.** A hand-written
   Converse tool loop, a human approval step for the refund tool, then the
   same agent on an AgentCore harness with inline functions, no shell tool,
   memory off and hard limits. Indirect prompt injection through a
   knowledge base document is the finale.

## Gotchas readers will hit

- **The region SCP from module 19 blocks `us.` profiles.** The error only
  says an SCP denied it; you have to know the destination Regions
  (`get-inference-profile`) to see why.
- **Global profiles evaluate `aws:RequestedRegion` as `unspecified`,**
  which a region allowlist denies unless you plan for it.
- **Nova Micro isn't in-Region in `us-east-2`;** Nova Lite and Titan Text
  Embeddings V2 are. Model availability per Region changes often.
- **Titan Text Embeddings V2 has no inference profile.** The knowledge
  base's embedding model must be in-Region.
- **The AWS CLI can't stream Bedrock responses;** use boto3
  `converse_stream`.
- **OpenSearch Serverless classic collections bill a minimum of OCUs
  while idle.** NextGen collections (May 2026) scale to zero, but only in a
  collection group. Check what a quick-create wizard made.
- **Chunking and parsing settings are create-only** on a data source;
  changing them in CloudFormation replaces it.
- **A new account can't create a Bedrock Agent** (Agents Classic
  maintenance mode since 2026-07-30); older tutorials and exam questions
  still use them.
- **The AgentCore harness defaults to Claude Sonnet 4.6** if you don't set
  a model, turns on memory by default, and exposes `shell` and
  `file_operations` tools unless `allowedTools` says otherwise.
- **Invocation logs contain every prompt,** including PII a guardrail
  masked in the reply. The log group is now sensitive data.
- **Long-term Bedrock API keys create an IAM user.** Deny
  `bedrock:CallWithBearerToken` and control
  `iam:CreateServiceSpecificCredential`.
- **Contextual grounding doesn't stop a poisoned document:** the answer is
  grounded, in the attacker's text.

## Exam objectives supported

- AIF-C01 Domain 2 (Tasks 2.1–2.3: tokens, embeddings, token-based
  pricing, agentic concepts, Bedrock, AgentCore, Kiro, cost trade-offs),
  Domain 3 (Tasks 3.1, 3.2 and 3.4: model selection, inference parameters,
  RAG, vector stores, prompt techniques and risks, evaluation), Domain 4
  (Task 4.1: Guardrails) and Domain 5 (Tasks 5.1 and 5.2: IAM,
  PrivateLink, prompt injection, logging, residency)
- SCS-C03 Domain 3 (Skill 3.2.7: protections and guardrails for GenAI
  applications, OWASP Top 10 for LLM Applications), plus Domains 1, 4 and
  5 for logging, model-level IAM and data protection
- SOA-C03 Domain 4 (Skill 4.1.5: enforce Region selections; Skill 4.1.2:
  audit with CloudTrail) and the Bedrock and Kiro in-scope services
- DVA-C03 and SAP-C03 GenAI / agent topics once their guides publish on
  2026-10-27

## Material to capture while doing the labs

- The SCP denial for `us.amazon.nova-micro-v1:0`, the destination Region
  list from `get-inference-profile`, and the before/after SCP diff (with
  account IDs as `*`).
- A table of the prompt variants from Lab 28.2 with accuracy, tokens and
  cost per 1,000 tickets on Nova Micro and Nova Lite; the tickets that flip
  between runs at temperature 0.
- The `retrieve-and-generate` answer with citations, and the same question
  answered after the poisoned `partner-faq.txt` was ingested, with and
  without each defence tried.
- `ApplyGuardrail` results for the PII, injection, denied-topic and
  grounding tests, including grounding and relevance scores.
- A trace of one harness session from the AgentCore observability view,
  and the token counts compared with the hand-written loop.
- A Logs Insights query of tokens by principal and by `requestMetadata`.
- Cost Explorer for the module, grouped by service and usage type, with
  account IDs redacted.
