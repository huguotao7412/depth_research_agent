import os
import httpx  # ✅ 1. 引入 httpx
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class KimiAPIParser:
    def __init__(self, output_dir: str = "./data/parsed_docs"):
        # ... 这里的 __init__ 保持原样不变 ...
        self.output_dir = output_dir
        self.api_key = os.getenv("MOONSHOT_API_KEY")
        if not self.api_key:
            raise ValueError("❌ 错误：未能在 .env 文件中找到 MOONSHOT_API_KEY！")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    # ✅ 2. 加上 async，为了规范可以改名为 aparse_pdf
    async def aparse_pdf(self, pdf_path: str) -> str:
        """
        使用 Kimi API 异步解析本地 PDF 文件
        """
        pdf_name = Path(pdf_path).stem
        print(f"☁️ 正在使用 Kimi 大模型【异步】解析本地文献: {pdf_name}...")

        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        # ✅ 3. 使用异步上下文管理器，设置充足的超时时间 (解析长 PDF 很慢)
        async with httpx.AsyncClient(timeout=120.0) as client:

            # ==========================================
            # 步骤 1: 异步上传本地文件
            # ==========================================
            upload_url = "https://api.moonshot.cn/v1/files"
            with open(pdf_path, 'rb') as f:
                files = {"file": (f"{pdf_name}.pdf", f, "application/pdf")}
                data = {"purpose": "file-extract"}

                print("🚀 正在异步上传本地文件...")
                # ✅ 4. 使用 await 发起异步 POST 请求
                upload_res = await client.post(upload_url, headers=headers, files=files, data=data)
                upload_res.raise_for_status()

                file_info = upload_res.json()
                file_id = file_info.get("id")

            if not file_id:
                raise Exception("文件上传失败，未能获取到 File ID")

            print(f"✅ 文件上传成功 (ID: {file_id})，正在提取内容...")

            # ==========================================
            # 步骤 2: 异步获取解析后的 Markdown 内容
            # ==========================================
            content_url = f"https://api.moonshot.cn/v1/files/{file_id}/content"
            # ✅ 5. 使用 await 发起异步 GET 请求
            content_res = await client.get(content_url, headers=headers)
            content_res.raise_for_status()

            result_data = content_res.json()
            md_content = result_data.get("content", "")

            if not md_content:
                raise Exception("内容提取失败，返回内容为空！")

        # ==========================================
        # 步骤 3: 保存结果到本地文件 (本地磁盘 I/O 极快，可保持同步)
        # ==========================================
        doc_output_dir = os.path.join(self.output_dir, pdf_name)
        os.makedirs(doc_output_dir, exist_ok=True)
        md_path = os.path.join(doc_output_dir, f"{pdf_name}.md")

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        print(f"✨ {pdf_name} 解析完成！结果已保存至 {md_path}")
        return md_path