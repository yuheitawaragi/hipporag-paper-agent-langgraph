from pathlib import Path
import requests


def download_pdf(
    pdf_url,
    save_dir
):
    """
    PDFをダウンロードする
    """

    filename = pdf_url.split("/")[-1] + ".pdf"

    save_path = Path(save_dir) / filename

    # 既に存在するなら再利用
    if save_path.exists():
        return save_path

    response = requests.get(pdf_url)

    response.raise_for_status()

    with open(save_path, "wb") as f:
        f.write(response.content)

    return save_path