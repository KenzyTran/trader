---
title: "Validation"
weight: 6
chapter: true
pre: "<b>6. </b>"
---

### Chapter 6

# Validate the result

Do not consider the deployment complete only because CloudFormation reports success.

## Checklist

### Local quality gate

```powershell
uv run pytest
uv run ruff check src tests
cd frontend
npm run build
```

### Runtime

- `agentcore status` shows the Runtime as ready.
- `agentcore invoke "Warren"` returns exactly one trader.
- `agentcore invoke "all"` returns four traders.
- An unknown trader is rejected with a clear error.

### State

```powershell
aws dynamodb query `
  --table-name strands-trader-state `
  --key-condition-expression "pk = :pk" `
  --expression-attribute-values '{":pk":{"S":"ACCOUNT#warren"}}'
```

There must be an item with `sk=STATE` and items whose `sk` begins with `LOG#`.

### Security

- The Runtime role does not have `AdministratorAccess` when the workshop is complete.
- The policy is scoped to the specific DynamoDB table ARN.
- Git and CloudWatch logs contain no keys or tokens.
- A production Gateway uses a JWT authorizer.

### Observability

- A trace exists for the Runtime invocation.
- Model and tool spans are visible.
- When an invalid payload is sent intentionally, logs explain the cause without exposing secrets.
