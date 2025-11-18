import io
from PIL import Image
from extraction import extract_pdf_text
from extraction import extract_docx_text
from extraction import extract_pptx_text
from extraction import extract_html_text
from extraction import extract_text_file
from ocr import ocr_image



def process_all_documents(pdf_docs, docx_docs, pptx_docs, html_docs, txt_docs, image_docs, enable_ocr, poppler_path):
    all_text = ""
    if pdf_docs:
        for pdf in pdf_docs:
            all_text += extract_pdf_text(pdf, enable_ocr, poppler_path) + "\n\n"
    if docx_docs:
        for docx in docx_docs:
            all_text += extract_docx_text(docx) + "\n\n"
    if pptx_docs:
        for pptx in pptx_docs:
            all_text += extract_pptx_text(pptx) + "\n\n"
    if html_docs:
        for html in html_docs:
            all_text += extract_html_text(html) + "\n\n"
    if txt_docs:
        for txt in txt_docs:
            all_text += extract_text_file(txt) + "\n\n"
    if image_docs:
        for img_file in image_docs:
            try:
                img = Image.open(io.BytesIO(img_file.read())).convert("RGB")
                ocr_text = ocr_image(img)
                if ocr_text:
                    all_text += ocr_text + "\n\n"
            except:
                pass
    return all_text