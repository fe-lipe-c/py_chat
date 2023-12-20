import os
from pdfminer.high_level import extract_text
import config as cfg
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from io import StringIO
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import pandas as pd

path_files = cfg.CONTEXT_DOCS_PATH / "teste_1" / "to_process"
list_to_process = [path_files / i for i in os.listdir(path_files)]
print(list_to_process[0])

text_pages = {}
for i,page_layout in enumerate(extract_pages(list_to_process[0])):
    text_pages[i+1] = ''
    for element in page_layout:
        if isinstance(element, LTTextContainer):
            # print(element.get_text())
            text_pages[i+1] += element.get_text()

text_pages
list_temp = list(text_pages.values())[:2]
len(list_temp)

emb = cfg.OPENAI_CLIENT.embeddings.create(input = [list_temp],model='text-embedding-ada-002')
emb.data[0].embedding


for i in text_pages.values():
    print(i)

df = pd.DataFrame(list(text_pages.items()), columns=['page','text'])
df 

text_pages[1]

{1: 'Article\nA Q-Cube Framework of Reinforcement Learning\nAlgorithm for Continuous Double
Auction\namong Microgrids\nNing Wang 1\n, Weisheng Xu 1,* and Weihui Shao 2\nand Zhiyu Xu 1\n1\n2\nSchool,
 2:of Electronics and Information Engineering, Tongji University, Shanghai 201804, China\nEducation
Technology and Computing Center, Tongji University, Shanghai 200092, China\n* Correspondence:
 xuweisheng@tongji.edu.cn; Tel.: +86-21-6598-1061\nReceived: 9 July 2019; Accepted: 23 July 2019}
