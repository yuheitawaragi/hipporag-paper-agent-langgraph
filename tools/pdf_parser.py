from pathlib import Path

import requests
from pypdf import PdfReader


class PDFParser:

    def __init__(self, save_dir="papers"):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)

    def download_pdf(self, pdf_url: str, filename: str) -> Path:
        """
        PDFをダウンロードして保存
        """

        print(f"Downloading: {pdf_url}")

        pdf_path = self.save_dir / filename

        response = requests.get(pdf_url, timeout=60)
        print(f"Status: {response.status_code}")
        response.raise_for_status()

        with open(pdf_path, "wb") as f:
            f.write(response.content)

        print(f"Saved: {pdf_path}")

        return pdf_path

    def extract_text(self, pdf_path: Path) -> str:
        """
        PDF全文を取得
        """

        reader = PdfReader(pdf_path)

        pages = []

        for page in reader.pages:

            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n".join(pages)
    
    def extract_pages(self, pdf_path):
        reader = PdfReader(pdf_path)
        pages = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                pages.append(
                {
                    "page": i + 1,
                    "text": text,
                }
            )
        
        return pages
    
    from pathlib import Path

import requests
from pypdf import PdfReader


class PDFParser:

    def __init__(self, save_dir="papers"):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)

    def download_pdf(self, pdf_url, filename):
        pdf_path = self.save_dir / filename

        response = requests.get(pdf_url, timeout=60)
        response.raise_for_status()

        with open(pdf_path, "wb") as f:
            f.write(response.content)

        return pdf_path

    def extract_pages(self, pdf_path):

        reader = PdfReader(pdf_path)

        pages = []

        for i, page in enumerate(reader.pages):

            text = page.extract_text()

            if text:

                pages.append(
                    {
                        "page": i + 1,
                        "text": text,
                    }
                )

        return pages

    def chunk_pages(
        self,
        pages,
        chunk_size=1000,
        overlap=200,
    ):
        """
        ページ情報を保持したままChunk化
        """

        chunks = []

        chunk_id = 0

        for page in pages:

            text = page["text"]

            start = 0

            while start < len(text):

                end = start + chunk_size

                chunk = text[start:end]

                chunks.append(
                    {
                        "chunk_id": chunk_id,
                        "page": page["page"],
                        "text": chunk,
                    }
                )

                chunk_id += 1

                start += chunk_size - overlap

        return chunks
