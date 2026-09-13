"""
🔌 MODEL CONTEXT PROTOCOL (MCP) SERVER MODULE
Mô phỏng kiến trúc MCP Server (Client-Server Architecture) cung cấp công cụ chuẩn hóa.
Hệ thống: Trợ lý Nhân sự VinFast (VinFast HR ReAct Agent - MCP Enhanced)
"""

import json
import os
import sys
from typing import Dict, Any, List

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools import TOOLS_SCHEMA, dispatch_tool_call

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class MCPAcademicServer:
    """
    Giả lập MCP Server tuân thủ chuẩn giao thức Model Context Protocol (MCP JSON-RPC 2.0)
    """
    def __init__(self, server_name: str = "vinfast-hr-mcp-server"):
        self.server_name = server_name
        self.version = "2026.1.0"
        
    def list_tools(self) -> List[Dict[str, Any]]:
        """Trả về danh sách các Tools chuẩn giao thức MCP"""
        return TOOLS_SCHEMA
        
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        [TASK 2.1] HỌC VIÊN HOÀN THIỆN HÀM THỰC THI TOOL TRÊN MCP SERVER
        Thực thi request gọi Tool theo chuẩn MCP JSON-RPC 2.0
        """
        # 1. Gọi hàm dispatch_tool_call để nhận chuỗi JSON từ Tool Execution Router
        raw_result = dispatch_tool_call(tool_name, arguments)
        
        # 2. Chuyển đổi chuỗi JSON kết quả thành Python Dictionary
        try:
            parsed_result = json.loads(raw_result)
        except Exception:
            parsed_result = {"status": "PARSE_ERROR", "raw": raw_result}
            
        # 3. Đóng gói phản hồi và trả về Dict theo đúng chuẩn giao thức MCP JSON-RPC 2.0
        return {
            "jsonrpc": "2.0",
            "server": self.server_name,
            "tool": tool_name,
            "result": parsed_result
        }


if __name__ == "__main__":
    print("==========================================================")
    print("🔌 KIỂM THỬ ĐỘC LẬP MCP SERVER (vinfast-hr-mcp-server)")
    print("==========================================================")
    
    server = MCPAcademicServer("vinfast-hr-mcp-server")
    tools = server.list_tools()
    print(f"✅ Khởi tạo thành công MCP Server: {server.server_name} (Version: {server.version})")
    print(f"📦 Số lượng Tools công bố: {len(tools)}")
    
    # Kiểm tra trạng thái Task 1.2 (Tool Schema submit_leave_request)
    leave_tool = next((t for t in tools if t.get("name") == "submit_leave_request"), None)
    if leave_tool and not leave_tool.get("parameters", {}).get("properties"):
        print("⏳ [TASK 1.2]: Tool 'submit_leave_request' chưa được định nghĩa properties trong 'src/tools.py'.")
    else:
        print("✅ [TASK 1.2]: Tool 'submit_leave_request' đã có schema đầy đủ theo chuẩn JSON Schema.")

    # Kiểm tra trạng thái Task 2.1 (call_tool theo chuẩn JSON-RPC)
    test_result = server.call_tool("hr_employee_query", {"employee_id": "VF2026001"})
    if not test_result or "result" not in test_result:
        print("⏳ [TASK 2.1]: Hàm call_tool() đang trả về rỗng. Học viên hãy hoàn thiện Task 2.1 trong 'src/mcp_server.py'!")
    else:
        print(f"✅ [TASK 2.1]: Test dispatch tool 'hr_employee_query' thành công:")
        print(f"   Phản hồi JSON-RPC 2.0: {json.dumps(test_result, ensure_ascii=False)}")
