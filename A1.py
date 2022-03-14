import pandas as pd
from rdflib import Graph,Namespace, RDF, RDFS, URIRef, Literal
from rdflib.namespace import FOAF, DC, XSD, OWL
import os
from urllib.parse import quote
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
                if content_type == "slides":
                    graph.add((lec, UNI.slideIs, URIRef(quote(file_path))))
                if content_type == "worksheets":
                    graph.add((lec, UNI.worksheetIs, URIRef(quote(file_path))))   
                    
    lec_1_IS_description = "This week professor covered Intelligent Systems Introduction."
    lec_1_IS_name = "Intelligent Systems Introduction"
    lec_2_IS_description = "This week professor covered Knowledge Graphs."
    lec_2_IS_name = "Knowledge Graphs"
    lec_3_IS_description = "This week professor covered Vocabularies & Ontologies."
    lec_3_IS_name = "Vocabularies & Ontologies "
    lec_4_IS_description = "This week professor covered Knowledge Base Queries & SPARQL."
    lec_4_IS_name = "Knowledge Base Queries & SPARQL"
    lec_5_IS_description = "This week professor covered Knowledge Base Design & Applications."
    lec_5_IS_name = "Knowledge Base Design & Applications"
    lec_6_IS_description = "This week professor covered Personalization, Collaborative Filtering & Content-based recommendation."
    lec_6_IS_name = "Recommender Systems"
    lec_7_IS_description = "This week professor covered Machine Learning for Intelligent Systems."
    lec_7_IS_name = "Machine Learning for Intelligent Systems"

    lec_1_SCM_description = "This week professor covered Introduction to Software Evolution and Software Aging."
    lec_1_SCM_name = "Introduction to Software Evolution and Software Aging"
    lec_2_SCM_description = "This week professor covered Software Maintenance and program comprehension."
    lec_2_SCM_name = "Software Maintenance and program comprehension"
    lec_3_SCM_description = "This week professor covered Program Analysis and Software Traceability"
    lec_3_SCM_name = "Program Analysis and Software Traceability"
    lec_4_SCM_description = "This week professor covered Program Analysis: Data flow Analysis."
    lec_4_SCM_name = "Program Analysis: Data flow Analysis"
    lec_5_SCM_description = "This week professor covered Control flow analysis."
    lec_5_SCM_name = "Control flow analysis"
    lec_6_SCM_description = "This week professor covered Refactoring."
    lec_6_SCM_name = "Refactoring"
    lec_7_SCM_description = "This week professor covered Software and Data Migration."
    lec_7_SCM_name = "Software and Data Migration"
    lec_8_SCM_description = "This week professor covered Program Slicing."
    lec_8_SCM_name = "Program Slicing"

    graph.add( (UNIDATA.COMP6741slides1, RDFS.comment, Literal(lec_1_IS_description)) )
    graph.add( (UNIDATA.COMP6741slides2, RDFS.comment, Literal(lec_2_IS_description)) )
    graph.add( (UNIDATA.COMP6741slides3, RDFS.comment, Literal(lec_3_IS_description)) )
    graph.add( (UNIDATA.COMP6741slides4, RDFS.comment, Literal(lec_4_IS_description)) )
    graph.add( (UNIDATA.COMP6741slides5, RDFS.comment, Literal(lec_5_IS_description)) )
    graph.add( (UNIDATA.COMP6741slides6, RDFS.comment, Literal(lec_6_IS_description)) )
    graph.add( (UNIDATA.COMP6741slides7, RDFS.comment, Literal(lec_7_IS_description)) )
    
    graph.add( (UNIDATA.SOEN6431slides1, RDFS.comment, Literal(lec_1_SCM_description)) )
    graph.add( (UNIDATA.SOEN6431slides2, RDFS.comment, Literal(lec_2_SCM_description)) )
    graph.add( (UNIDATA.SOEN6431slides3, RDFS.comment, Literal(lec_3_SCM_description)) )
    graph.add( (UNIDATA.SOEN6431slides4, RDFS.comment, Literal(lec_4_SCM_description)) )
    graph.add( (UNIDATA.SOEN6431slides5, RDFS.comment, Literal(lec_5_SCM_description)) )
    graph.add( (UNIDATA.SOEN6431slides6, RDFS.comment, Literal(lec_6_SCM_description)) )
    graph.add( (UNIDATA.SOEN6431slides7, RDFS.comment, Literal(lec_7_SCM_description)) )
    graph.add( (UNIDATA.SOEN6431slides8, RDFS.comment, Literal(lec_8_SCM_description)) )
    
    graph.add( (UNIDATA.COMP6741slides1, FOAF.name, Literal(lec_1_IS_name)) )
    graph.add( (UNIDATA.COMP6741slides2, FOAF.name, Literal(lec_2_IS_name)) )
    graph.add( (UNIDATA.COMP6741slides3, FOAF.name, Literal(lec_3_IS_name)) )
    graph.add( (UNIDATA.COMP6741slides4, FOAF.name, Literal(lec_4_IS_name)) )
    graph.add( (UNIDATA.COMP6741slides5, FOAF.name, Literal(lec_5_IS_name)) )
    graph.add( (UNIDATA.COMP6741slides6, FOAF.name, Literal(lec_6_IS_name)) )
    graph.add( (UNIDATA.COMP6741slides7, FOAF.name, Literal(lec_7_IS_name)) )
    
    graph.add( (UNIDATA.SOEN6431slides1, FOAF.name, Literal(lec_1_SCM_name)) )
    graph.add( (UNIDATA.SOEN6431slides2, FOAF.name, Literal(lec_2_SCM_name)) )
    graph.add( (UNIDATA.SOEN6431slides3, FOAF.name, Literal(lec_3_SCM_name)) )
    graph.add( (UNIDATA.SOEN6431slides4, FOAF.name, Literal(lec_4_SCM_name)) )
    graph.add( (UNIDATA.SOEN6431slides5, FOAF.name, Literal(lec_5_SCM_name)) )
    graph.add( (UNIDATA.SOEN6431slides6, FOAF.name, Literal(lec_6_SCM_name)) )
    graph.add( (UNIDATA.SOEN6431slides7, FOAF.name, Literal(lec_7_SCM_name)) )
    graph.add( (UNIDATA.SOEN6431slides8, FOAF.name, Literal(lec_8_SCM_name)) )
    
    COMP6741_description = "Intelligent Systems. This subject is of 4 credits. Knowledge representation and reasoning. Uncertainty and conflict resolution. Design of intelligent systems. Grammar-based, rule-based, and blackboard architectures. A project is required. Laboratory: two hours per week."
    SOEN6431_description = "The course addresses both technical and managerial views of software comprehension and software maintenance issues. Topics covered in this course include: cognitive models, software visualization, CASE tools, reverse engineering, static and dynamic source code analysis, software configuration management, and introduction to current research topics in software maintenance and program comprehension. A project is required."
    
    graph.add( (UNIDATA.COMP6741, RDFS.comment, Literal(COMP6741_description) ))
    graph.add( (UNIDATA.SOEN6431, RDFS.comment, Literal(SOEN6431_description) ))
        
DBP = Namespace("http://dbpedia.org/resource/")
UNI = Namespace("http://unibot.io/schema#")
UNIDATA = Namespace("http://unibot.io/data#")

graph= Graph()

graph.bind('dbp',DBP)
graph.bind('uni',UNI)
graph.bind('unidata',UNIDATA)
graph.bind('dc',DC)
graph.bind('rdfs',RDFS)
graph.bind('rdf',RDF)
graph.bind('foaf',FOAF)


university()
course()
get_folder_details()

graph.serialize(destination='knowledge_graph.ttl', format='turtle', encoding='utf-8')
graph.serialize("knowledge_graph_in_nt_format.nt", format="nt")