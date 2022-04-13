# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import requests
import json
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset
import re
import string
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

PREFIXES = '''
            PREFIX dbp: <http://dbpedia.org/resource/>
            PREFIX dc: <http://purl.org/dc/elements/1.1/>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX uni: <http://unibot.io/schema#>
            PREFIX unidata: <http://unibot.io/data#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            '''
def runQuery(query):
    fuseki_url = 'http://localhost:3030/IS/sparql'
    # print('Fuseki Query: ' + query)
    httpresponse = requests.post(fuseki_url, data={'query': query})
    result = json.loads(httpresponse.text)
    # print('Fuseki Response:')
    # print(result)
    return result

class ActionCourseDetails(Action):

    def name(self) -> Text:
        return "action_course_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course_code = tracker.slots['course_code']

        course_name = course_code.split(" ")
        answer = ""
        result = ""
        if(len(course_name) != 2):
            answer = "Invalid course code."
        else:
            temp = '''SELECT ?course_outline ?description
                                  WHERE {
                                    ?course rdf:type uni:Course ;
                                    uni:subjectOf "%s" ;
                                    dc:identifier "%s" ;
                                    dc:description ?description ;
                                    OPTIONAL { ?course rdfs:seeAlso ?course_outline }
                                }'''%(course_name[0],course_name[1])
            query = PREFIXES + temp
            result = runQuery(query)
            headers = result['head']['vars']
            if len(result['results']['bindings']) > 0 :
                for header in headers:
                    response = ""
                    if header in result['results']['bindings'][0].keys():
                        response = result['results']['bindings'][0][header]['value']
                        answer = answer + header.title() + ": " + response + " \n"
            else:
                answer = "Course data is not available."            

        dispatcher.utter_message(text=f"{answer}")

        return []

class ActionStudentsDetails(Action):

    def name(self) -> Text:
        return "action_student_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        studentName = tracker.slots['student_name']
        result = ""
        temp = '''SELECT ?topics
                    WHERE {  
                        ?course a uni:CompletedCourse ;
                            uni:studentIs ?studentName ;		
                            uni:courseIs ?courses .
                        ?studentName a uni:Student ;
                            foaf:givenName "%s" .
                        ?name rdf:type uni:Lecture ;
                            dc:isPartOf ?courses ;
                            uni:topicIs ?topics .	
                        }'''%(studentName)
        query = PREFIXES + temp
        result = runQuery(query)
        headers = result['head']['vars']
        answer = "Topics: \n"
        if len(result['results']['bindings']) > 0 :
            for result in result['results']['bindings']:
                for header in headers:
                    answer = answer + " " + result[header]['value']
                answer = answer + "\n"
        else:
            answer = "Student data is not available."                   

        dispatcher.utter_message(text=f"{answer}")

        return []

class ActionLectureDetails(Action):

    def name(self) -> Text:
        return "action_lecture_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        lecture_number = tracker.slots['lecture_number'][:1]
        keyword = tracker.slots['keyword']
        course_code = tracker.slots['course_code'].split(" ")

        answer = ""
        result = ""
        if(len(course_code) != 2):
            answer = "Invalid subject code."
        content_type = "uni:Lab"
        if(keyword == "lecture"): 
            content_type = "uni:Lecture"

        temp = '''SELECT ?topics
                    WHERE {  
                            ?subject rdf:type uni:Course ;
                                uni:subjectOf "%s" ;
                                dc:identifier "%s" .
                            ?course rdf:type %s ;
                            dc:isPartOf  ?subject;
                            dc:identifier "%s" ;
                            uni:topicIs ?topics .		
                        }'''%(course_code[0],course_code[1],content_type,lecture_number)
        query = PREFIXES + temp
        result = runQuery(query)
        headers = result['head']['vars']
        answer = ""
        if len(result['results']['bindings']) > 0 :
            answer = "Topics: \n"
            for result in result['results']['bindings']:
                for header in headers:
                    answer = answer + " " + result[header]['value'].split("/")[-1]+ "     " + result[header]['value']
                answer = answer + "\n"
        else:
            answer = "Lecture data is not available."                

        dispatcher.utter_message(text=f"{answer}")

        return []

class ActionTopicDetails(Action):

    def name(self) -> Text:
        return "action_topic_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        topic= tracker.slots['topic']
        material = tracker.slots['material']
        topicName = "dbp:"+topic
        result = ""
        temp = ""
        if(material == "courses"):
            temp = '''SELECT DISTINCT ?name
                WHERE{
                    ?lec a uni:Lecture ;
                        dc:isPartOf ?course ;
                        uni:topicIs %s .
                    ?course a uni:Course ;
                            foaf:name ?name .
                }'''%(topicName)
        if(material == "lecture"):   
            temp = '''SELECT ?names
                WHERE{
                    ?lec a uni:Lecture ;
                    uni:topicIs %s ;
                        foaf:name ?names .
                }'''%(topicName)

        query = PREFIXES + temp
        result = runQuery(query)
        headers = result['head']['vars']

        answer = ""
        if(material == "courses"):
            answer = "Courses: \n"
        if(material == "lecture"):
            answer = "Lectures: \n"    
        if len(result['results']['bindings']) > 0 :
            for result in result['results']['bindings']:
                for header in headers:
                    answer = answer + " " + result[header]['value']
                answer = answer + "\n"
        else:
            answer = "Topic data is not available."                   

        dispatcher.utter_message(text=f"{answer}")

        return []

class ActionMultipleLectureDetails(Action):

    def name(self) -> Text:
        return "action_multiple_lecture_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        keyword = tracker.slots['content_type']
        courseCode = tracker.slots['course_code']
        lecture1 = tracker.slots['lecture1'][:1]
        lecture2 = tracker.slots['lecture2'][:1]

        courseName = "unidata:"+courseCode
        result = ""
        temp = ""
        if(keyword == "worksheets"):
            temp = '''SELECT ?work_sheets
                WHERE{
                            ?lec a uni:Lecture ;
                                dc:isPartOf %s ;
                                uni:worksheetIs ?work_sheets .
                    {?lec dc:identifier "%s" ; }
                    UNION
                    {?lec dc:identifier "%s" ; }
                        }'''%(courseName, lecture1, lecture2)
        if(keyword == "slides"):
            temp = '''SELECT ?slides
                WHERE{
                            ?lec a uni:Lecture ;
                                dc:isPartOf %s ;
                                uni:slideIs ?slides .
                    {?lec dc:identifier "%s" ; }
                    UNION
                    {?lec dc:identifier "%s" ; }
                        }'''%(courseName, lecture1, lecture2)                
        query = PREFIXES + temp
        result = runQuery(query)
        headers = result['head']['vars']
        answer = keyword.capitalize()+": \n"
        if len(result['results']['bindings']) > 0 :
            for result in result['results']['bindings']:
                for header in headers:
                    answer = answer + " " + result[header]['value']
                answer = answer + "\n"
        else:
            answer = "Lecture data is not available."                   

        dispatcher.utter_message(text=f"{answer}")

        return []        

class ActionDepartmentDetails(Action):

    def name(self) -> Text:
        return "action_department_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        department = tracker.slots['department']

        result = ""
        temp = '''SELECT ?name
                    WHERE {
                            ?course rdf:type uni:Course ;
                            uni:subjectOf "%s" ;
                            foaf:name ?name.
                        }'''%(department)               
        query = PREFIXES + temp
        result = runQuery(query)
        headers = result['head']['vars']
        answer = "Subjects: \n"
        if len(result['results']['bindings']) > 0 :
            for result in result['results']['bindings']:
                for header in headers:
                    answer = answer + " " + result[header]['value']
                answer = answer + "\n"
        else:
            answer = "Department data is not available."                   

        dispatcher.utter_message(text=f"{answer}")

        return []   

class ActionSubjectNameDetails(Action):

    def name(self) -> Text:
        return "action_subject_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        subjectName = tracker.slots['subject_name']

        result = ""
        temp = '''SELECT ?name
                    WHERE{
                        ?course a uni:Course ;  
                        foaf:name ?name .
                        FILTER contains((?name),"%s")  
                }'''%(subjectName)               
        query = PREFIXES + temp
        result = runQuery(query)
        headers = result['head']['vars']
        answer = "Subjects: \n"
        if len(result['results']['bindings']) > 0 :
            for result in result['results']['bindings']:
                for header in headers:
                    answer = answer + " " + result[header]['value']
                answer = answer + "\n"
        else:
            answer = "Subject data is not available."                   

        dispatcher.utter_message(text=f"{answer}")

        return []  

class ActionRetrieveStudentDetails(Action):

    def name(self) -> Text:
        return "action_retrieve_student_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        studentName = "unidata:"+tracker.slots['student_name']

        result = ""
        temp = '''SELECT (COUNT(?course) as ?total)
                WHERE{
                    ?course a uni:CompletedCourse ;
                        uni:studentIs %s .
                }'''%(studentName)               
        query = PREFIXES + temp
        result = runQuery(query)
        headers = result['head']['vars']
        answer = "Completed Course: \n"
        if len(result['results']['bindings']) > 0 :
            for result in result['results']['bindings']:
                for header in headers:
                    answer = answer + " " + result[header]['value']
                answer = answer + "\n"
        else:
            answer = "Student data is not available."                   

        dispatcher.utter_message(text=f"{answer}")

        return []                 

class ActionRetrieveStudentGradeDetails(Action):

    def name(self) -> Text:
        return "action_retrieve_student_grade_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        studentName = "unidata:"+tracker.slots['student_name']
        grade = tracker.slots['grade']

        result = ""
        temp = '''SELECT ?name
                    WHERE{
                        ?course a uni:CompletedCourse ;
                                uni:studentIs %s ;
                                uni:grade "%s" ;
                                uni:courseIs ?courseID .
                        ?courseID a uni:Course ;
                                foaf:name ?name .
                    }'''%(studentName, grade)               
        query = PREFIXES + temp
        result = runQuery(query)
        headers = result['head']['vars']
        answer = "Subjects: \n"
        if len(result['results']['bindings']) > 0 :
            for result in result['results']['bindings']:
                for header in headers:
                    answer = answer + " " + result[header]['value']
                answer = answer + "\n"
        else:
            answer = "Student data is not available."                   

        dispatcher.utter_message(text=f"{answer}")

        return []                 

class ActionRetrieveLectureContentDetails(Action):

    def name(self) -> Text:
        return "action_retrieve_lecture_contents"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        lecture_number = tracker.slots['lecture_number'][:1]
        keyword = tracker.slots['keyword']
        course_code = tracker.slots['course_code'].replace(" ","")

        result = ""
        temp = ""
        if(keyword == "lecture"):
            temp = '''SELECT ?slide ?topics ?work_sheets
                        WHERE{
                            ?lec a uni:Lecture ;
                                    dc:identifier "%s" ;                                                  
                                    dc:isPartOf unidata:%s ;
                            uni:slideIs ?slide ;
                            uni:topicIs ?topics .
                    OPTIONAL {?lec uni:worksheetIs ?work_sheets} 
                }'''%(lecture_number, course_code)    
        if(keyword == "lab"):
               temp = '''SELECT ?slide ?topics ?work_sheets
                        WHERE{
                            ?lec a uni:Lab ;
                                    dc:identifier "%s" ;                                                  
                                    dc:isPartOf unidata:%s ;
                            uni:slideIs ?slide ;
                            uni:topicIs ?topics .
                    OPTIONAL {?lec uni:worksheetIs ?work_sheets} 
                }'''%(lecture_number, course_code)                 
        query = PREFIXES + temp
        result = runQuery(query)
        headers = result['head']['vars']
        answer = "Result: \n"
        content = "true"
        workSheetContent = "true"
        if len(result['results']['bindings']) > 0 :
            for result in result['results']['bindings']:
                for header in headers:
                    if header in result.keys():
                        if(header == "slide" and content == "true"):
                            content = "false"
                            answer = answer + " " + result[header]['value']+"\n"        
                        elif(header == "work_sheets" and workSheetContent == "true"):
                            workSheetContent = "false"
                            answer = answer + " " + result[header]['value']+"\n"        
                        elif(header == "topics"):  
                            answer = answer + " " + result[header]['value']        
                answer = answer + "\n"
        else:
            answer = "Data is not available."                   

        dispatcher.utter_message(text=f"{answer}")

        return []          