from PyPDF2 import PdfFileWriter, PdfFileReader
import os
import time

paper_dir = "C:/Users/User/Desktop/fyp/Malay/hansard/paper"

def split(filename, docs):
	output = PdfFileWriter()
	input1 = PdfFileReader(open(docs, "rb"))

	# print how many pages input1 has:
	print "%s.pdf has %d pages." %(filename, input1.getNumPages())
	counter = 0
	while counter < input1.getNumPages():
		if counter > 8:
			output.addPage(input1.getPage(counter))
		counter += 1

	# add page 1 from input1 to output document, unchanged
	# output.addPage(input1.getPage(0))
	# add some Javascript to launch the print window on opening this PDF.
	# the password dialog may prevent the print dialog from being shown,
	# comment the the encription lines, if that's the case, to try this out
	output.addJS("this.print({bUI:true,bSilent:false,bShrinkToFit:true});")

	# encrypt your new PDF and add a password
	password = ""
	output.encrypt(password)

	# finally, write "output" to document-output.pdf
	hue = filename + ".pdf"
	outputStream = file(os.path.join(filename + ".pdf"), "wb")
	output.write(outputStream)


if __name__ == "__main__":  
	start_time = time.time()
	for filename in os.listdir(paper_dir):
		interval_time = time.time()
		if filename.startswith("DR-") and filename.endswith(".pdf"):
			split(filename[:-4], os.path.join(paper_dir, filename))
		print("--- Done %s with %s seconds ---" % (filename, time.time() - interval_time))
	print("--- Done all! %s seconds ---" % (time.time() - start_time))
