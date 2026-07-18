---
title: "Xác minh"
weight: 6
chapter: true
pre: "<b>6. </b>"
---

### Chương 6

# Xác minh kết quả

Không xem deployment là hoàn thành chỉ vì CloudFormation trả về thành công.

## Checklist

### Local quality gate

```powershell
uv run pytest
uv run ruff check src tests
cd frontend
npm run build
```

### Runtime

- `agentcore status` hiển thị Runtime ở trạng thái sẵn sàng.
- `agentcore invoke "Warren"` trả về đúng một trader.
- `agentcore invoke "all"` trả về bốn trader.
- Unknown trader bị từ chối rõ ràng.

### State

```powershell
aws dynamodb query `
  --table-name strands-trader-state `
  --key-condition-expression "pk = :pk" `
  --expression-attribute-values '{":pk":{"S":"ACCOUNT#warren"}}'
```

Phải có item `sk=STATE` và các item `sk` bắt đầu bằng `LOG#`.

### Security

- Runtime role không có `AdministratorAccess` khi kết thúc workshop.
- DynamoDB table ARN được scope cụ thể trong policy.
- Không có key/token trong Git hoặc CloudWatch logs.
- Gateway production sử dụng JWT authorizer.

### Observability

- Có trace cho Runtime invocation.
- Model và tool spans xuất hiện.
- Khi cố ý gửi payload lỗi, log cho biết nguyên nhân nhưng không lộ secret.
