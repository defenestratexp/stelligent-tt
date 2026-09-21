# Topic 28: Generative AI on AWS

<!-- TOC -->

- [Topic 28: Generative AI on AWS](#topic-28-generative-ai-on-aws)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Guidance](#guidance)
  - [Conventions](#conventions)
  - [Lesson 28.1: Foundation models on Amazon Bedrock](#lesson-281-foundation-models-on-amazon-bedrock)
    - [Principle 28.1](#principle-281)
    - [Practice 28.1](#practice-281)
      - [Lab 28.1.1: What you can call from us-east-2](#lab-2811-what-you-can-call-from-us-east-2)
      - [Lab 28.1.2: Your first Converse call](#lab-2812-your-first-converse-call)
      - [Lab 28.1.3: Inference parameters](#lab-2813-inference-parameters)
      - [Lab 28.1.4: Cross-Region inference meets your region guardrail](#lab-2814-cross-region-inference-meets-your-region-guardrail)
      - [Lab 28.1.5: What did that cost?](#lab-2815-what-did-that-cost)
    - [Retrospective 28.1](#retrospective-281)
  - [Lesson 28.2: Prompt engineering](#lesson-282-prompt-engineering)
    - [Principle 28.2](#principle-282)
    - [Practice 28.2](#practice-282)
      - [Lab 28.2.1: Zero-shot, few-shot and the system prompt](#lab-2821-zero-shot-few-shot-and-the-system-prompt)
      - [Lab 28.2.2: Output you can parse](#lab-2822-output-you-can-parse)
      - [Lab 28.2.3: Measure, don't admire](#lab-2823-measure-dont-admire)
    - [Retrospective 28.2](#retrospective-282)
  - [Lesson 28.3: Retrieval-augmented generation with Knowledge Bases](#lesson-283-retrieval-augmented-generation-with-knowledge-bases)
    - [Principle 28.3](#principle-283)
    - [Practice 28.3](#practice-283)
      - [Lab 28.3.1: Embeddings by hand](#lab-2831-embeddings-by-hand)
      - [Lab 28.3.2: A knowledge base on S3 Vectors](#lab-2832-a-knowledge-base-on-s3-vectors)
      - [Lab 28.3.3: Ingest, retrieve, generate](#lab-2833-ingest-retrieve-generate)
      - [Lab 28.3.4: Chunking and choosing a vector store](#lab-2834-chunking-and-choosing-a-vector-store)
    - [Retrospective 28.3](#retrospective-283)
  - [Lesson 28.4: Guardrails](#lesson-284-guardrails)
    - [Principle 28.4](#principle-284)
    - [Practice 28.4](#practice-284)
      - [Lab 28.4.1: A guardrail in CloudFormation](#lab-2841-a-guardrail-in-cloudformation)
      - [Lab 28.4.2: Test it without a model](#lab-2842-test-it-without-a-model)
      - [Lab 28.4.3: Contextual grounding](#lab-2843-contextual-grounding)
      - [Lab 28.4.4: Make the guardrail mandatory](#lab-2844-make-the-guardrail-mandatory)
    - [Retrospective 28.4](#retrospective-284)
  - [Lesson 28.5: Agents and tools](#lesson-285-agents-and-tools)
    - [Principle 28.5](#principle-285)
    - [Practice 28.5](#practice-285)
      - [Lab 28.5.1: The agent loop by hand](#lab-2851-the-agent-loop-by-hand)
      - [Lab 28.5.2: A human in the loop](#lab-2852-a-human-in-the-loop)
      - [Lab 28.5.3: Bedrock Agents Classic, on paper](#lab-2853-bedrock-agents-classic-on-paper)
      - [Lab 28.5.4: The same agent on an AgentCore harness](#lab-2854-the-same-agent-on-an-agentcore-harness)
    - [Retrospective 28.5](#retrospective-285)
  - [Lesson 28.6: AI coding assistants](#lesson-286-ai-coding-assistants)
    - [Principle 28.6](#principle-286)
    - [Practice 28.6](#practice-286)
      - [Lab 28.6.1: Amazon Q Developer and Kiro in 2026](#lab-2861-amazon-q-developer-and-kiro-in-2026)
      - [Lab 28.6.2: Steer an assistant with the course rules (optional)](#lab-2862-steer-an-assistant-with-the-course-rules-optional)
    - [Retrospective 28.6](#retrospective-286)
  - [Lesson 28.7: Securing generative AI workloads](#lesson-287-securing-generative-ai-workloads)
    - [Principle 28.7](#principle-287)
    - [Practice 28.7](#practice-287)
      - [Lab 28.7.1: A least-privilege invoker role](#lab-2871-a-least-privilege-invoker-role)
      - [Lab 28.7.2: Log every model invocation](#lab-2872-log-every-model-invocation)
      - [Lab 28.7.3: Indirect prompt injection](#lab-2873-indirect-prompt-injection)
      - [Lab 28.7.4: Where your data goes](#lab-2874-where-your-data-goes)
      - [Lab 28.7.5: Clean up the module](#lab-2875-clean-up-the-module)
    - [Retrospective 28.7](#retrospective-287)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- **New module.** The 2022 course had no generative AI at all. In 2026 it
  has its own exam (AWS Certified AI Practitioner, AIF-C01), a skill of its
  own on Security Specialty (SCS-C03 Skill 3.2.7: guardrails for generative
  AI applications), Amazon Bedrock and Kiro in scope for CloudOps
  (SOA-C03), and GenAI and agent topics in the DVA-C03 and SAP-C03 guides
  that publish on 2026-10-27.
- **Model access is automatic.** The old "request model access" page is
  gone: every serverless model is enabled by default. Third-party models
  subscribe through AWS Marketplace on first use, and Anthropic models still
  need a one-time use-case form. The labs use Amazon Nova models, which need
  neither.
- **Cross-Region inference is the normal path, not an extra.** Many models
  are offered in `us-east-2` only through a geographic (`us.`) or global
  (`global.`) inference profile. That collides with the region guardrail
  SCP you wrote in module 19. Lab 28.1.4 makes it fail and fixes it the way
  AWS now documents, with the `bedrock:InferenceProfileArn` condition key.
- **A cheap vector store exists.** Knowledge bases can use Amazon S3
  Vectors (GA December 2025), which bills for storage and queries only. The
  2024-era default, an OpenSearch Serverless *classic* collection, bills a
  minimum number of OCUs around the clock; see [Cost and
  cleanup](#cost-and-cleanup).
- **Bedrock Agents is now "Agents Classic" and closed to new customers**
  (2026-07-30). A new lab account can't create one. Agents are built on
  **Amazon Bedrock AgentCore** instead; its managed **harness** is the
  config-based replacement, and Lesson 28.5 uses it.
- **Amazon Q Developer is being replaced by Kiro** for IDE and CLI work:
  no new Q Developer sign-ups since 2026-05-15 and end of support for the
  IDE plugins and paid subscriptions on 2027-04-30. Q Developer in the AWS
  console and in chat applications continues.
- **Guardrails grew up.** Standard and Classic safeguard tiers, a prompt
  attack filter, contextual grounding and Automated Reasoning checks, the
  standalone `ApplyGuardrail` API, and account- and organization-level
  guardrail enforcement.
- **Bedrock API keys** (bearer tokens) exist, including long-term keys that
  quietly create an IAM user. Lesson 28.7 treats them the way module 00
  treats IAM user access keys: as something to deny.

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| AIF-C01 | Domain 2: Fundamentals of GenAI (Task 2.1: tokens, chunking, embeddings, vectors, token-based pricing, context engineering, and agentic concepts: tool usage, memory, MCP; Task 2.2: limitations such as hallucinations and nondeterminism, and model selection by cost, latency and compliance; Task 2.3: Amazon Bedrock, Kiro, Strands Agents and Amazon Bedrock AgentCore, and cost trade-offs including Regional coverage and token-based pricing) |
| AIF-C01 | Domain 3: Applications of Foundation Models (Task 3.1: FM selection criteria including prompt caching, inference parameters, RAG with Knowledge Bases, vector stores on AWS, customization cost trade-offs, agents; Task 3.2: zero-, single- and few-shot, chain-of-thought, prompt templates, Prompt Management, and prompt risks: exposure, poisoning, hijacking, jailbreaking; Task 3.3: fine-tuning and distillation, on paper only; Task 3.4: human evaluation, Bedrock Model Evaluation, LLM-as-a-judge) |
| AIF-C01 | Domain 4: Guidelines for Responsible AI (Task 4.1: features of responsible AI and tools to support them, such as Amazon Bedrock Guardrails; legal risks including hallucinations; Task 4.2: transparency and human oversight) |
| AIF-C01 | Domain 5: Security, Compliance, and Governance for AI Solutions (Task 5.1: IAM, encryption, PrivateLink, the shared responsibility model, Policy in AgentCore, Guardrails, prompt injection, output validation, audit logging of AI interactions, grounding; Task 5.2: CloudTrail, data residency, logging and retention) |
| SOA-C03 | Amazon Bedrock and Kiro are in scope. Domain 1: Monitoring, Logging, Analysis, Remediation, and Performance Optimization (Skill 1.2.1 names Kiro among the tools for analysing metrics and automating remediation); Domain 4: Security and Compliance (Skill 4.1.2: audit access with CloudTrail; Skill 4.1.5: enforce Region selections, which is Lab 28.1.4) |
| SCS-C03 | Domain 3: Infrastructure Security (Skill 3.2.7: implement protections and guardrails for generative AI applications, for example by applying the OWASP Top 10 for LLM Applications). Also Domain 1: Detection (invocation logging, CloudTrail), Domain 4: Identity and Access Management (model-level IAM, API keys) and Domain 5: Data Protection |
| DVA-C02 → C03 | Domain 1: Development with AWS Services (Task 1.1: write code that uses AWS services through the SDK). The C03 guide publishes 2026-10-27 and adds GenAI / agent topics; map this module to it when it does |
| SAP-C02 → C03 | Domain 2: Design for New Solutions (security, cost and Region design for a new workload). The C03 guide publishes 2026-10-27 and adds GenAI / agent topics |

AIF-C01 Domain 1 (Fundamentals of AI and ML, 20%) is mostly outside this
module: it covers classical ML and the ML lifecycle on Amazon SageMaker AI.
Read its task statements and the SageMaker AI overview in [Further
Reading](#further-reading) alongside Lesson 28.1.

## Cost and cleanup

Almost everything here is billed **per token, per request or per text
unit**, so an idle module costs close to nothing. The exceptions are a
vector store that bills by the hour and an agent session left warm. Prices
below are for `us-east-2`, Standard tier, on demand, read from the AWS Price
List API on 2026-09-18.

- **Model inference: pick a small model and it rounds to zero.**

  | Model (ID used in the labs) | How `us-east-2` reaches it | Input / output per 1M tokens |
  |---|---|---|
  | Amazon Nova Lite (`amazon.nova-lite-v1:0`) | In-Region, or `us.` profile | $0.06 / $0.24 |
  | Amazon Nova Micro (`us.amazon.nova-micro-v1:0`) | `us.` profile only | $0.035 / $0.14 |
  | Amazon Nova 2 Lite (`us.amazon.nova-2-lite-v1:0`) | `us.` or `global.` profile only | $0.33 / $2.75 (`global.`: $0.30 / $2.50) |
  | Anthropic Claude Haiku 4.5 | `us.` or `global.` profile only | $1.10 / $5.50 (`global.`: $1.00 / $5.00) |
  | Anthropic Claude Sonnet 4.6 | `us.` or `global.` profile only | $3.30 / $16.50 (`global.`: $3.00 / $15.00) |
  | Amazon Titan Text Embeddings V2 (`amazon.titan-embed-text-v2:0`) | In-Region only | $0.02 input, no output |

  **Worked estimate.** Suppose the whole module makes 1,000 model calls
  averaging 1,500 input tokens and 300 output tokens (generous: most labs
  send a few hundred tokens). That is 1.5 million input and 0.3 million
  output tokens.
  - On Nova Lite: 1.5 × $0.06 + 0.3 × $0.24 = $0.09 + $0.072 = **about
    $0.16**.
  - The same traffic on Claude Sonnet 4.6 through the `us.` profile: 1.5 ×
    $3.30 + 0.3 × $16.50 = $4.95 + $4.95 = **about $9.90**, some 60 times
    more.
  - One prompt-evaluation run in Lab 28.2.3 (24 tickets × 4 prompt
    variants × 3 repeats = 288 calls, about 600 input and 10 output tokens
    each) on Nova Lite: 172,800 × $0.06 / 1M + 2,880 × $0.24 / 1M ≈
    **$0.011**.

  Output tokens cost four to eight times more than input tokens, and a
  global profile is about 10% cheaper than a geographic one. Batch
  inference is half price. The price follows the **source** Region you
  call, not the Region that serves the request.
- **Embeddings** for the course corpus (a few kilobytes) cost a fraction of
  a cent; embedding every README in this repository once would cost about a
  cent.
- **Knowledge base vector store: this is where the money is.**
  - **Amazon S3 Vectors (used in the labs):** $0.06 per GB-month stored,
    $0.20 per GB uploaded, $2.50 per million queries plus a per-TB charge
    for data processed. The lab's few hundred vectors cost well under a
    cent a month. S3 Vectors is available in `us-east-2`.
  - **Amazon Aurora PostgreSQL Serverless v2** can scale to 0 ACUs and
    auto-pause when idle, so it is the cheap choice if you need SQL, hybrid
    search or metadata-heavy filtering. You still pay for storage, and the
    first query after a pause waits for it to resume.
    <!-- VERIFY: whether the Bedrock console's Aurora quick-create sets a
    minimum capacity of 0 ACUs, and the us-east-2 ACU-hour price. -->
  - **Amazon OpenSearch Serverless: read this before you click "quick
    create".** A *classic* collection bills a **minimum of 2 OCUs** (1 with
    redundancy disabled for dev/test), around the clock, whether or not
    you query it. At $0.24 per OCU-hour that is about **$350 a month**, or
    about $175 in dev/test mode, plus storage. Since May 2026 the
    **NextGen** collection type scales to zero after 10 minutes idle, but
    only when it's part of a collection group. Unless you have checked
    which kind a wizard created, assume the classic minimum. This module
    doesn't use OpenSearch Serverless.
    <!-- VERIFY: the us-east-2 OCU-hour price (the pricing page summary
    quotes us-east-1), and whether the Bedrock knowledge base quick-create
    now creates a NextGen collection in a collection group. -->
  - **Bedrock Managed Knowledge Base** (GA June 2026) bundles parsing,
    embedding and storage at $5.00 per GB of raw data per month plus $1.00
    per 1,000 retrievals. It isn't offered in `us-east-2` yet, so the labs
    build a self-managed knowledge base instead.
- **Knowledge base ingestion and retrieval** in a self-managed knowledge
  base cost only the embedding tokens and the vector store operations.
  `RetrieveAndGenerate` adds the generation model's tokens.
- **Guardrails** bill per 1,000 **text units** (a text unit is up to 1,000
  characters) per policy: content filters and denied topics $0.15,
  sensitive information filters $0.10 (regex patterns and word filters are
  free), contextual grounding $0.10, Automated Reasoning $0.17 per policy.
  Contextual grounding counts the source, the query and the response, so a
  RAG answer with 5 KB of retrieved text is at least 6 text units per
  check. The labs make a few hundred checks: cents.
- **AgentCore** has no charge for the harness itself. You pay for model
  tokens, plus **Runtime** at $0.0895 per vCPU-hour of CPU actually used
  and $0.00945 per GB-hour of memory for as long as the session's microVM
  is alive, including the idle timeout (default 15 minutes) after your last
  call. **Memory** (on by default for a harness) is $0.25 per 1,000
  short-term events. **Gateway** calls are $0.005 per 1,000. Observability
  data goes to CloudWatch at CloudWatch prices. A session of the Lab 28.5.4
  agent should cost well under a cent in Runtime. **The harness defaults to
  Claude Sonnet 4.6 if you don't set a model**, so always set one.
  <!-- VERIFY: which AgentCore Runtime price generation (v1 or v2) applies
  to a new harness session, and the default microVM size. -->
- **Model invocation logging** goes to CloudWatch Logs at normal ingestion
  prices; the lab log group has 7-day retention.
- **Kiro** (Lesson 28.6, optional) has a free plan with 50 credits a month;
  paid plans start at $20 per user per month. Nothing in this module needs
  a paid plan.
- **Cleanup:** [Lab 28.7.5](#lab-2875-clean-up-the-module) deletes the
  knowledge base stack (and empties its buckets), the guardrail, the
  harness and its memory, the invocation logging configuration and its log
  group, the test roles, and any Bedrock API key you created. It also
  decides what to keep of the SCP change from Lab 28.1.4.

## Guidance

- Explore the official docs! See the
  [Amazon Bedrock User Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html),
  the [Amazon Bedrock AgentCore Developer Guide](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html),
  the CLI references for
  [bedrock](https://docs.aws.amazon.com/cli/latest/reference/bedrock/),
  [bedrock-runtime](https://docs.aws.amazon.com/cli/latest/reference/bedrock-runtime/),
  [bedrock-agent](https://docs.aws.amazon.com/cli/latest/reference/bedrock-agent/),
  [bedrock-agent-runtime](https://docs.aws.amazon.com/cli/latest/reference/bedrock-agent-runtime/),
  [bedrock-agentcore-control](https://docs.aws.amazon.com/cli/latest/reference/bedrock-agentcore-control/)
  and [s3vectors](https://docs.aws.amazon.com/cli/latest/reference/s3vectors/),
  the [boto3 Converse reference](https://docs.aws.amazon.com/boto3/latest/reference/services/bedrock-runtime/client/converse.html),
  and the CloudFormation reference for
  [AWS::Bedrock::KnowledgeBase](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-bedrock-knowledgebase.html),
  [AWS::Bedrock::DataSource](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-bedrock-datasource.html),
  [AWS::S3Vectors::Index](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-s3vectors-index.html),
  [AWS::Bedrock::Guardrail](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-bedrock-guardrail.html)
  and
  [AWS::BedrockAgentCore::Harness](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-bedrockagentcore-harness.html).

- **Generative AI on AWS changes monthly.** Model IDs, Regional
  availability, prices and even service names in this README were checked
  in September 2026. Before each lab, check the model's page in [Models at
  a glance](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html)
  and [Regional availability by
  model](https://docs.aws.amazon.com/bedrock/latest/userguide/models-region-compatibility.html).
  If the docs disagree with this README, the docs win: note the difference
  in your answers.

- Avoid using other sites like stackoverflow.com for answers \-- part
  of the skill set you're building is finding answers straight from
  the source, AWS. Blog posts about Bedrock more than a year old are
  especially likely to be wrong about model access, agents and pricing.

- Explore your curiosity. Try to understand why things work the way
  they do. Read more of the documentation than just what you need to
  find the answers.

## Conventions

- **Profile and Region.** Everything runs in the lab account with the `lab`
  profile from module 19, in `us-east-2`. Export `AWS_PROFILE=lab` for the
  Python scripts. CLI examples don't pass `--region` except where a lab is
  about Regions.
- **SDK versions.** Bedrock's APIs move fast. Use a current AWS CLI v2 and
  a current boto3 in a virtual environment (`pip install --upgrade boto3`);
  a year-old SDK won't know `requestMetadata`, `serviceTier`, S3 Vectors or
  AgentCore.
- **Names.** Every resource and stack name starts with your identifier,
  shown here as `<you>`: `<you>-kb`, `<you>-guardrail`, `<you>-invoker`.
  Tag everything with `owner=<you>` and `topic=28`.
- **Placeholders.** Examples use `123456789012` for the account ID. Write
  `<lab-account-id>` in your answers. Keep account IDs, knowledge base IDs,
  guardrail IDs and harness ARNs out of your repository: read them from
  stack outputs or environment variables.
- **Model IDs are not ARNs.** Code passes a model ID
  (`amazon.nova-lite-v1:0`) or an inference profile ID
  (`us.amazon.nova-micro-v1:0`). IAM policies and templates build ARNs with
  `${AWS::Region}`, `${AWS::AccountId}` and `${AWS::Partition}`. Never paste
  an ARN containing your account ID into a file you commit.
- **Starter files.** [starter/converse.py](starter/converse.py) sends one
  prompt and reports tokens and cost;
  [starter/eval_prompts.py](starter/eval_prompts.py) and
  [starter/tickets.jsonl](starter/tickets.jsonl) score prompt variants;
  [starter/knowledge-base.yaml](starter/knowledge-base.yaml) is a partial
  knowledge base template; [starter/corpus/](starter/corpus/) is a small
  set of policy documents for a fictional outdoor-gear shop;
  [starter/agent_loop.py](starter/agent_loop.py) is a tool-use loop with
  the interesting step missing. Each has `TODO(student)` markers.
  Everything else you write: templates in YAML, code in Python 3.13 with
  boto3.
- **Templates live next to your answers.** Keep `knowledge-base.yaml`,
  `guardrail.yaml` and `invoker-role.yaml` in your copy of this directory.
  Each must pass `cfn-lint`.
- DO use the AWS CLI, CloudFormation and boto3 rather than the console. The
  Bedrock console's playgrounds are fine for a quick look; anything you
  keep goes in a template or a script.

## Lesson 28.1: Foundation models on Amazon Bedrock

### Principle 28.1

*A foundation model on Bedrock is an API you pay for by the token. You
choose the model, the path your request takes between Regions, and the
parameters that shape the answer; each choice changes the cost, the
latency and the result.*

### Practice 28.1

Amazon Bedrock puts models from Amazon and third parties behind one set of
APIs. The **Converse** API is the one to learn: the same request shape
works for every text model, with a system prompt, a list of messages,
inference parameters and, later, tools and guardrails. A request goes to a
**model ID** (served in your Region) or to an **inference profile** (which
may serve it in another Region). The response tells you exactly how many
input and output tokens you used, which is how you're billed.

Read [Inference using the Converse
API](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html)
and [Route model inference requests across AWS
Regions](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html)
before you start.

#### Lab 28.1.1: What you can call from us-east-2

- Read [Request access to
  models](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html).
  Note what happens the first time you invoke a third-party model, which
  permissions that needs, and what Anthropic models need beyond that.
- List the Amazon text models offered in `us-east-2` with
  `aws bedrock list-foundation-models`. Filter by provider and output
  modality with the command's options and `--query`, not with `grep`.
- List the system-defined inference profiles with
  `aws bedrock list-inference-profiles`. Find the ones for Nova Micro and
  Nova Lite.
- Run `aws bedrock get-inference-profile` on `us.amazon.nova-micro-v1:0`.
  Its `models` list names one foundation-model ARN per **destination
  Region**. Which Regions can a request from `us-east-2` land in?
- Check one model's status with
  `aws bedrock get-foundation-model-availability`.
- Fill in this table for your answers, from the CLI and the model pages in
  [Models at a
  glance](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html):
  model, model ID, in-Region in `us-east-2`?, `us.` profile?, `global.`
  profile?, context window, maximum output tokens, supports tool use?,
  supports guardrails?. Do it for Nova Micro, Nova Lite, Nova 2 Lite,
  Titan Text Embeddings V2 and one Anthropic model.

##### Question: No access page

_In 2024 you had to request access to each model in the console before
using it. What replaced that, and what are the two things that can still
make a first call to a third-party model fail with `AccessDeniedException`?
If your organization must review a model's licence before anyone uses it,
what does the documentation tell you to do instead of relying on "not
subscribed yet"?_

##### Question: Why Nova for the labs

_Name two reasons, one about cost and one about access, why this module's
labs use Amazon Nova models rather than a Claude model. What would you
have to do, once per account or once per organization, before calling a
Claude model?_

#### Lab 28.1.2: Your first Converse call

- Call Nova Lite in-Region with the CLI:
  `aws bedrock-runtime converse --model-id amazon.nova-lite-v1:0` and a
  `--messages` JSON array with one user message. Look at every field in the
  response: `output`, `stopReason`, `usage`, `metrics`.
- Add a `--system` prompt that tells the model it answers only in one
  sentence, and ask the same question again.
- Run [starter/converse.py](starter/converse.py) with the same prompt. Read
  the script: it builds exactly the request you just sent by hand.
- Add streaming to your own copy of the script with boto3's
  `converse_stream` (the AWS CLI doesn't support Bedrock's streaming
  operations). When does the first text arrive compared with the whole
  reply, and where do the token counts appear in a stream?
- Find your calls in CloudTrail **Event history** (`eventName` `Converse`).
  What does the event record, and what doesn't it?

##### Question: Converse or InvokeModel

_`InvokeModel` also calls a model. Compare its request body with
Converse's for Nova Lite and for one Anthropic model (see [Inference
request parameters](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-parameters.html)).
Why does AWS recommend Converse for new code? Which IAM action does a
Converse call need?_

#### Lab 28.1.3: Inference parameters

Use `converse.py --runs` for these; each run is a separate call.

- **Temperature.** Ask "Suggest a name for a hiking-boot brand. Reply with
  the name only." five times at `--temperature 0`, then five times at
  `--temperature 1`. Count the distinct answers.
- **Top P.** Repeat at temperature 1 with `--top-p 0.1`. What changed?
- **Max tokens.** Ask for a 300-word essay with `--max-tokens 40`. What is
  the `stopReason`, and what did you pay for?
- **Stop sequences.** Ask for a numbered list of ten items with
  `--stop "4."`. Where did it stop, and is the stop sequence in the reply?
- Read [Influence response generation with inference
  parameters](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-parameters.html).
  Find how to pass a parameter that Converse doesn't have a field for, such
  as `topK`.

##### Question: Deterministic enough?

_Did temperature 0 give you the same answer every time? What does that
tell you about relying on a model's output in an automated pipeline?
Which settings would you use for classifying support tickets, and which
for suggesting brand names?_

##### Question: Tokens are not words

_Send one short English sentence, the same sentence in another language,
and a line of JSON of similar length. Compare `inputTokens` (or count
them without paying for a generation with `aws bedrock-runtime
count-tokens`). What does that
mean for estimating cost from a character count, and for a context
window?_

#### Lab 28.1.4: Cross-Region inference meets your region guardrail

Nova Micro is offered in `us-east-2` only through the US geographic
profile. Your module 19 region guardrail SCP allows only `us-east-2` and
`us-east-1`.

- Call `us.amazon.nova-micro-v1:0` with `converse.py`. Read the whole
  error. (If it succeeds, confirm that the region SCP from Lab 19.2.2 is
  still attached to the `Sandbox` OU.)
- Read [Geographic cross-Region
  inference](https://docs.aws.amazon.com/bedrock/latest/userguide/geographic-cross-region-inference.html),
  especially "Service Control Policy requirements" and the note after it,
  and [Global cross-Region
  inference](https://docs.aws.amazon.com/bedrock/latest/userguide/global-cross-region-inference.html).
  Work out, from the destination Regions you listed in Lab 28.1.1, which
  authorization check failed.
- Fix it **without** adding a Region to the allowlist for every other
  service. With the `mgmt` profile, edit your module 19
  `scp-region-guardrail.json` so its `Deny` doesn't apply to Bedrock's
  cross-Region routing through the **US geographic** profiles you call from
  `us-east-2`. The documented mechanism is the `bedrock:InferenceProfileArn`
  condition key. Think about how a negated condition operator such as
  `ArnNotLike` behaves when the key isn't in the request at all (see
  [Condition
  operators](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition_operators.html)),
  and use `*` for the account in the ARN pattern rather than your account
  ID.
- Validate the policy with Access Analyzer, update it, and test:
  - Positive: `us.amazon.nova-micro-v1:0` from `us-east-2` now works.
  - Positive: `amazon.nova-lite-v1:0` in-Region still works.
  - Negative: `aws ec2 describe-availability-zones --region us-west-2`
    is still denied.
  - Negative: `global.amazon.nova-2-lite-v1:0` is still denied. (Should
    it be? Decide, and write down why.)
- Compare your change with the "with Bedrock CRIS support" variant in the
  [aws-samples SCP
  examples](https://github.com/aws-samples/service-control-policy-examples)
  and the AWS blog post [Enable Amazon Bedrock cross-Region inference in
  multi-account
  environments](https://aws.amazon.com/blogs/machine-learning/enable-amazon-bedrock-cross-region-inference-in-multi-account-environments/).

<!-- VERIFY: the exact AccessDenied message for a cross-Region inference
call blocked by an SCP on a destination Region, and whether the aws-samples
region-controls variant is still named "with Bedrock CRIS support". -->

##### Question: What the exception opens

_Your exception lets Bedrock route prompts to a Region your SCP otherwise
blocks. What data leaves `us-east-2`, where is it stored, and what does
CloudTrail record, and in which Region? (Look for
`additionalEventData.inferenceRegion`.) Why can't the exception be used to
call Bedrock **from** `us-west-2`?_

##### Question: Geographic or global

_A global profile is about 10% cheaper and has more capacity. When would
you allow it, and when would you add a `Deny` for `global.*` profiles
instead? Which condition value does a global profile's routing check carry
for `aws:RequestedRegion`?_

#### Lab 28.1.5: What did that cost?

- Fill in `PRICES_PER_MILLION` and `estimate_cost()` in your copy of
  `converse.py` from the [Amazon Bedrock pricing
  page](https://aws.amazon.com/bedrock/pricing/). Run the same prompt
  against Nova Micro and Nova Lite and compare cost and latency.
- Tag some calls with `--meta lab=28.1.5 --meta owner=<you>`
  (`requestMetadata`). Read [Per-request metadata
  tagging](https://docs.aws.amazon.com/bedrock/latest/userguide/cost-mgmt-request-metadata.html):
  where do these tags show up, and where don't they?
- Open the `AWS/Bedrock` namespace in CloudWatch and graph
  `Invocations`, `InputTokenCount` and `OutputTokenCount` by `ModelId` for
  the last hour. See [CloudWatch
  metrics](https://docs.aws.amazon.com/bedrock/latest/userguide/monitoring-runtime-metrics.html).
- Read [Create an application inference
  profile](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-create.html)
  and [Best practices for cost
  attribution](https://docs.aws.amazon.com/bedrock/latest/userguide/cost-mgmt-best-practices.html).
  Optional: create an application inference profile for Nova Lite with
  your `owner` tag, call through it, and look for it in Cost Explorer
  tomorrow.
- Read [Service tiers](https://docs.aws.amazon.com/bedrock/latest/userguide/service-tiers-inference.html),
  [Prompt caching](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html)
  and [Batch
  inference](https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference.html).
  Which of them does Nova Lite support?

##### Question: The cheapest correct model

_Your team wants to summarise 50,000 support tickets a day, about 800
input and 150 output tokens each. Estimate the monthly cost on Nova Micro,
Nova Lite and Claude Haiku 4.5, with and without batch inference. What
would make you pay for the most expensive one?_

### Retrospective 28.1

#### Question: What a foundation model is

_Using what you saw in this lesson, explain in your own words: a
foundation model, a token, a context window, an inference parameter and
an inference profile. Then say which AIF-C01 task statements this lesson
covered and which parts of Domain 1 (classical ML, the ML lifecycle) you
still need to study elsewhere._

## Lesson 28.2: Prompt engineering

### Principle 28.2

*The prompt is the program. Make it explicit, give it examples, constrain
its output, and measure every change against a fixed test set, because a
prompt that reads better isn't necessarily one that works better.*

### Practice 28.2

The same model gives very different answers depending on the system
prompt, the instructions, the examples and the format you ask for. These
labs classify the support tickets in
[starter/tickets.jsonl](starter/tickets.jsonl) into five labels (billing,
shipping, returns, account, other). Some tickets are deliberately
ambiguous; one contains personal data; one tries to hijack the prompt.
[starter/eval_prompts.py](starter/eval_prompts.py) runs each prompt
variant you write against the set and reports accuracy and tokens.

Read [Prompt engineering
concepts](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-engineering-guidelines.html)
and the prompting guidance for Amazon Nova linked from it.

#### Lab 28.2.1: Zero-shot, few-shot and the system prompt

Create a `prompts/` directory next to your answers and write one variant
per file, in the format described at the top of `eval_prompts.py`:

- `1-zero-shot.txt`: instruction and ticket only, no system prompt.
- `2-system.txt`: the same, with a system prompt that defines the role and
  **what each label means**.
- `3-few-shot.txt`: the system prompt plus three to five labelled
  examples. Don't use tickets from the test set as examples; write new
  ones.
- `4-reasoning.txt`: ask the model to think briefly before giving the
  label, and to put the label on the last line.

Run them with `--limit 5` first, then on the full set.

##### Question: Which change mattered

_Which single change gave the biggest improvement in accuracy? Which
cost the most extra tokens? Was the reasoning variant worth it for this
task?_

#### Lab 28.2.2: Output you can parse

- Change your best variant so the model answers with JSON only:
  `{"label": ..., "confidence": ..., "reason": ...}`. Delimit the ticket
  clearly (for example with XML-style tags) so the model can't confuse the
  ticket with your instructions.
- Rewrite `parse_label()` in your copy of `eval_prompts.py` to parse the
  JSON, reject any label not in `LABELS`, and count replies that aren't
  valid JSON instead of crashing.
- Look at the Converse `outputConfig` field in the [API
  reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html)
  and the "Structured outputs" row on each model's page. Does Nova Lite
  support it? What would it change about your parser if it did?

##### Question: Never trust the reply

_Ticket `t21` tells the model to ignore its instructions. What did each of
your variants do with it? Your parser rejects labels outside the list;
what else in a real application could an injected ticket do that a strict
parser wouldn't stop? (Lesson 28.7 comes back to this.)_

#### Lab 28.2.3: Measure, don't admire

- Run your best two variants with `--repeat 3` at temperature 0. Do the
  results change between runs? Which tickets flip?
- Run your best variant on `us.amazon.nova-micro-v1:0` and on
  `amazon.nova-lite-v1:0`. Compute accuracy, total tokens and the cost per
  1,000 tickets for each.
- Read [Evaluate the performance of Amazon Bedrock
  resources](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html).
  Find the difference between automatic evaluation with built-in metrics,
  LLM-as-a-judge, and human evaluation, and what each costs.
- Read [Prompt
  management](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management.html).
  Where would you keep the winning prompt so that changing it doesn't need
  a code deployment, and how would you version it?

##### Question: The test set is the spec

_Twenty-four tickets is a tiny test set. What's the smallest change in
accuracy you could trust with it? How would you grow the set, and who
should decide the right label for an ambiguous ticket such as `t22` or
`t24`?_

##### Question: Prompt engineering, fine-tuning or RAG

_AIF-C01 asks when to use prompt engineering, retrieval-augmented
generation, fine-tuning or continued pre-training. Read [Customize your
model](https://docs.aws.amazon.com/bedrock/latest/userguide/custom-models.html).
For each of these, say which you'd reach for first and why: (a) the model
mislabels tickets about a product line it has never heard of; (b) answers
must quote this week's returns policy; (c) replies must follow your
company's tone of voice in every language._

### Retrospective 28.2

#### Question: Prompt risks

_AIF-C01 names four prompt risks: exposure, poisoning, hijacking and
jailbreaking. Define each, and say where prompt injection fits. Which of
them could a customer attempt through a support ticket, and which need
access to something else (the training data, a document store, the system
prompt)?_

## Lesson 28.3: Retrieval-augmented generation with Knowledge Bases

### Principle 28.3

*Don't retrain a model to teach it your documents. Retrieve the relevant
passages at question time and give them to the model with the question.
The quality of the answer is capped by the quality of the retrieval.*

### Practice 28.3

A **knowledge base** turns documents into **chunks**, turns each chunk
into an **embedding** (a vector of numbers that captures its meaning),
and stores the vectors in a **vector store**. At question time it embeds
the question, finds the nearest chunks, and optionally hands them to a
model to write the answer with citations. You'll do the embedding by hand
first, then build a knowledge base on S3 Vectors, the cheapest vector store
Bedrock supports, over the policy documents in
[starter/corpus/](starter/corpus/).

Read [How Amazon Bedrock knowledge bases
work](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-how-it-works.html).

#### Lab 28.3.1: Embeddings by hand

- Read [Amazon Titan Text Embeddings
  models](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html).
- Write `embed.py`: call `invoke_model` on `amazon.titan-embed-text-v2:0`
  with 512 dimensions and normalization on, for five sentences: two about
  returning boots, one about shipping to a PO box, one about passwords,
  and one about the weather.
- Compute the cosine similarity of every pair (with normalized vectors it's
  a dot product; no NumPy needed). Which pairs are closest?
- Embed the question "can I send back shoes that don't fit?". Which
  sentence is nearest, even though it shares almost no words with it?

##### Question: Dimensions

_Titan Text Embeddings V2 offers 256, 512 or 1,024 dimensions. What do
more dimensions cost you in storage and query price on S3 Vectors, and
what might they buy you? Why must the index's dimension match the
embedding model's exactly?_

#### Lab 28.3.2: A knowledge base on S3 Vectors

- Read [Prerequisites for using a vector store you created for a knowledge
  base](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-setup.html)
  (the Amazon S3 Vectors tab), [Working with S3
  Vectors](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors.html)
  and [Create a service role for Knowledge
  Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-permissions.html).
- Copy [starter/knowledge-base.yaml](starter/knowledge-base.yaml) and
  finish its `TODO(student)` items: the service role's S3 read
  permissions, and an `AWS::Bedrock::DataSource` for the document bucket.
- Check it with `cfn-lint`, then deploy it as `<you>-kb`.
- Upload every file in `starter/corpus/` **except `partner-faq.txt`** to
  the document bucket. (That one is for Lab 28.7.3.)
- With the CLI, look at what you built: `aws s3vectors get-index` and
  `aws bedrock-agent get-knowledge-base`.

##### Question: The service role

_The knowledge base's role can invoke one embedding model, read one bucket
and write one vector index. Which principal assumes it, and what do the
`aws:SourceAccount` and `aws:SourceArn` conditions in its trust policy
prevent? Why does the index keep `AMAZON_BEDROCK_TEXT` and
`AMAZON_BEDROCK_METADATA` as non-filterable metadata?_

#### Lab 28.3.3: Ingest, retrieve, generate

- Start an ingestion job with `aws bedrock-agent start-ingestion-job` and
  poll `get-ingestion-job` until it finishes. How many documents were
  scanned and indexed, and how many vectors did that make (`aws s3vectors
  list-vectors`)? Read [Sync your
  data](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-data-source-sync-ingest.html).
- **Retrieve only:** `aws bedrock-agent-runtime retrieve` with "How long
  do I have to return unworn boots?". Read the chunks and their scores.
- **Retrieve and generate:** `aws bedrock-agent-runtime
  retrieve-and-generate` with the same question and Nova Lite as the model.
  Find the citations in the response and match each sentence of the answer
  to a chunk.
- Ask something the corpus doesn't answer ("Do you price-match
  competitors?"). What does the model do? Ask something the corpus answers
  only partly ("Can I return a damaged tent after two years?").
- Read [Query a knowledge base and retrieve
  data](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-test-retrieve.html)
  and [Configure and customize queries and response
  generation](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-test-config.html).
  Change the number of results, and try a metadata filter.

##### Question: Retrieve or RetrieveAndGenerate

_When would an application call `Retrieve` and then Converse itself,
rather than `RetrieveAndGenerate`? Think about prompt control, guardrails,
model choice, streaming and cost. Which IAM actions does each need?_

##### Question: Who may see which document

_Your corpus is public policy. Suppose it also held HR documents that only
some users may read. The knowledge base doesn't know who is asking. Where
would you enforce document-level access, and why is "tell the model not to
reveal HR documents" not an answer?_

#### Lab 28.3.4: Chunking and choosing a vector store

- Read [How content chunking works for knowledge
  bases](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking.html).
- Change the data source's chunking strategy (for example from default to
  fixed-size with small chunks and overlap, or to hierarchical), update the
  stack, re-ingest and repeat the questions from Lab 28.3.3. Some chunking
  settings can't be changed on an existing data source: find out which, and
  what that means for your stack update.
- Fill in this comparison for your answers, from the docs and pricing
  pages linked in [Cost and cleanup](#cost-and-cleanup): S3 Vectors,
  Aurora PostgreSQL Serverless v2, OpenSearch Serverless (classic and
  NextGen), and the Managed Knowledge Base. Columns: minimum monthly cost
  when idle, hybrid (keyword plus semantic) search, metadata filtering,
  query latency, available in `us-east-2`.
- Read [Scale to zero for OpenSearch
  Serverless](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-scale-to-zero.html),
  [Quick create an Aurora PostgreSQL Knowledge
  Base](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.quickcreatekb.html)
  and [Build a managed knowledge
  base](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-build-managed.html).

##### Question: The expensive default

_A colleague builds a proof of concept with the console's quick-create and
leaves it for a month. Which vector store choice turns that into a bill of
hundreds of dollars, and why? What would you put in place so it can't
happen silently in the lab account (think module 00 and module 19)?_

### Retrospective 28.3

#### Question: When RAG isn't the answer

_RAG adds a retrieval step, a vector store and more input tokens to every
question. Give one use case where RAG is the right choice, one where a
longer prompt with the whole document is simpler, and one where
fine-tuning is better. How does the model's context window change the
answer?_

## Lesson 28.4: Guardrails

### Principle 28.4

*A guardrail is a policy that sits outside the model and checks what goes
in and what comes out. Treat it like any other security control: write it
as code, test it with inputs that should pass and inputs that should fail,
and don't assume it catches everything.*

### Practice 28.4

Amazon Bedrock Guardrails evaluates text (and images) against the
policies you configure: **content filters** (hate, insults, sexual,
violence, misconduct, and **prompt attacks**), **denied topics**, **word
filters**, **sensitive information filters** (PII entities and your own
regular expressions, blocked or masked), **contextual grounding** checks
for RAG answers, and **Automated Reasoning** checks. You can attach a
guardrail to a Converse call, or call it on its own with
**`ApplyGuardrail`**, which needs no model at all.

Read [Detect and filter harmful content by using Amazon Bedrock
Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)
and [Safeguard
tiers](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-tiers.html).

#### Lab 28.4.1: A guardrail in CloudFormation

Write `guardrail.yaml` with an
[AWS::Bedrock::Guardrail](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-bedrock-guardrail.html)
named `<you>-guardrail` and an
[AWS::Bedrock::GuardrailVersion](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-bedrock-guardrailversion.html).
Use the **Classic** tier for now. For the shop's support assistant it
should:

- filter all content categories on input and output at a strength you can
  justify, and filter **prompt attacks** on input (read [Detect prompt
  attacks](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-prompt-attack.html)
  for the output setting it requires);
- deny one topic the shop must never discuss, for example medical advice
  about altitude sickness or investment advice, with a definition and a few
  example phrases ([Denied
  topics](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-denied-topics.html));
- block profanity with the managed word list and one custom word, such as
  a competitor's name;
- **mask** email addresses and phone numbers, and **block** payment card
  numbers and US Social Security numbers ([Sensitive information
  filters](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-sensitive-filters.html)),
  plus one regular expression of your own (the shop's order IDs look like
  `A1001`);
- check **contextual grounding** and relevance with thresholds you choose;
- return blocked-input and blocked-output messages that tell a customer
  what happened without revealing the policy.

Deploy it, then note the guardrail ID and version from the stack outputs
(not in your repository).

##### Question: Classic or Standard

_What does the Standard tier add, and what does it require that brings
back the SCP issue from Lab 28.1.4? Read [Distribute guardrail inference
across AWS
Regions](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-cross-region.html).
Which tier would you choose for a shop whose customers write in Spanish and
Portuguese?_

#### Lab 28.4.2: Test it without a model

- Read [Use the ApplyGuardrail API in your
  application](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-use-independent-api.html).
- With `aws bedrock-runtime apply-guardrail`, test at least these as
  `INPUT`, and record the `action` and the assessment that fired:
  - ticket `t09` (an email address and a phone number);
  - ticket `t21` (the injection attempt);
  - a message containing a test card number (use a documented test number
    such as `4111 1111 1111 1111`);
  - a question on your denied topic, and one near it that should pass;
  - an order ID.
- Test one model-style answer as `OUTPUT`, and compare masking with
  blocking.
- Now attach the guardrail to a real call with
  `converse.py --guardrail-id ... --guardrail-version ... --show-trace`.
  What is the `stopReason` when the guardrail intervenes? Did you pay for
  model tokens on a blocked **input**?
- Read [Include a guardrail with the Converse
  API](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-use-converse-api.html)
  and [Apply tags to user
  input](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-tagging.html).
  Change one call so that only the user's text is in a `guardContent`
  block, not your system prompt or examples.

##### Question: Probabilistic and deterministic filters

_Which of your policies are deterministic (the same input always gives
the same result) and which are probabilistic? Which of your tests would
you expect to flip between runs? What does that mean for a guardrail you
rely on for compliance?_

##### Question: What a guardrail costs

_Using the text-unit prices in [Cost and cleanup](#cost-and-cleanup),
what does checking one 2,500-character input with your guardrail cost? Why
might you send only the user's message through the guardrail instead of
the whole prompt?_

#### Lab 28.4.3: Contextual grounding

- Read [Use contextual grounding check to filter hallucinations in
  responses](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-contextual-grounding-check.html).
- With `apply-guardrail`, send a `grounding_source` (a chunk you retrieved
  in Lab 28.3.3), a `query` and a `guard_content` answer. Try an answer that
  is faithful to the source, one that adds a made-up detail ("returns are
  free for 90 days"), and one that is faithful but doesn't answer the
  question. Record both scores for each.
- Add the guardrail to a `retrieve-and-generate` call and ask the
  questions from Lab 28.3.3 again.

##### Question: Grounded is not true

_Contextual grounding checks the answer against the retrieved source.
What happens if the source itself is wrong or malicious? Keep your answer:
you'll test it in Lab 28.7.3._

#### Lab 28.4.4: Make the guardrail mandatory

A guardrail only protects the calls that use it. Two ways to require one:

- **IAM.** Read [Enforce the use of specific guardrails in model inference
  requests](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-permissions-id.html).
  You'll build this into the invoker role in Lab 28.7.1. For now, note
  which API calls the documented limitations say will break under it.
- **Enforcement.** Read [Apply cross-account safeguards with Guardrails
  enforcements](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-enforcements.html)
  and [Amazon Bedrock policies in AWS
  Organizations](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_bedrock.html).
  Don't turn on enforcement in the lab account: it applies to **every**
  model call, including your embedding calls, and bills for each check.
  Answer the questions instead.

##### Question: Three layers

_An organization-level enforced guardrail, an account-level one, and the
guardrail in the request can all apply to one call. How are they combined?
Which one can a developer bypass with input tags, and which setting stops
that? Which policy type can't be used in an enforced guardrail?_

### Retrospective 28.4

#### Question: Guardrails and responsible AI

_AIF-C01 Domain 4 lists features of responsible AI: bias, fairness,
inclusivity, robustness, safety, veracity. Which of them can a guardrail
help with, and which need something else, such as evaluation, a human
review step, or better data? Give one example of each._

## Lesson 28.5: Agents and tools

### Principle 28.5

*An agent is a loop: the model chooses a tool, something runs it, the
result goes back to the model, and it repeats until the model is done.
The tools' permissions are the agent's permissions, so design them as if
an attacker could choose the arguments.*

### Practice 28.5

With **tool use** (function calling), the model doesn't run anything
itself. It replies with `stopReason` `tool_use` and a structured request:
"call `lookup_order` with `{"order_id": "A1002"}`". Your code decides
whether to run it, runs it, and sends the result back. You'll write that
loop by hand first, then add a human approval step for the one tool with a
side effect. Then you'll look at the managed options: Bedrock Agents
Classic, now closed to new customers, and the **Amazon Bedrock AgentCore
harness**, which runs the loop for you in an isolated microVM per session.

Read [Use a tool to complete a model
response](https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html).

#### Lab 28.5.1: The agent loop by hand

- Read [starter/agent_loop.py](starter/agent_loop.py). The tools, their
  schemas and the loop are there; the step that runs a tool and sends back
  the result isn't.
- Complete the `TODO(student)` for Lab 28.5.1.
- Ask: "Where is order A1001?", "What's your returns policy?", and
  "Check orders A1001, A1002 and A1003." Watch the turns and the token
  count grow.
- Ask about an order that doesn't exist, and send a malformed request
  ("Look up order `; DROP TABLE orders`"). What reaches your tool?
- Run a question with `--max-turns 1`. Why does every agent loop need a
  limit?

##### Question: Where the tokens go

_Why does the input token count grow on every turn even when your
question is short? What does the tool list itself cost on each call? What
would that mean for an agent with fifty tools?_

#### Lab 28.5.2: A human in the loop

- Ask: "Order A1002 arrived broken. I want my money back." With the
  starter code as it is, the model can call `issue_refund` and the refund
  happens.
- Complete the `TODO(student)` in `issue_refund()`: require a human to
  approve every refund, cap the amount the tool will refund without a
  second approval, and return a clear result when the human says no.
- Try to talk the agent into refunding an order that isn't delivered, or
  refunding twice. What stopped it: the model, the system prompt, or your
  code?

##### Question: Excessive agency

_The OWASP Top 10 for LLM Applications calls this risk "excessive
agency". Name three ways to limit it in this agent (think about which
tools exist, what each tool may do, and who confirms). Which of them still
work if the model is completely fooled by a prompt injection?_

#### Lab 28.5.3: Bedrock Agents Classic, on paper

- Read [Amazon Bedrock Agents Classic maintenance
  mode](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-classic-maintenance-mode.html)
  and the overview of [Bedrock
  Agents](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)
  (action groups, knowledge bases, aliases, traces).
- Don't try to create one. Your lab account is new, so `CreateAgent` would
  fail, and you'd learn nothing the page doesn't tell you.

##### Question: Classic and its replacement

_What happened on 2026-07-30, and which accounts can still create agents?
Map each Agents Classic feature (action groups, knowledge base
association, return of control, prompt overrides, multi-agent
collaboration) to its AgentCore equivalent. Which one has no direct
equivalent in the harness? Why do exam questions written before 2026
still mention Bedrock Agents?_

#### Lab 28.5.4: The same agent on an AgentCore harness

The AgentCore harness is a managed agent loop: you declare the model,
system prompt and tools; AgentCore runs each session in its own microVM,
with memory, tracing and identity. Tools can be MCP servers, AgentCore
Gateway targets, the built-in browser and code interpreter, or **inline
functions** that pause the loop and hand the call back to your code, which
is how you'll keep the refund approval on your side.

- Read [AgentCore harness](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness.html),
  [Get started](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-get-started.html),
  [Tools](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-tools.html),
  [Observability and cost
  controls](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-operations.html)
  and [Security and access
  controls](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-security.html).
  Confirm in [Supported AWS
  Regions](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-regions.html)
  that the harness is available in `us-east-2`.
- Write `harness-role.yaml`: an execution role that
  `bedrock-agentcore.amazonaws.com` can assume, starting from the sample
  execution role policy but **scoped down**: invoke only the model you
  choose (in-Region Nova Lite, or the US Nova Micro profile and its
  destination models), write only to the AgentCore log groups, and drop the
  browser and code interpreter statements you won't use.
- Create the harness with `aws bedrock-agentcore-control create-harness`
  (or an `AWS::BedrockAgentCore::Harness` in the same template). Set:
  - `--model` explicitly to Nova Lite (a `bedrockModelConfig` with its
    `modelId`; see
    [CreateHarness](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_CreateHarness.html));
  - `--system-prompt` from `agent_loop.py`;
  - `--allowed-tools` so the built-in `shell` and `file_operations` tools
    **aren't** available;
  - `--memory` disabled, unless you want to test memory (it's on by
    default and billed per event);
  - `--max-iterations`, `--max-tokens` and `--timeout-seconds` small
    enough that a runaway loop costs cents.
- Poll `get-harness` until its status is `READY`.
- Write `harness_client.py`: define `lookup_order` and `issue_refund` as
  **inline function** tools, call
  [InvokeHarness](https://docs.aws.amazon.com/bedrock-agentcore/latest/APIReference/API_InvokeHarness.html)
  with a session ID, read the event stream, and when `stopReason` is
  `tool_use`, run the function locally (with your approval step for
  refunds) and send back the `toolUse` and `toolResult` messages. Reuse
  your functions from `agent_loop.py`.
- Ask the questions from Lab 28.5.1 again. Read the token usage from the
  `metadata` events.
- Turn on traces ([Get started with AgentCore
  Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-get-started.html);
  it needs CloudWatch Transaction Search once per account) and find one
  session's model calls and tool calls in CloudWatch.
- Leave the harness in place until Lab 28.7.5, or delete it now with
  `delete-harness` if you'll take a break of more than a day.

<!-- VERIFY: that an allowedTools list naming only the inline functions
hides the built-in shell and file_operations tools (the docs say "if
omitted, all tools are allowed" but don't show the exclusion case). -->

##### Question: Harness or runtime

_Read [AgentCore harness vs.
Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-vs-runtime.html).
When would you deploy your own agent code (for example with Strands Agents
or LangGraph) on AgentCore Runtime instead of using the harness? What do
you give up?_

##### Question: Who can call the agent

_Invoking a harness needs two IAM actions on the harness ARN. Which? The
harness also exposes `InvokeAgentRuntimeCommand`, which runs commands in
the session's microVM without going through the model. Why does the
documentation tell you not to grant it, and does `allowedTools` protect
you from it?_

##### Question: Gateway and Policy

_Read [AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)
and [Policy in AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html).
If `issue_refund` were a Lambda function behind a gateway instead of an
inline function, how would you stop the agent refunding more than $500
without a human, using Policy rather than code in the function?_

### Retrospective 28.5

#### Question: Loop, harness or workflow

_You built the same agent twice. Compare the hand-written loop and the
harness for cost, security boundary, observability, and how much code you
own. When would a fixed Step Functions workflow (module 18) that calls a
model at one step be better than an agent that decides its own steps?_

## Lesson 28.6: AI coding assistants

### Principle 28.6

*An AI coding assistant is a fast, tireless collaborator that runs with
your credentials. Give it the least access it needs, tell it your rules in
writing, and review everything it changes before you commit it.*

### Practice 28.6

AWS's coding assistant has changed name and shape more than once. In
2026, **Kiro** is the agentic IDE and CLI (spec-driven development,
steering files, hooks and MCP), and it is the successor to the **Amazon Q
Developer** IDE plugins. Q Developer in the AWS console and in chat
applications carries on. The CloudOps exam guide names Kiro; older
practice questions name Q Developer. This lesson is mostly reading, with
one optional lab.

#### Lab 28.6.1: Amazon Q Developer and Kiro in 2026

- Read [Amazon Q Developer end-of-support
  announcement](https://aws.amazon.com/blogs/devops/amazon-q-developer-end-of-support-announcement/)
  and [What is Amazon Q
  Developer?](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/what-is.html).
- Read the Kiro docs on [specs](https://kiro.dev/docs/specs/),
  [steering](https://kiro.dev/docs/steering/),
  [hooks](https://kiro.dev/docs/hooks/), [MCP](https://kiro.dev/docs/mcp/)
  and [privacy and security](https://kiro.dev/docs/privacy-and-security/),
  and the [pricing page](https://kiro.dev/pricing/).

##### Question: What happens to Q Developer

_Write down the three dates in the Q Developer announcement and what each
changes. Which Q Developer features are **not** affected? If a CloudOps
exam question asks for "an AI assistant to help investigate an
operational issue", which products might the answer name?_

##### Question: Your code, their service

_What does Kiro's privacy page say about whether your content can be used
to improve the service, and how do you opt out? How do the answers differ
between the free tier and a paid subscription managed through IAM
Identity Center? Why does that matter for a client's code?_
<!-- VERIFY: Kiro's current data-use and opt-out terms per plan; they have
changed since launch. -->

#### Lab 28.6.2: Steer an assistant with the course rules (optional)

Only if you want to try Kiro on its free plan. Any assistant with project
rules works the same way.

- Open your copy of this module's directory as a project. Write a
  steering file in `.kiro/steering/` with this course's rules:
  CloudFormation in YAML that passes `cfn-lint`; Region from the profile,
  never hard-coded; no account IDs, ARNs with account IDs, emails or
  credentials in any file; Python 3.13 with boto3; resource names start
  with your identifier.
- Ask it to finish one piece of **your** work you've already designed, for
  example the `estimate_cost()` function in `converse.py` or the data source
  in `knowledge-base.yaml`, using a spec so you see its requirements,
  design and task list before it writes code.
- Review the diff line by line. Run `cfn-lint` and `python -m py_compile`
  yourself. Commit only what you understand and would have written.
- Check which terminal profile and credentials the assistant used when it
  ran commands. Make sure it was `lab`, never `mgmt`.

##### Question: Prompt injection through your repository

_An assistant reads files in your project to build its context. What
could `starter/corpus/partner-faq.txt` do to an assistant that reads it,
and what could an assistant with shell access and your `lab` credentials
do next? List three settings or habits that limit the damage._

### Retrospective 28.6

#### Question: What you still own

_The exams talk about AI assistants that generate code, explain it, scan
it for vulnerabilities and upgrade it. For each, what is still your
responsibility under the shared responsibility model? Would you let an
assistant apply CloudFormation changes to a production account? Under
what controls?_

## Lesson 28.7: Securing generative AI workloads

### Principle 28.7

*Treat the model as an untrusted component. Control who can call which
model, what the model's output is allowed to reach, what gets logged, and
where your data travels; a well-written system prompt is not a security
boundary.*

### Practice 28.7

The security controls for generative AI are mostly the ones you already
know, pointed at new resources: IAM for model invocation, Organizations
policies, logging, encryption and private networking. What's new is that
the input is natural language, so instructions can hide in data, and that
the output may be acted on by code. These labs build a least-privilege
role, log every invocation, attack your own knowledge base with an
indirect prompt injection, and trace where a prompt goes.

Read the [OWASP Top 10 for LLM
Applications](https://genai.owasp.org/llm-top-10/) (SCS-C03 names it) and
the security pillar of the [Generative AI
Lens](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html).

#### Lab 28.7.1: A least-privilege invoker role

Write `invoker-role.yaml` with a role, `<you>-invoker`, that your own
`lab` session can assume (trust your account and require your Identity
Center role, as in module 03), and an inline policy that:

- allows `bedrock:InvokeModel` (Converse's action) on the in-Region Nova
  Lite foundation model only;
- allows the US Nova Micro inference profile and the Nova Micro foundation
  model in each of its destination Regions, the latter **only** through
  that profile (`bedrock:InferenceProfileArn`), following [Geographic
  cross-Region
  inference](https://docs.aws.amazon.com/bedrock/latest/userguide/geographic-cross-region-inference.html);
- requires your guardrail from Lesson 28.4 on every inference call, with
  `bedrock:GuardrailIdentifier` and an explicit `Deny`, and allows
  `bedrock:ApplyGuardrail` on it;
- denies the use of Bedrock API keys (`bedrock:CallWithBearerToken`), as in
  [API keys](https://docs.aws.amazon.com/bedrock/latest/userguide/api-keys.html).

Build every ARN with pseudo-parameters. Validate the policy with IAM Access
Analyzer, deploy, assume the role with a CLI profile (`role_arn` and
`source_profile = lab`), then test:

- Positive: `converse.py` on Nova Lite **with** the guardrail.
- Negative: the same call without the guardrail.
- Negative: `us.amazon.nova-2-lite-v1:0`, or any other model.
- Negative: `retrieve-and-generate` against your knowledge base. Is that
  the result you wanted?

##### Question: API keys

_A Bedrock long-term API key is a service-specific credential on an IAM
user that the console creates for you. Compare it with a short-term key
and with your SigV4 session credentials: lifetime, what it can do, how
you'd revoke it, and what CloudTrail records. Write the SCP statement
you'd attach to the `Sandbox` OU so nobody in the lab account can create
or use a long-term key._

##### Question: Model allowlists at scale

_Your role names two models. How would you restrict an entire
organization to an approved list of models, and still allow new approved
models without editing every role? Consider SCPs, `aws-marketplace`
permissions, application inference profiles and [How Amazon Bedrock
works with
IAM](https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_service-with-iam.html)._

#### Lab 28.7.2: Log every model invocation

- Read [Monitor model invocation using CloudWatch Logs and Amazon
  S3](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html).
- Create a log group `/stelligent-u/<you>/bedrock-invocations` with 7-day
  retention, and a role that Bedrock can assume to write to it (trust
  `bedrock.amazonaws.com` with `aws:SourceAccount` and `aws:SourceArn`
  conditions). Put both in a small template.
- Turn on text logging with `aws bedrock
  put-model-invocation-logging-configuration`. It is per Region and per
  account.
- Make a few calls: `converse.py` with `--meta` tags, one RAG query, and
  ticket `t09` with and without the guardrail.
- Query the log group with Logs Insights: tokens by principal
  (`identity.arn`), and tokens by one of your `requestMetadata` keys.
- Read the entry for `t09`. Is the email address in the log? With the
  guardrail masking it?
- Compare with CloudTrail: find the same Converse call in Event history
  and list what each record has that the other doesn't. Read [Monitor
  Amazon Bedrock API calls using
  CloudTrail](https://docs.aws.amazon.com/bedrock/latest/userguide/logging-using-cloudtrail.html)
  to find which Bedrock calls are data events that a default trail
  doesn't record.

##### Question: The log is now the sensitive data

_Invocation logs contain every prompt and answer, including anything
customers typed. Which controls from modules 08, 10 and 19 would you put
on the log group or bucket: retention, KMS, access, where the logs live?
Who in your organization should be able to read them? Why might you log
metadata only for one application and full text for another?_

##### Question: Auditing an assistant

_The CloudOps exam describes a company that must produce an audit report
of who used a Bedrock assistant, how much, which knowledge bases it read,
and with which parameters. Which of CloudTrail management events, CloudTrail
data events, model invocation logs and CloudWatch metrics answers each
part?_

#### Lab 28.7.3: Indirect prompt injection

The attacker doesn't talk to your assistant. They put instructions in a
document it will read.

- Read [starter/corpus/partner-faq.txt](starter/corpus/partner-faq.txt).
  Upload it to your document bucket and re-sync the knowledge base.
- Ask with `retrieve-and-generate`, without a guardrail: "How long do I
  have to return boots?" and "How do I get my refund faster?". Run each a
  few times. Did the poisoned instructions reach the answer?
- Repeat with your guardrail. Which policy, if any, fired: prompt attack,
  sensitive information, denied topic, contextual grounding?
- Try to make the defence work. Options include: a denied topic for
  requests for payment details; an output check for the fraudulent email
  address; the prompt attack filter applied to retrieved content by
  calling `Retrieve` and `ApplyGuardrail` yourself before generation; a
  system prompt that marks retrieved text as data, not instructions; and
  removing the document at the source. Record what worked, what didn't,
  and at what cost.
- Remove `partner-faq.txt` from the bucket and re-sync. Confirm with
  `retrieve` that its chunks are gone.

##### Question: Where to stop it

_Map this attack to the OWASP Top 10 for LLM Applications entries it
touches. Which control stopped it most reliably, and which one only made
it less likely? Why didn't contextual grounding help? In a real system,
who should be allowed to add documents to a knowledge base, and how would
you review what they add?_

#### Lab 28.7.4: Where your data goes

- Read [Data protection](https://docs.aws.amazon.com/bedrock/latest/userguide/data-protection.html),
  [Amazon Bedrock abuse
  detection](https://docs.aws.amazon.com/bedrock/latest/userguide/abuse-detection.html)
  and [Protect your data using Amazon VPC and AWS
  PrivateLink](https://docs.aws.amazon.com/bedrock/latest/userguide/usingVPC.html).
- Trace one `retrieve-and-generate` call through the US geographic
  profile: which Regions and services see the question, the retrieved
  chunks and the answer? Where is anything stored, by whom, for how long,
  and encrypted with which key? Draw it.

<!-- VERIFY: the current wording of Bedrock's statement that prompts and
completions are not used to train AWS or third-party models and are not
shared with model providers; quote it in the answer from the Bedrock FAQ
or data protection pages. -->

##### Question: The shared responsibility model for GenAI

_For a RAG assistant on Bedrock, list what AWS is responsible for and what
you are: the model weights, the model provider's access, your prompts and
logs, the knowledge base contents, the guardrail configuration, IAM, and
the network path. Which of your responsibilities did this module leave
undone for a production system?_

#### Lab 28.7.5: Clean up the module

Delete in this order, in `us-east-2`, and check each step:

- **Harness:** `aws bedrock-agentcore-control delete-harness`, then
  confirm with `list-harnesses`. Check that the managed memory it created
  is gone too, and delete the `harness-role` stack.
- **Knowledge base:** empty the document bucket, then delete the `<you>-kb`
  stack. Confirm with `aws bedrock-agent list-knowledge-bases` and
  `aws s3vectors list-vector-buckets`. If the vector bucket survives
  because it isn't empty, delete its index first.
  <!-- VERIFY: whether deleting an AWS::S3Vectors::Index through
  CloudFormation deletes the vectors in it, so the vector bucket can then
  be deleted. -->
- **Guardrail:** delete the guardrail stack. (A guardrail used by an
  enforcement configuration can't be deleted; you didn't create one.)
- **Invocation logging:** `aws bedrock
  delete-model-invocation-logging-configuration`, then delete the log
  group and its role. Check `get-model-invocation-logging-configuration`
  returns nothing.
- **Roles:** delete the `invoker-role` stack and remove the CLI profile
  that assumed it.
- **Log groups:** delete leftovers under `/aws/bedrock-agentcore/` and any
  other log group this module created
  (`aws logs describe-log-groups --log-group-name-prefix`).
- **Application inference profile** (if you made one in Lab 28.1.5):
  `aws bedrock delete-inference-profile`.
- **API keys:** if you created a long-term Bedrock API key to look at it,
  delete the service-specific credential **and** the IAM user the console
  created.
- **SCP:** keep the cross-Region inference exception from Lab 28.1.4
  only if it's limited to the US geographic profiles; otherwise narrow or
  revert it. Write down which you did. Your guardrails from module 19 must
  still pass their tests.
- **Transaction Search:** turn it off again if you don't want it for other
  modules.
- **Check the bill:** tomorrow, look at Cost Explorer grouped by service
  and usage type for Bedrock, S3 Vectors, AgentCore and CloudWatch.
  Explain every non-zero line.

### Retrospective 28.7

#### Question: A security review

_A team asks you to approve their Bedrock-based support assistant for
production. Write the ten questions you'd ask them, covering identity,
model access and Regions, data classification and logging, guardrails,
tools and agency, prompt injection, cost controls and incident response.
For each, say which lab in this module taught you what a good answer looks
like._

## Further Reading

- [Generative AI Lens](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html)
  for the AWS Well-Architected Framework.
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/).
- [The Generative AI Security Scoping
  Matrix](https://aws.amazon.com/ai/generative-ai/security/scoping-matrix/),
  the governance framework AIF-C01 Task 5.2 names.
- [Responsible AI at AWS](https://aws.amazon.com/ai/responsible-ai/), for
  AIF-C01 Domain 4.
- [What is Amazon SageMaker AI?](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html),
  for the classical ML topics in AIF-C01 Domain 1 that this module doesn't
  cover.
- The exam guides for [AIF-C01](https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01.html),
  [SCS-C03](https://docs.aws.amazon.com/aws-certification/latest/security-specialty-03/security-specialty-03.html)
  and [SOA-C03](https://docs.aws.amazon.com/aws-certification/latest/sysops-administrator-associate-03/sysops-administrator-associate-03.html).
- [Monitor Amazon Bedrock Guardrails using CloudWatch
  metrics](https://docs.aws.amazon.com/bedrock/latest/userguide/monitoring-guardrails-cw-metrics.html).
- [Security best practices for AgentCore
  Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-security-best-practices.html),
  if you go on to deploy your own agent code.
- [Identity-based policy examples for Amazon
  Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html).
