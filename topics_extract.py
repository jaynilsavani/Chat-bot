import spacy
import csv
import os
from PyPDF2 import PdfFileReader, PdfFileWriter

temp = []
for root, dirs,files in os.walk(os.getcwd() + os.sep +'courses'):
     for fileName in files:
            file_path = os.path.join(root,fileName)
            splitted_file_path = file_path.split(os.sep)
            if splitted_file_path[-3] != "courses":
                course_name = splitted_file_path[-3]
                content_type = splitted_file_path[-2]
                if(content_type == "slides"):
                    lec_no = splitted_file_path[-1].split("_")[1].split(".")[0]
                    pdfFile = open(file_path, 'rb')

                    # create PDFFileReader object to read the file
                    pdfReader = PdfFileReader(pdfFile)
                    output_file = open("output.txt", "w", encoding="utf-8")

                    numOfPages = pdfReader.getNumPages()
                    input = ''
                    for i in range(0, numOfPages):
                        pageObj = pdfReader.getPage(i)
                        input += pageObj.extractText()
                        output_file.write(input)
                        
                    # close the PDF file object
                    pdfFile.close()
                    output_file.close()

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

                    with open('topics.csv', 'a', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)

                        for x in output:
                            y = x.split('/')
                            temp.append([course_name, lec_no, y[len(y) - 1]])
                            
with open('topics.csv', 'a', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    header = ['course', 'lec', 'topic']
    writer.writerow(header)
    for x in temp:
        # write the data
        writer.writerow(x) 

from more_itertools import unique_everseen
with open('topics.csv', 'r') as f, open('final_topics.csv', 'w') as out_file:
    out_file.writelines(unique_everseen(f))                         

file = 'topics.csv'
if(os.path.exists(file) and os.path.isfile(file)):
  os.remove(file)