import fitz
from docx import Document


class JDParser:

    @staticmethod
    def extract_text(file_path):

        if file_path.endswith(".pdf"):

            text = ""

            pdf = fitz.open(file_path)

            for page in pdf:
                text += page.get_text()

            pdf.close()

            return text.strip()

        elif file_path.endswith(".docx"):

            doc = Document(file_path)

            return "\n".join(
                paragraph.text
                for paragraph in doc.paragraphs
            )

        elif file_path.endswith(".txt"):

            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()

        return ""