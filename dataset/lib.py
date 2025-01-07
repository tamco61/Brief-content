import os
import requests
import pdfplumber
from bs4 import BeautifulSoup

ARTICLE_DATA_DIR = "data"


def create_abs_link(arxivId: str):
    return f"https://arxiv.org/abs/{arxivId}"


def create_pdf_link(arxivId: str):
    return f"https://arxiv.org/pdf/{arxivId}.pdf"


def get_abs(arxivId: str):
    url = create_abs_link(arxivId)

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Ошибка при получении статьи по ссылке {url}: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    abstract = soup.find('blockquote', class_='abstract').get_text(strip=True)

    return abstract


def get_pdf(arxivId: str):
    url = create_pdf_link(arxivId)

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Ошибка при получении pdf по ссылке {url}: {response.status_code}")

    return response.content


def save_pdf(path, content, arxivId):
    with open(os.path.join(path, f'{arxivId}.pdf'), 'wb') as f:
        f.write(content)


def save_abs(path, content, arxivId):
    with open(os.path.join(path, f'{arxivId}_abs.txt'), 'w', encoding='utf-8') as f:
        f.write(content)


# Выгрузка описания статьи и текста в формате pdf
def article_handler(arxivId: str):
    resultDir = os.path.join(ARTICLE_DATA_DIR, arxivId)
    if os.path.exists(resultDir):
        raise Exception(f"По статье {arxivId} материалы уже созданы")

    os.mkdir(resultDir)

    absContent = get_abs(arxivId)
    pdfContent = get_pdf(arxivId)

    save_abs(resultDir, absContent, arxivId)
    save_pdf(resultDir, pdfContent, arxivId)


def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def pdf_handler(arxivId: str):

    text = extract_text_from_pdf(os.path.join(ARTICLE_DATA_DIR, arxivId, f"{arxivId}.pdf"))

    with open(os.path.join(os.path.join(ARTICLE_DATA_DIR, arxivId), f'{arxivId}_pdf.txt'), 'w', encoding='utf-8') as f:
        f.write(text)


def main():
    for i in range(378, 1000):
        arxivId = "2412." + (5 - len(str(i))) * "0" + str(i)
        article_handler(arxivId)
        pdf_handler(arxivId)
        print(i)

if __name__ == "__main__":
    main()



