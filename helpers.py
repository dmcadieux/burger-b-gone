from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTTextBoxHorizontal, LTTextLine
from docx import Document
import os
from chardet import detect

class my_dict(dict):
    def __init__(self):
        self = dict()
    def add(self, key, value):
        self[key] = value

text_dict = my_dict()

# Adds contents of plaintext to dict
def plaintext_reader(inp):

    text_dict.clear()

    with open(inp, 'r', encoding="UTF-8") as target:
        i = 0
        for line in target:
            text_dict.key = i
            text_dict.value = line.rstrip('\n')
            text_dict.add(text_dict.key, text_dict.value)
            i += 1
            
        encoding = "UTF-8"
        

        return text_dict, encoding


# Adds text content of pdf to dict
def pdf_reader(inp):

    text_dict.clear()

    with open(inp, 'rb') as document:

        # Create resource manager
        rsrcmgr = PDFResourceManager()
    
        # Set params for analysis
        laparams = LAParams()

        # Create PDF page aggregator object
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        i = 0

        for page in PDFPage.get_pages(document):
            interpreter.process_page(page)

            # Receive the LTPage object for the page
            layout = device.get_result()

            # Add extracted text to dict line by line
            for element in layout:
                if isinstance(element, LTTextBoxHorizontal):
                    for line in element:
                        if isinstance(line, LTTextLine):
                            txt = line.get_text()

                            

                            text_dict.key = i
                            text_dict.value = txt
                            text_dict.add(text_dict.key, text_dict.value)
                            i += 1

        encoding = detect(txt.encode())['encoding']

    return text_dict, encoding


# Adds content of word doc to dict
def doc_reader(inp):

    text_dict.clear()

    file = os.path.basename(inp)

    doc = Document(file)
    full_text = []

    for para in doc.paragraphs:
        full_text.append(para.text.split("\n"))

    i = 0

    for item in full_text:
        text_dict.key = i
        text_dict.value = item[0]
        text_dict.add(text_dict.key, text_dict.value)
        i += 1

    encoding = detect(text_dict[i-1].encode())['encoding']

    return text_dict, encoding
