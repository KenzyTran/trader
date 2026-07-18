---
title: "Tổng kết"
weight: 8
chapter: true
pre: "<b>8. </b>"
---

### Chương 8

# Tổng kết Workshop

Bạn đã đi qua toàn bộ đường dẫn từ một Strands trading workflow local đến một kiến trúc AgentCore có thể
vận hành trên AWS.

## Những gì đã học

- Phân tách LLM proposal khỏi deterministic risk check và executor.
- Dùng Amazon Bedrock qua Strands `BedrockModel`.
- Dùng DynamoDB thay SQLite khi `STORAGE_BACKEND=dynamodb`.
- Đóng gói `BedrockAgentCoreApp` và deploy bằng AgentCore CLI.
- Đặt Gateway/Identity ở biên tool và credentials.
- Theo dõi Runtime bằng AgentCore Observability/CloudWatch.
- Phân phối dashboard qua S3/CloudFront và bảo vệ API bằng Cognito.

## Bước phát triển tiếp theo

Giữ nguyên nguyên tắc phát triển từng bước:

1. Hoàn tất `TradeProposal` schema.
2. Thêm validator cơ bản.
3. Tách executor.
4. Đưa workflow vào Strands Graph.
5. Bật duy nhất giới hạn tỷ trọng vị thế.

Không bổ sung thêm data source, memory hoặc risk rule trước khi bước hiện tại có test và đã được review.

## Tài liệu tham khảo

- [Amazon Bedrock AgentCore — Get started](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-cli.html)
- [AgentCore Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-get-started-cli.html)
- [AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-quick-start.html)
- [AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html)
- [AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html)
- [Strands Agents](https://strandsagents.com/)
