# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Lưu Xuân Dũng  
> **Mã Sinh Viên / Mã Học viên:** 2A202602746  
> **Chủ đề Lựa chọn:** Gợi ý 2.1: Trợ lý Nhân sự VinFast (VinFast HR ReAct Agent - MCP Enhanced)  

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | **5** / 5 | Bài toán yêu cầu chia nhỏ chuỗi suy luận nối tiếp: Tra cứu hồ sơ nhân sự trước để xác định số ngày phép còn lại và người quản lý trực tiếp $\rightarrow$ Kiểm tra điều kiện nghỉ phép $\rightarrow$ Tạo đơn xin nghỉ phép chỉ định đúng quản lý phê duyệt. |
| **2. Tool Interaction** | **5** / 5 | Hệ thống kết nối MCP Server (`vinfast-hr-mcp-server`) theo chuẩn giao thức MCP JSON-RPC 2.0 với 2 công cụ: `hr_employee_query` (tra cứu thông tin nhân sự) và `submit_leave_request` (khởi tạo đơn nghỉ phép vào CSDL). |
| **3. Dynamic Decision** | **4** / 5 | Quyết định bước tiếp theo phụ thuộc động vào kết quả quan sát (Observation): Nếu `STATUS == SUCCESS` và đủ ngày phép thì nộp đơn; nếu số ngày nghỉ vượt hạn mức thì từ chối; nếu mã nhân viên `NOT_FOUND` thì dừng và giải thích lịch sự (Anti-Hallucination). |
| **4. Long Horizon Goal** | **4** / 5 | Tác tử duy trì mục tiêu nghiệp vụ xuyên suốt: Từ lúc tiếp nhận yêu cầu tự nhiên của nhân viên, qua các bước gọi công cụ trung gian, cho đến khi xuất mã đơn nghỉ phép và tóm tắt số dư ngày phép mới. |
| **TỔNG ĐIỂM AGENTIC FIT** | **18 / 20** | *Tổng điểm 18/20 (> 12/20): Bài toán nghiệp vụ Trợ lý Nhân sự VinFast đặc biệt phù hợp để triển khai Agentic System.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp đã chạy thành công 100% trên mô hình thật Google Gemini `gemini-3.1-flash-lite`.

Dưới đây là trích xuất chuỗi suy luận ReAct đa bước (Multi-step) thực tế từ tệp `docs/trace_waterfall.json` (Test Case TC04: Tra cứu nhân viên $\rightarrow$ Gọi tool tạo đơn gửi quản lý):

```json
[
  {
    "step": 1,
    "query": "Nhân viên VF2026002 hiện còn bao nhiêu ngày phép năm và ai là người quản lý trực tiếp? Hãy tra cứu thông tin rồi tạo đơn xin nghỉ phép 1 ngày vào ngày 25/09/2026 gửi cho người quản lý đó.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "hr_employee_query",
    "arguments": {
      "employee_id": "VF2026002"
    },
    "observation": {
      "status": "SUCCESS",
      "employee_id": "VF2026002",
      "data": {
        "full_name": "Lê Thị Mai",
        "department": "Khối R&D Phần mềm Xe Thông minh (Hà Nội - Đội Tự hành ADAS)",
        "position": "Chuyên viên Phát triển Thuật toán AI",
        "annual_leave_remaining": 3,
        "manager": "Đỗ Minh Tuấn",
        "email": "mai.lt@vinfast.vn",
        "insurance": "Vinmec Care Platinum",
        "status": "Chính thức - Đang làm việc"
      }
    },
    "latency_ms": 2831.39
  },
  {
    "step": 2,
    "query": "Nhân viên VF2026002 hiện còn bao nhiêu ngày phép năm và ai là người quản lý trực tiếp? Hãy tra cứu thông tin rồi tạo đơn xin nghỉ phép 1 ngày vào ngày 25/09/2026 gửi cho người quản lý đó.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "submit_leave_request",
    "arguments": {
      "employee_id": "VF2026002",
      "start_date": "25/09/2026",
      "days_count": 1,
      "reason": "Việc cá nhân",
      "approver_name": "Đỗ Minh Tuấn"
    },
    "observation": {
      "status": "SUCCESS",
      "request_id": "LR-VF2026002-2026",
      "employee_id": "VF2026002",
      "full_name": "Lê Thị Mai",
      "start_date": "25/09/2026",
      "days_count": 1,
      "reason": "Việc cá nhân",
      "approver": "Đỗ Minh Tuấn",
      "leave_balance_before": 3,
      "leave_balance_after": 2,
      "message": "Tạo đơn nghỉ phép thành công (Mã đơn: LR-VF2026002-2026) cho nhân viên Lê Thị Mai (VF2026002) - Nghỉ 1 ngày kể từ 25/09/2026. Đơn đã chuyển tới Quản lý (Đỗ Minh Tuấn) phê duyệt."
    },
    "latency_ms": 3287.64
  },
  {
    "step": 3,
    "query": "Nhân viên VF2026002 hiện còn bao nhiêu ngày phép năm và ai là người quản lý trực tiếp? Hãy tra cứu thông tin rồi tạo đơn xin nghỉ phép 1 ngày vào ngày 25/09/2026 gửi cho người quản lý đó.",
    "action_type": "FINAL_ANSWER",
    "thought": "Gemini phản hồi trực tiếp bằng văn bản (không cần gọi công cụ).",
    "output": "Chào bạn Lê Thị Mai,\n\nTôi đã hoàn tất việc tra cứu thông tin và thực hiện yêu cầu của bạn. Dưới đây là kết quả chi tiết:\n\n1. **Thông tin nhân sự của bạn:**\n   - **Họ và tên:** Lê Thị Mai\n   - **Số ngày phép năm còn lại:** 3 ngày\n   - **Người quản lý trực tiếp:** Anh Đỗ Minh Tuấn\n\n2. **Kết quả tạo đơn xin nghỉ phép:**\n   - Đơn xin nghỉ phép của bạn đã được gửi thành công.\n   - **Mã đơn:** LR-VF2026002-2026\n   - **Thời gian nghỉ:** 1 ngày (ngày 25/09/2026)\n   - **Lý do:** Việc cá nhân\n   - **Người phê duyệt:** Anh Đỗ Minh Tuấn\n   - **Số ngày phép còn lại sau khi nghỉ:** 2 ngày\n\nĐơn của bạn đã được chuyển đến quản lý trực tiếp để xem xét và phê duyệt. Nếu cần hỗ trợ thêm thông tin gì khác, bạn vui lòng cho tôi biết nhé!",
    "latency_ms": 3145.22
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Google Gemini `gemini-3.1-flash-lite`).
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases (TC01 đến TC05).
- **Số lượt gọi Tool qua MCP Server chính xác:** 6 lượt (1 lượt tại TC02, 2 lượt tại TC03, 2 lượt tại TC04, 1 lượt tại TC05).
- **Kết quả đẩy Repo nộp bài:** [x] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!  
> 📌 **URL Repo cá nhân:** `https://github.com/luuxuandung04/K4A-DAY03-LuuXuanDung-2A202602746`
