# Strands Trading Floor

Mô phỏng bốn trader tự động được xây dựng trên Strands Agents. Mỗi agent có chiến lược riêng và dùng
Python tools để nghiên cứu tin tức, xem giá, quản lý tài khoản và gửi kết quả qua Telegram.

Project gồm:

- `src/trader`: workflow Strands, tài khoản, market tools và FastAPI.
- `frontend`: dashboard TypeScript/Vite gốc, sử dụng uPlot.
- `src/trader/ui.py`: dashboard Gradio phụ để kiểm tra nhanh backend.
- `data`: SQLite và dữ liệu runtime, không được commit.

## Cài đặt

```powershell
uv sync --extra dev
Copy-Item .env.example .env
cd frontend
npm install
```

Điền `OPENAI_API_KEY` và các biến tùy chọn `TAVILY_API_KEY`, `MASSIVE_API_KEY`,
`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` trong `.env`.

Có thể dùng API tương thích OpenAI bằng `MODEL_PROVIDER=deepseek|grok|gemini|openrouter`.

## Chạy dashboard

Mở terminal thứ nhất tại thư mục gốc:

```powershell
uv run trader api
```

Mở terminal thứ hai:

```powershell
cd frontend
npm run dev
```

Truy cập `http://localhost:5173`. Vite chuyển tiếp `/api` đến FastAPI tại `http://127.0.0.1:8000`.

## Các lệnh backend

```powershell
uv run trader reset  # khởi tạo lại bốn tài khoản
uv run trader once   # chạy một vòng giao dịch
uv run trader run    # scheduler chạy liên tục
uv run trader api    # API dành cho dashboard Vite
uv run trader ui     # dashboard Gradio phụ
uv run pytest        # unit test
```

Đây là môi trường mô phỏng, không phải hệ thống giao dịch tiền thật.
