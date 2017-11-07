import os
import time
import csv
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTChar
from pdfminer.converter import PDFPageAggregator

start_time = time.time()

directory = "C:/Users/User/Desktop/paper"
base_path = "C://Users/User/Desktop/fyp/order_paper"
log_file = os.path.join(base_path + "/" + "log_2.csv")
stopword_file = os.path.join("C://Users/User/Desktop/fyp/" + "stopword.txt")
word_1 = "AT THE COMMENCEMENT OF PUBLIC BUSINESS PRESENTATION OF GOVERNMENT BILL FOR FIRST READING"
word_2 = "AT THE COMMENCEMENT OF PUBLIC BUSINESS PRESENTATION OF GOVERNMENT BILLS FOR FIRST READING"
word_3 = "ORDERS OF THE DAY AND MOTIONS"
word_4 = "ORDERS OF THE DAY AND MOTION"
word_5 = "AT THE COMMENCEMENT OF PUBLIC BUSINESS PRESENTATION OF GOVERNMENT BILL FOR THE FIRST READING"
# word_5 = "AT THE COMMENCEMENT OF PUBLIC BUSINESS PRESENTATION OF GOVERNMENT BILLS FOR FIRST READINNG"

open(log_file, 'wb').close()

def write_header():
	with open(log_file, 'wb') as csvfile:
	    fieldnames = ['date', 'content']
	    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	    writer.writeheader()
	    # writer.writerow({'date': filename[4:-4], 'content': extracted_text.encode("utf-8")})

def stopword():
	with open(stopword_file) as f:
		stop_list = f.readlines()
	# you may also want to remove whitespace characters like `\n` at the end of each line
	stop_list = [x.strip() for x in stop_list]
	return stop_list

def parser(date, file):
	page_count = 1
	password = ""
	extracted_text = ""
	blacklist = stopword()

	# Open and read the pdf file in binary mode
	fp = open(file, "rb")
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

		if not 9 < page_count < 12:
			print "sup", page_count
		else:
			# As the interpreter processes the page stored in PDFDocument object
			interpreter.process_page(page)
			# The device renders the layout from interpreter
			layout = device.get_result()
			# Out of the many LT objects within layout, we are interested in LTTextBox and LTTextLine
			for lt_obj in layout:
				if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
					if word_1 in extracted_text or word_2 in extracted_text or word_3 in extracted_text or word_4 in extracted_text or word_5 in extracted_text:
						break
					else:
						extracted_text += lt_obj.get_text()
						# print lt_obj.get_text()
						extracted_text = extracted_text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace(u'\u2019', '\'').replace('       ',' ').replace('    ', ' ').replace('         ', ' ').replace(',', '').replace('READINNG', 'READING')
						while "  " in extracted_text:
							extracted_text = extracted_text.replace('  ', ' ')  # Replace double spaces by one while double spaces are in text
						for word in blacklist:
								extracted_text = extracted_text.replace(' ' + word + ' ', ' ')
		page_count = page_count + 1

	fp.close()
	with open(log_file, "ab") as newFile:
		newFileWriter = csv.writer(newFile)
		newFileWriter.writerow([date, extracted_text.encode("utf-8")])



if __name__ == "__main__":	
	write_header()
	for filename in os.listdir(directory):
		interval_time = time.time()
		if filename.startswith("OPDR") and filename.endswith(".pdf"):
			parser(filename[4:-4], os.path.join(directory, filename))
			# print filename[13:-7]
		print("--- Done %s with %s seconds ---" % (filename, time.time() - interval_time))        	
	print("--- Done all! %s seconds ---" % (time.time() - start_time))
