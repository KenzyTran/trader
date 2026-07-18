---
title: "Deploying Strands Trading Agents on AWS"
date: 2026-07-18
weight: 0
---

# Strands Trading Agents on Amazon Bedrock AgentCore

This workshop guides you through moving a four-LLM-trader system from a local environment to AWS in small, incremental steps using **Strands Agents** and **Amazon Bedrock AgentCore Runtime**.

| Information | Details |
|---|---|
| Duration | 120–150 minutes |
| Level | Intermediate |
| Framework | Strands Agents |
| Core infrastructure | Amazon Bedrock AgentCore, Bedrock, DynamoDB |
| User interface | TypeScript/Vite dashboard |
| Mode | Simulation / paper trading |

{{% notice warning %}}
This workshop does not place real-money orders. Third-party APIs and Amazon Bedrock models may incur charges. Complete the **Resource Cleanup** section after the workshop.
{{% /notice %}}

## Learning outcomes

After this workshop, you will be able to:

- Explain the `Trader → Proposal → Risk check → Executor` workflow.
- Run a trading cycle locally with Strands Agents.
- Package and deploy the entrypoint to AgentCore Runtime.
- Use Amazon Bedrock as the model provider and DynamoDB as the state store.
- Inspect traces and logs with AgentCore Observability and CloudWatch.
- Understand where AgentCore Gateway and Identity fit in a production architecture.

## Contents

{{% children depth="1" %}}
