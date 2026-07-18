---
title: "Resource Cleanup"
weight: 7
chapter: true
pre: "<b>7. </b>"
---

### Chapter 7

# Clean up resources

Perform cleanup in reverse creation order.

## 1. Disable the schedule

Disable or delete the EventBridge schedule first so it cannot create new invocations.

## 2. Remove AgentCore resources

From `deploy/agentcore/TraderFloor`:

```powershell
agentcore remove all
agentcore deploy
agentcore status
```

## 3. Remove the application layer if created

- CloudFront distribution.
- S3 dashboard bucket after emptying it.
- API Gateway and Lambda.
- Cognito User Pool and App Client.
- Any separate log groups not removed automatically by the stack.

## 4. Delete DynamoDB

```powershell
aws dynamodb delete-table `
  --table-name strands-trader-state `
  --region us-west-2
```

## 5. Verify

- No workshop CloudFormation stacks remain.
- No workshop Runtime or Gateway remains in the AgentCore console.
- No EventBridge schedule remains.
- Cost Explorer shows no new usage after its data refreshes.

{{% notice warning %}}
Deleting the local AgentCore project does not guarantee that manually created resources outside the stack, such as DynamoDB or S3, are deleted. Check every item in the list.
{{% /notice %}}
