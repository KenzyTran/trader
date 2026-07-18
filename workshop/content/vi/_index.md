---
title: "Triển khai Strands Trading Agents trên AWS"
date: 2026-07-18
weight: 0
---

# Strands Trading Agents trên Amazon Bedrock AgentCore

Workshop hướng dẫn đưa hệ thống bốn LLM trader từ môi trường local lên AWS theo từng bước nhỏ, sử dụng
**Strands Agents** và **Amazon Bedrock AgentCore Runtime**.

| Thông tin | Chi tiết |
|---|---|
| Thời lượng | 120–150 phút |
| Cấp độ | Intermediate |
| Framework | Strands Agents |
| Hạ tầng chính | Amazon Bedrock AgentCore, Bedrock, DynamoDB |
| Giao diện | TypeScript/Vite dashboard |
| Chế độ | Simulation / paper trading |

{{% notice warning %}}
Workshop không đặt lệnh tiền thật. Các API bên thứ ba và model Amazon Bedrock có thể phát sinh chi phí.
Hãy hoàn thành phần **Dọn dẹp tài nguyên** sau buổi học.
{{% /notice %}}

## Kết quả đạt được

Sau workshop, bạn có thể:

- Giải thích workflow `Trader → Proposal → Risk check → Executor`.
- Chạy một trading cycle bằng Strands Agents ở local.
- Đóng gói và triển khai entrypoint lên AgentCore Runtime.
- Dùng Amazon Bedrock làm model provider và DynamoDB làm state store.
- Theo dõi trace/log bằng AgentCore Observability và CloudWatch.
- Hiểu vị trí của AgentCore Gateway và Identity trong kiến trúc production.

## Nội dung

{{% children depth="1" %}}
