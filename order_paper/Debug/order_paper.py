# pdfTextMiner.py
# Python 2.7.6
# For Python 3.x use pdfminer3k module
# This link has useful information on components of the program
# https://euske.github.io/pdfminer/programming.html
# http://denis.papathanasiou.org/posts/2010.08.04.post.html


''' Important classes to remember
PDFParser - fetches data from pdf file
PDFDocument - stores data parsed by PDFParser
PDFPageInterpreter - processes page contents from PDFDocument
PDFDevice - translates processed information from PDFPageInterpreter to whatever you need
PDFResourceManager - Stores shared resources such as fonts or images used by both PDFPageInterpreter and PDFDevice
LAParams - A layout analyzer returns a LTPage object for each page in the PDF document
PDFPageAggregator - Extract the decive to page aggregator to get LT object elements
'''

import os
import time

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
# From PDFInterpreter import both PDFResourceManager and PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
# Import this to raise exception whenever text extraction from PDF is not allowed
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTChar
from pdfminer.converter import PDFPageAggregator

''' This is what we are trying to do:
1) Transfer information from PDF file to PDF document object. This is done using parser
2) Open the PDF file
3) Parse the file using PDFParser object
4) Assign the parsed content to PDFDocument object
5) Now the information in this PDFDocumet object has to be processed. For this we need
   PDFPageInterpreter, PDFDevice and PDFResourceManager
 6) Finally process the file page by page 
'''

start_time = time.time()

base_path = "C://Users/User/Desktop/fyp/order_paper"


my_file = os.path.join(base_path + "/" + "OPDR26032014.pdf")
log_file = os.path.join(base_path + "/" + "log8.txt")
stopword_file = os.path.join("C://Users/User/Desktop/fyp/stopword/" + "code.txt")

password = ""
extracted_text = ""

# stopword list
with open(stopword_file) as f:
    blacklist = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
blacklist = [x.strip() for x in blacklist] 


# Open and read the pdf file in binary mode
fp = open(my_file, "rb")

# Create parser object to parse the pdf content
parser = PDFParser(fp)

# Store the parsed content in PDFDocument object
document = PDFDocument(parser, password)

# Check if document is extractable, if not abort
if not document.is_extractable:
	raise PDFTextExtractionNotAllowed
	
# Create PDFResourceManager object that stores shared resources such as fonts or images
rsrcmgr = PDFResourceManager()

# set parameters for analysis
laparams = LAParams()

# Create a PDFDevice object which translates interpreted information into desired format
# Device needs to be connected to resource manager to store shared resources
# device = PDFDevice(rsrcmgr)
# Extract the decive to page aggregator to get LT object elements
device = PDFPageAggregator(rsrcmgr, laparams=laparams)

# Create interpreter object to process page content from PDFDocument
# Interpreter needs to be connected to resource manager for shared resources and device 
interpreter = PDFPageInterpreter(rsrcmgr, device)

# Ok now that we have everything to process a pdf document, lets process it page by page
for page in PDFPage.create_pages(document):
	# As the interpreter processes the page stored in PDFDocument object
	interpreter.process_page(page)
	# The device renders the layout from interpreter
	layout = device.get_result()
	# Out of the many LT objects within layout, we are interested in LTTextBox and LTTextLine
	for lt_obj in layout:
		if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
			extracted_text += lt_obj.get_text()
			extracted_text = extracted_text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace(u'\u2019', '\'').replace('       ',' ').replace('    ', ' ').replace('         ', ' ').replace(',', '')
			while "  " in extracted_text:
				extracted_text = extracted_text.replace('  ', ' ')  # Replace double spaces by one while double spaces are in text
			for word in blacklist:
				extracted_text = extracted_text.replace(' ' + word + ' ', ' ')
			#close the pdf file
fp.close()

with open(log_file, "w") as my_log:
    my_log.write(extracted_text.encode("utf-8"))

print("--- Done parsing! %s seconds ---" % (time.time() - start_time))



