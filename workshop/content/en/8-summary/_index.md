---
title: "Summary"
weight: 8
chapter: true
pre: "<b>8. </b>"
---

### Chapter 8

# Workshop summary

You followed the complete path from a local Strands trading workflow to an AgentCore architecture that can run on AWS.

## What you learned

- Separate the LLM proposal from the deterministic risk check and executor.
- Use Amazon Bedrock through Strands `BedrockModel`.
- Use DynamoDB instead of SQLite when `STORAGE_BACKEND=dynamodb`.
- Package `BedrockAgentCoreApp` and deploy it with the AgentCore CLI.
- Place Gateway and Identity at the tool and credential boundary.
- Monitor the Runtime with AgentCore Observability and CloudWatch.
- Distribute the dashboard through S3 and CloudFront and protect the API with Cognito.

## Next development steps

Continue with the same incremental approach:

1. Complete the `TradeProposal` schema.
2. Add the basic validator.
3. Separate the executor.
4. Move the workflow into a Strands Graph.
5. Enable only the position-weight limit.

Do not add more data sources, memory, or risk rules until the current step has tests and has been reviewed.

## References

- [Amazon Bedrock AgentCore — Get started](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-cli.html)
- [AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-get-started-cli.html)
- [AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-quick-start.html)
- [AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html)
- [AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html)
- [Strands Agents](https://strandsagents.com/)
