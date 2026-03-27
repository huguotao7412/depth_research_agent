# app/rag/pdf_parser.py
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class KimiAPIParser:
    def __init__(self, output_dir: str = "./data/parsed_docs"):
        self.output_dir = output_dir
        self.api_key = os.getenv("MOONSHOT_API_KEY")

        if not self.api_key:
            raise ValueError("❌ 错误：未能在 .env 文件中找到 MOONSHOT_API_KEY！请前往 Kimi 开放平台申请。")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def parse_pdf(self, pdf_path: str) -> str:
        """
        使用 Kimi (Moonshot) API 解析本地 PDF 文件，提取出 Markdown 内容。
        """
        pdf_name = Path(pdf_path).stem
        print(f"☁️ 正在使用 Kimi 大模型解析本地文献: {pdf_name}...")

        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        # ==========================================
        # 步骤 1: 直接上传本地文件给 Kimi
        # ==========================================
        upload_url = "https://api.moonshot.cn/v1/files"

        with open(pdf_path, 'rb') as f:
            files = {
                "file": (f"{pdf_name}.pdf", f, "application/pdf")
            }
            data = {
                "purpose": "file-extract"  # 声明用途为文件内容提取
            }
            print("🚀 正在上传本地文件...")
            # 发起上传请求
            upload_res = requests.post(upload_url, headers=headers, files=files, data=data)
            upload_res.raise_for_status()

            file_info = upload_res.json()
            file_id = file_info.get("id")

        if not file_id:
            raise Exception("文件上传失败，未能获取到 File ID")

        print(f"✅ 文件上传成功 (ID: {file_id})，正在提取内容...")

        # ==========================================
        # 步骤 2: 获取解析后的 Markdown 内容
        # ==========================================
        content_url = f"https://api.moonshot.cn/v1/files/{file_id}/content"
        content_res = requests.get(content_url, headers=headers)
        content_res.raise_for_status()

        # Kimi 会返回包含 Markdown 内容的 JSON
        result_data = content_res.json()
        md_content = result_data.get("content", "")

        if not md_content:
            raise Exception("内容提取失败，返回内容为空！")

        # ==========================================
        # 步骤 3: 保存结果到本地文件
        # ==========================================
        doc_output_dir = os.path.join(self.output_dir, pdf_name)
        os.makedirs(doc_output_dir, exist_ok=True)
        md_path = os.path.join(doc_output_dir, f"{pdf_name}.md")

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        print(f"✨ {pdf_name} 解析完成！结果已保存至 {md_path}")
        return md_path