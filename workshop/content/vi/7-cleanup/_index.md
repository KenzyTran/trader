---
title: "Dọn dẹp tài nguyên"
weight: 7
chapter: true
pre: "<b>7. </b>"
---

### Chương 7

# Dọn dẹp tài nguyên

Thực hiện theo thứ tự ngược với lúc tạo.

## 1. Tắt schedule

Disable hoặc xóa EventBridge schedule trước để không phát sinh invocation mới.

## 2. Xóa AgentCore resources

Từ thư mục `deploy/agentcore/TraderFloor`:

```powershell
agentcore remove all
agentcore deploy
agentcore status
```

## 3. Xóa application layer nếu đã tạo

- CloudFront distribution.
- S3 dashboard bucket sau khi empty.
- API Gateway và Lambda.
- Cognito User Pool/App Client.
- Các log group riêng không được stack xóa tự động.

## 4. Xóa DynamoDB

```powershell
aws dynamodb delete-table `
  --table-name strands-trader-state `
  --region us-west-2
```

## 5. Xác minh

- CloudFormation không còn stack workshop.
- AgentCore console không còn Runtime/Gateway workshop.
- EventBridge không còn schedule.
- Cost Explorer không còn usage mới sau thời gian cập nhật dữ liệu.

{{% notice warning %}}
Xóa AgentCore project local không tự động đảm bảo mọi resource ngoài stack như DynamoDB/S3 do bạn tạo
thủ công đã bị xóa. Hãy kiểm tra từng mục trong checklist.
{{% /notice %}}
