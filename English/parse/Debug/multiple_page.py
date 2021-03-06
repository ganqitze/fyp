import os
import time
import csv
from datetime import datetime
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTChar
from pdfminer.converter import PDFPageAggregator

start_time = time.time()

directory = "C:/Users/User/Desktop/fyp/order_paper/Debug"
log_file = "C://Users/User/Desktop/fyp/order_paper/Debug/log_2.csv"
stopword_dir = "C://Users/User/Desktop/fyp/stopword"
symbol_file = "C://Users/User/Desktop/fyp/stopword/special/symbol.txt"

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

def stopword_read():
	stop_list = []
	try:
		for file in os.listdir(stopword_dir):
			if file.endswith(".txt"):
				with open(os.path.join(stopword_dir + "/" + file)) as f:
					stop_list += f.readlines()
			stop_list = [x.strip() for x in stop_list]
	except IOError as e:
		print 'Operation failed: %s' % e.strerror
	return stop_list

def symbol_stop():
	with open(symbol_file) as f:
		symbol_list = f.readlines()
	# you may also want to remove whitespace characters like `\n` at the end of each line
	symbol_list = [x.strip() for x in symbol_list]
	return symbol_list


def parser(paper_id, date, file, stopword, symbol):
	page_count = 1
	password = ""
	extracted_text = ""
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
		if not 27 < page_count < 30:
			print "sup", page_count
			# break
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
						print extracted_text
						extracted_text = extracted_text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('       ',' ').replace('    ', ' ').replace('         ', ' ').replace(',', '').replace('READINNG', 'READING')
						extracted_text = extracted_text.replace(u'\u2018', '\'').replace(u'\u2019', '\'').replace(u'\u201C', '\"').replace(u'\u201D', '\"').replace(u'\u2013', '-')
						extracted_text = extracted_text.replace('.', '').replace('-', '').replace('MALAYSIA', '')
						for s in symbol:
							extracted_text = extracted_text.replace(s, ' ')
						for word in stopword:
							extracted_text = extracted_text.replace(' ' + word + ' ', ' ')
						while "  " in extracted_text:
							extracted_text = extracted_text.replace('  ', ' ')  # Replace double spaces by one while double spaces are in text			
						# print extracted_text, "SKIP"
		page_count = page_count + 1

	fp.close()
	# with open(log_file, "ab") as newFile:
	# 	newFileWriter = csv.writer(newFile)
	# 	newFileWriter.writerow([date, extracted_text.encode("utf-8")])


if __name__ == "__main__":	
	write_header()
	blacklist = stopword_read()
	symbol_blacklist = symbol_stop()
	for filename in os.listdir(directory):
		interval_time = time.time()
		if filename.startswith("OPDR") and filename.endswith(".pdf"):
			date = datetime.strptime(filename[4:-4], '%d%m%Y')
			parser(filename[:-4], date, os.path.join(directory, filename), blacklist, symbol_blacklist)  
			# print filename[4:-4]
		print("--- Done %s with %s seconds ---" % (filename, time.time() - interval_time))        	
	print("--- Done all! %s seconds ---" % (time.time() - start_time))
