# app/core/workspace.py
import json
import os
from datetime import datetime

WORKSPACE_FILE = "data/workspaces.json"

def init_workspaces():
    """初始化全局工作区注册表"""
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(WORKSPACE_FILE):
        with open(WORKSPACE_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "workspace_1": {
                    "display_name": "默认研究区",
                    "is_sniffed": False,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            }, f, ensure_ascii=False, indent=2)

def get_workspaces():
    """获取所有工作区列表"""
    init_workspaces()
    with open(WORKSPACE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def create_workspace():
    """创建一个纯物理 ID 的新工作区"""
    workspaces = get_workspaces()
    new_id = f"workspace_{len(workspaces) + 1}"
    workspaces[new_id] = {
        "display_name": f"新建工作区 {len(workspaces) + 1}",
        "is_sniffed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(WORKSPACE_FILE, "w", encoding="utf-8") as f:
        json.dump(workspaces, f, ensure_ascii=False, indent=2)
    return new_id

def update_workspace_name(workspace_id: str, new_name: str):
    """(由 AI 嗅探器调用) 更新工作区的显示名称"""
    workspaces = get_workspaces()
    if workspace_id in workspaces:
        workspaces[workspace_id]["display_name"] = new_name
        workspaces[workspace_id]["is_sniffed"] = True
        with open(WORKSPACE_FILE, "w", encoding="utf-8") as f:
            json.dump(workspaces, f, ensure_ascii=False, indent=2)