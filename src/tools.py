"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND (VINFAST HR ASSISTANT)
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
Đề tài: Trợ lý Nhân sự VinFast (VinFast HR Assistant)
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Tra cứu thông tin hồ sơ nhân sự VinFast
    {
        "name": "hr_employee_query",
        "description": "Tra cứu thông tin hồ sơ nhân sự của nhân viên VinFast bằng mã nhân viên (bao gồm họ tên, phòng ban, chức vụ, số ngày phép năm còn lại, người quản lý trực tiếp và gói bảo hiểm sức khỏe Vinmec Care).",
        "parameters": {
            "type": "object",
            "properties": {
                "employee_id": {
                    "type": "string",
                    "description": "Mã nhân viên VinFast cần tra cứu (ví dụ: 'VF2026001', 'VF2026002')"
                }
            },
            "required": ["employee_id"]
        }
    },
    
    # --------------------------------------------------------------------------
    # TASK 1.2: HOÀN THIỆN TOOL SCHEMA CHO 'submit_leave_request'
    # 🎯 YÊU CẦU THIẾT KẾ SCHEMA (JSON SCHEMA STANDARD):
    # Tool dùng để nộp đơn xin nghỉ phép cho nhân viên VinFast.
    # --------------------------------------------------------------------------
    {
        "name": "submit_leave_request",
        "description": "Tạo và gửi đơn xin nghỉ phép năm/nghỉ việc riêng cho nhân viên VinFast tới Quản lý trực tiếp để phê duyệt.",
        "parameters": {
            "type": "object",
            "properties": {
                "employee_id": {
                    "type": "string",
                    "description": "Mã nhân viên nộp đơn xin nghỉ phép (ví dụ: 'VF2026001')"
                },
                "start_date": {
                    "type": "string",
                    "description": "Ngày bắt đầu nghỉ phép (định dạng DD/MM/YYYY hoặc chuỗi ngày, ví dụ: '20/09/2026')"
                },
                "days_count": {
                    "type": "integer",
                    "description": "Số ngày đăng ký nghỉ phép (ví dụ: 1, 2)"
                },
                "reason": {
                    "type": "string",
                    "description": "Lý do xin nghỉ phép (ví dụ: 'Việc cá nhân', 'Nghỉ du lịch gia đình')"
                },
                "approver_name": {
                    "type": "string",
                    "description": "Tên người quản lý phê duyệt đơn (không bắt buộc, nếu có)"
                }
            },
            "required": ["employee_id", "start_date", "days_count", "reason"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_DATABASE = {
    "VF2026001": {
        "full_name": "Nguyễn Văn An",
        "department": "Khối Sản xuất Ô tô Điện (Nhà máy Hải Phòng - Xưởng Lắp ráp VF3 & VF8)",
        "position": "Kỹ sư Tự động hóa Dây chuyền",
        "annual_leave_remaining": 10,
        "manager": "Trần Văn Bình",
        "email": "an.nv@vinfast.vn",
        "insurance": "Vinmec Care Gold",
        "status": "Chính thức - Đang làm việc"
    },
    "VF2026002": {
        "full_name": "Lê Thị Mai",
        "department": "Khối R&D Phần mềm Xe Thông minh (Hà Nội - Đội Tự hành ADAS)",
        "position": "Chuyên viên Phát triển Thuật toán AI",
        "annual_leave_remaining": 3,
        "manager": "Đỗ Minh Tuấn",
        "email": "mai.lt@vinfast.vn",
        "insurance": "Vinmec Care Platinum",
        "status": "Chính thức - Đang làm việc"
    }
}


def execute_hr_employee_query(employee_id: str) -> str:
    """Thực thi tra cứu thông tin nhân sự VinFast theo mã nhân viên"""
    clean_id = employee_id.strip().upper()
    emp = MOCK_DATABASE.get(clean_id)
    if emp:
        return json.dumps({
            "status": "SUCCESS",
            "employee_id": clean_id,
            "data": emp
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy dữ liệu hồ sơ nhân sự cho mã nhân viên '{employee_id}' trong hệ thống VinFast."
        }, ensure_ascii=False)


def execute_submit_leave_request(
    employee_id: str,
    start_date: str,
    days_count: int = 1,
    reason: str = "Việc riêng cá nhân",
    approver_name: str = ""
) -> str:
    """Thực thi tạo đơn xin nghỉ phép nhân viên VinFast"""
    clean_id = employee_id.strip().upper()
    emp = MOCK_DATABASE.get(clean_id)
    
    try:
        days_num = int(days_count)
    except (ValueError, TypeError):
        days_num = 1

    if not emp:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không thể tạo đơn nghỉ phép do mã nhân viên '{employee_id}' không tồn tại trên hệ thống VinFast."
        }, ensure_ascii=False)

    leave_remaining = emp.get("annual_leave_remaining", 0)
    manager = approver_name if approver_name else emp.get("manager", "Phòng Nhân sự VinFast")

    if days_num > leave_remaining:
        return json.dumps({
            "status": "REJECTED",
            "employee_id": clean_id,
            "full_name": emp["full_name"],
            "requested_days": days_num,
            "available_days": leave_remaining,
            "message": f"Từ chối tạo đơn: Số ngày xin nghỉ ({days_num} ngày) vượt quá số ngày phép còn lại ({leave_remaining} ngày) của nhân viên {emp['full_name']}."
        }, ensure_ascii=False)

    request_id = f"LR-{clean_id}-2026"
    return json.dumps({
        "status": "SUCCESS",
        "request_id": request_id,
        "employee_id": clean_id,
        "full_name": emp["full_name"],
        "start_date": start_date,
        "days_count": days_num,
        "reason": reason,
        "approver": manager,
        "leave_balance_before": leave_remaining,
        "leave_balance_after": leave_remaining - days_num,
        "message": f"Tạo đơn nghỉ phép thành công (Mã đơn: {request_id}) cho nhân viên {emp['full_name']} ({clean_id}) - Nghỉ {days_num} ngày kể từ {start_date}. Đơn đã chuyển tới Quản lý ({manager}) phê duyệt."
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "hr_employee_query": execute_hr_employee_query,
    "submit_leave_request": execute_submit_leave_request,
    # Alias tương thích ngược
    "academic_query": execute_hr_employee_query,
    "schedule_appointment": execute_submit_leave_request
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)
