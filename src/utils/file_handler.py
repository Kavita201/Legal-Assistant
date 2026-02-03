import PyPDF2
from docx import Document
from typing import Optional

class FileHandler:
    def extract_text(self, file) -> Optional[str]:
        """Extract text from uploaded file"""
        try:
            if file.type == "application/pdf":
                return self._extract_pdf(file)
            elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                return self._extract_docx(file)
            elif file.type == "text/plain":
                return str(file.read(), "utf-8")
            return None
        except Exception:
            return None
    
    def _extract_pdf(self, file) -> str:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    
    def _extract_docx(self, file) -> str:
        doc = Document(file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text