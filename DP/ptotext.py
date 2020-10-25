
from PyPDF2 import PdfFileWriter,PdfFileReader,PdfFileMerger


pdf_file = PdfFileReader(open("testforpdf.pdf","rb"))
my_file = open("knigga.txt", "w")
numPages = pdf_file.getNumPages()
for i in range(numPages):
        page = pdf_file.getPage(i)
        text = page.extractText()
        my_file.write(text)
        

my_file.close()