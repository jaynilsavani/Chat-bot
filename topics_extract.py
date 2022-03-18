import spacy

# open the PDF file
fileName = 'slides_8.pdf'
pdfFile = open(fileName, 'rb')

# create PDFFileReader object to read the file
pdfReader = PdfFileReader(pdfFile)

numOfPages = pdfReader.getNumPages()
input = ''
for i in range(0, numOfPages):
	pageObj = pdfReader.getPage(i)
	input += pageObj.extractText()
# close the PDF file object
pdfFile.close()

def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist
input=' '.join(unique_list(input.split())) 

nlp = spacy.blank('en')
nlp.add_pipe('dbpedia_spotlight')
doc = nlp(input)
output = []
for ent in doc.ents:
    output.append(ent._.dbpedia_raw_result['@URI']) 

newfile = open('topics.txt','a')
print(' ', file = newfile)
print('--------------------------------', file = newfile)
print(fileName, file = newfile)
print('--------------------------------', file = newfile)

for x in output:
    y = x.split('/')
    print(y[len(y) - 1], file = newfile)
newfile.close()       