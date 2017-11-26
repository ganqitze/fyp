
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

# base_path_lin  = "/home/User/Desktop/fyp/order_paper"
# base_path_win = "C:/Users/User/Desktop/fyp/English/order_paper"

paper_dir = "C:/Users/User/Desktop/fyp/Malay/order_paper/paper"
stopword_dir = "C:/Users/User/Desktop/fyp/Malay/order_paper/stopword"
log_file = "C:/Users/User/Desktop/fyp/Malay/order_paper/parse/log.csv"
symbol_file = "C:/Users/User/Desktop/fyp/Malay/order_paper/stopword/special/symbol.txt"

# paper_dir = "/home/User/fyp/paper"
# stopword_dir = "/home/User/fyp/stopword"
# log_file = "/home/User/fyp/order_paper/log.csv"
# symbol_file = "/home/User/fyp/stopword/special/symbol.txt"

word_1 = "UCAPANUCAPAN"
word_2 = "UCAPAN PENANGGUHAN"
word_3 = "UCAPANUCAPAN PENANGGUHAN"
word_4 = "RISALATRISALAT YANG DIBAWA KE DALAM MESYUARAT"
word_5 = "RISALAT DOKUMEN TARIKH DIBENTANGKAN"

open(log_file, 'wb').close()

def write_header():
    with open(log_file, 'wb') as csvfile:
        fieldnames = ['paper_id', 'date', 'content']
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
    extracted_text = " "
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
        # if not 8 < page_count < 10:
        #   print "sup", page_count
        # else:
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
                    # print lt_obj.get_text(), "SKIP"
                    extracted_text = extracted_text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('       ',' ').replace('    ', ' ').replace('         ', ' ').replace(',', '')
                    extracted_text = extracted_text.replace(u'\u2018', '\'').replace(u'\u2019', '\'').replace(u'\u201C', '\"').replace(u'\u201D', '\"').replace(u'\u2013', '')
                    extracted_text = extracted_text.replace('.', '').replace('-', '').replace(')', '').replace('(', '').replace('MALAYSIA', '')
                    extracted_text = remove_stopword(extracted_text, symbol, stopword)
        page_count = page_count + 1        
        if (page_count%10 == 0):     
            extracted_text = remove_stopword(extracted_text, symbol, stopword)
            save_text(paper_id, date, extracted_text)
            extracted_text = " "        
    fp.close()
    extracted_text = remove_stopword(extracted_text, symbol, stopword)
    if not extracted_text == " ":
        save_text(paper_id, date, extracted_text)


def remove_stopword(extracted_text, symbol, stopword):
    for s in symbol:
        extracted_text = extracted_text.replace(s, ' ')
    for word in stopword:
            extracted_text = extracted_text.replace(' ' + word + ' ', ' ')
    while "  " in extracted_text:
        extracted_text = extracted_text.replace('  ', ' ')  # Replace double spaces by one while double spaces are in text
    extracted_text = extracted_text.replace(word_1 + ' ', '').replace(word_2 + ' ', '').replace(word_3 + ' ', '').replace(word_4 + ' ', '').replace(word_5 + ' ', '')
    return extracted_text


def save_text(paper_id, date, extracted_text):    
    with open(log_file, "ab") as newFile:
        newFileWriter = csv.writer(newFile)
        newFileWriter.writerow([paper_id, date, extracted_text.encode("utf-8")])


if __name__ == "__main__":  
    write_header()
    blacklist = stopword_read()
    symbol_blacklist = symbol_stop()
    for filename in os.listdir(paper_dir):
        page_start = 0
        interval_time = time.time()
        if filename.startswith("AUMDR") and filename.endswith(".pdf"):
            date = datetime.strptime(filename[5:-4], '%d%m%Y')
            parser(filename[:-4], date, os.path.join(paper_dir, filename), blacklist, symbol_blacklist) 
        print("--- Done %s with %s seconds ---" % (filename, time.time() - interval_time))
    print("--- Done all! %s seconds ---" % (time.time() - start_time))
