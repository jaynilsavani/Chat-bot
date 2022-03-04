import pandas as pd
from rdflib import Graph,Namespace, RDF, RDFS, URIRef, Literal
from rdflib.namespace import FOAF, DC, XSD, OWL
import os
os.chdir(os.path.dirname(__file__))

def university():
    graph.add((UNIDATA.Concordia_University, RDF.type, UNI.University))
    graph.add((UNIDATA.Concordia_University, RDFS.label, Literal("Concordia University", lang="en")))
    graph.add((UNIDATA.Concordia_University, RDFS.seeAlso, URIRef(DBP.Concordia_University)))

def course():
    course_data = pd.read_csv(os.getcwd() + os.sep +"combine.csv",encoding="unicode_escape")
    for subject in course_data["Subject"].unique():
        graph.add((URIRef(UNIDATA+ str(subject)), RDF.type, UNI.Subject))
    for i, row in course_data.iterrows():
        course_uniqueID = URIRef(UNIDATA+row["Subject"]+str(row["Catalog"]))
        graph.add((course_uniqueID, RDF.type, UNI.Course))
        graph.add((course_uniqueID, FOAF.name, Literal(row["Long Title"])))
        graph.add((course_uniqueID, UNI.subjectOf , Literal(row["Subject"])))
        graph.add((course_uniqueID, DC.identifier, Literal(row["Catalog"])))
        graph.add((course_uniqueID, DC.description, Literal(row["Descr"])))
        
def get_folder_details():
   
    for root, dirs,files in os.walk(os.getcwd() + os.sep +'courses'):
        for filename in files:
            file_path = os.path.join(root,filename)
            splitted_file_path = file_path.split(os.sep)
            if splitted_file_path[-3] != "courses":
                course_name = splitted_file_path[-3]
                content_type = splitted_file_path[-2]
                lec_no = splitted_file_path[-1].split("_")[1].split(".")[0]
                uri = file_path
               
                """ data = {}
                data["course_name"] = splitted_file_path[-3]
                data["content_type"] = splitted_file_path[-2]
                data["lec_no"] = splitted_file_path[-1].split("_")[1].split(".")[0]
                data["uri"] = file_path
                course_list.append(data)"""
                lec = URIRef(UNIDATA +course_name+content_type+lec_no)
                graph.add((lec, RDF.type, UNI.Lecture))
                ss = course_name.upper()
                graph.add((lec, DC.isPartOf, UNIDATA.ss))
                graph.add((lec, DC.identifier, Literal(str(lec_no))))
                if content_type == "sildes":
                    graph.add((lec, UNI.slideIs, URIRef(file_path)))
                """if content_type == "worksheets":
                        graph.add((lec, UNI.worksheetIs, URIRef(file_path)))"""
                


DBP = Namespace("http://dbpedia.org/resource/")
UNI = Namespace("http://unibot.io/schema#")
UNIDATA = Namespace("http://unibot.io/data#")

graph= Graph()

graph.bind('dbp',DBP)
graph.bind('uni',UNI)
graph.bind('unidata',UNIDATA)


university()
course()
get_folder_details()

graph.serialize(destination='knowledge_graph.ttl', format='turtle', encoding='utf-8')
graph.serialize("knowledge_graph_in_nt_format.nt", format="nt")