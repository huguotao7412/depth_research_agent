# app/core/memory_store.py
import os
import json
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from app.core.llm_factory import get_embeddings


def get_memory_paths(workspace_id: str):
    base_dir = f"data/{workspace_id}/memory"
    os.makedirs(base_dir, exist_ok=True)
    return f"{base_dir}/profile.json", f"{base_dir}/experience_db"


# ====================================
# 1. 显式画像 (Explicit Profile JSON)
# ====================================
def get_profile(workspace_id: str) -> dict:
    profile_path, _ = get_memory_paths(workspace_id)
    if os.path.exists(profile_path):
        try:
            with open(profile_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def update_profile(workspace_id: str, new_preferences: dict):
    profile_path, _ = get_memory_paths(workspace_id)
    current_profile = get_profile(workspace_id)

    # 智能合并字典：如果是列表则追加去重，如果是字符串则覆盖
    for k, v in new_preferences.items():
        if k in current_profile and isinstance(current_profile[k], list) and isinstance(v, list):
            current_profile[k] = list(set(current_profile[k] + v))
        else:
            current_profile[k] = v

    with open(profile_path, "w", encoding="utf-8") as f:
        json.dump(current_profile, f, ensure_ascii=False, indent=2)


# ====================================
# 2. 隐式经验库 (Implicit Experience FAISS)
# ====================================
def add_experience(workspace_id: str, lessons: list[str]):
    if not lessons:
        return
    _, db_path = get_memory_paths(workspace_id)
    embeddings = get_embeddings()
    docs = [Document(page_content=lesson, metadata={"type": "lesson"}) for lesson in lessons]

    if os.path.exists(os.path.join(db_path, "index.faiss")):
        vector_store = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)
        vector_store.add_documents(docs)
    else:
        vector_store = FAISS.from_documents(docs, embeddings)

    vector_store.save_local(db_path)


def search_experience(workspace_id: str, query: str, top_k: int = 2) -> str:
    _, db_path = get_memory_paths(workspace_id)
    if not os.path.exists(os.path.join(db_path, "index.faiss")):
        return ""
    try:
        embeddings = get_embeddings()
        vector_store = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)
        results = vector_store.similarity_search(query, k=top_k)
        return "\n".join([f"- {res.page_content}" for res in results])
    except Exception as e:
        print(f"⚠️ [Memory Store] 经验库检索异常: {e}")
        return ""