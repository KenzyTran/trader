# Kế hoạch nâng cấp workflow giao dịch

## Mục tiêu hiện tại

Nâng cấp **workflow ra quyết định và thực hiện giao dịch** của các LLM trader theo từng bước nhỏ,
có thể kiểm thử và đánh giá độc lập sau mỗi bước.

Project sẽ không cố gắng giải quyết đồng thời tất cả vấn đề của một hệ thống giao dịch hoàn chỉnh.
Mỗi giai đoạn phải chạy ổn định trước khi bắt đầu giai đoạn kế tiếp.

## Phạm vi

Trong giai đoạn hiện tại, chỉ thay đổi luồng xử lý giao dịch:

```text
Quan sát tài khoản
        ↓
Trader phân tích và đề xuất
        ↓
Kiểm tra đề xuất
        ↓
Phê duyệt hoặc từ chối
        ↓
Thực hiện giao dịch
        ↓
Ghi nhận kết quả
```

Các nguồn dữ liệu và tool hiện có tiếp tục được sử dụng. Không bổ sung nguồn dữ liệu mới khi chưa có
nhu cầu và dữ liệu phù hợp.

## Những phần chưa thực hiện

Các nội dung sau không nằm trong phạm vi nâng cấp trước mắt:

- Nguồn dữ liệu thị trường, fundamentals hoặc filings mới.
- Vector database, knowledge graph hoặc long-term memory.
- Backtest engine hoàn chỉnh.
- Kết nối broker hoặc giao dịch tiền thật.
- Fine-tuning model.
- Hệ thống observability hoặc evaluation quy mô lớn.
- Thay đổi dashboard ngoài những gì workflow mới bắt buộc phải hiển thị.

Chỉ đưa một nội dung trên vào kế hoạch khi workflow hiện tại đã ổn định và có yêu cầu cụ thể.

## Nguyên tắc phát triển

1. Mỗi lần chỉ triển khai một thay đổi nhỏ, có mục tiêu rõ ràng.
2. Không thay đổi hành vi giao dịch hiện tại nếu bước đang làm chưa yêu cầu.
3. Logic tài chính bắt buộc phải viết bằng Python; không giao các giới hạn cứng cho LLM tự diễn giải.
4. LLM đề xuất hành động nhưng không được tự vượt qua bước kiểm tra của workflow.
5. Mọi bước mới phải có test trước khi chuyển sang bước tiếp theo.
6. Giữ chế độ mô phỏng làm mặc định.
7. Không mở rộng dependency hoặc kiến trúc nếu chưa đem lại giá trị cho bước hiện tại.

## Lộ trình từng bước

### Bước 1 — Chuẩn hóa đề xuất giao dịch

Trader chưa gọi `buy_shares` hoặc `sell_shares` trực tiếp. Trader tạo một kết quả có cấu trúc gồm:

- `action`: `buy`, `sell` hoặc `hold`.
- `symbol`.
- `quantity`.
- `rationale`.
- `confidence`.
- `risks`.

Đầu ra được kiểm tra bằng Pydantic. Nếu sai schema, workflow dừng an toàn và không giao dịch.

**Điều kiện hoàn thành:** Có schema, prompt tương ứng và unit test cho dữ liệu hợp lệ/không hợp lệ.

### Bước 2 — Thêm lớp kiểm tra giao dịch

Tạo một `TradeValidator` bằng Python để kiểm tra tối thiểu:

- Số lượng phải lớn hơn 0.
- Mã cổ phiếu không được rỗng.
- Tài khoản đủ tiền khi mua.
- Tài khoản đủ cổ phiếu khi bán.
- `hold` không được tạo order.

Ở bước này chưa thêm các quy tắc quản trị rủi ro nâng cao.

**Điều kiện hoàn thành:** Mọi đề xuất đều phải qua validator; test bao phủ từng lý do từ chối.

### Bước 3 — Tách đề xuất khỏi thực thi

Tạo `TradeExecutor` chỉ nhận đề xuất đã được phê duyệt. Executor gọi nghiệp vụ tài khoản hiện có và trả
về kết quả thực thi có cấu trúc.

Luồng lúc này là:

```text
TraderAgent → TradeProposal → TradeValidator → TradeExecutor
```

**Điều kiện hoàn thành:** Trader không còn quyền truy cập trực tiếp tool mua/bán; test chứng minh proposal
bị từ chối không làm thay đổi tài khoản.

### Bước 4 — Biểu diễn workflow bằng Strands Graph

Sau khi ba bước trên hoạt động ổn định, chuyển luồng sang Strands Graph với các node rõ ràng:

```text
Context → Trader → Validator → Executor → Summary
```

Validator và Executor vẫn là logic deterministic. Không tạo thêm agent nếu một hàm Python là đủ.

**Điều kiện hoàn thành:** Graph cho kết quả tương đương workflow ở Bước 3 và toàn bộ test cũ vẫn pass.

### Bước 5 — Thêm Risk Manager tối thiểu

Chỉ triển khai sau khi Graph ổn định. Risk Manager trước mắt chỉ áp dụng một quy tắc:

- Giới hạn tỷ trọng tối đa cho một vị thế.

Ngưỡng tỷ trọng phải nằm trong config và được kiểm tra bằng code. Tỷ trọng dự kiến sau giao dịch được
tính theo giá trị vị thế chia cho tổng giá trị danh mục. Nếu vượt ngưỡng, proposal bị từ chối và không
được chuyển đến Executor.

**Điều kiện hoàn thành:** Có test cho trường hợp dưới ngưỡng, đúng ngưỡng và vượt ngưỡng; lý do từ chối
được lưu rõ ràng.

## Bước sẽ làm tiếp theo

Chỉ thực hiện **Bước 1 — Chuẩn hóa đề xuất giao dịch**.

Không tự động triển khai Bước 2 hoặc các bước sau trong cùng một thay đổi. Sau khi Bước 1 hoàn tất,
chạy test, xem lại kết quả và chờ quyết định trước khi tiếp tục.

## Tiêu chí chung cho mỗi thay đổi

Một bước được xem là hoàn tất khi:

- Code mới có type hints và trách nhiệm rõ ràng.
- Unit test liên quan đều pass.
- `ruff check src tests` không có lỗi.
- Không làm hỏng `trader api`, Vite dashboard, `trader ui`, `trader once` và `trader run` ngoài thay đổi đã mô tả.
- README được cập nhật nếu cách chạy hoặc cấu hình thay đổi.
- Không chứa secret, dữ liệu runtime hoặc database trong commit.
