import urllib2
from bs4 import BeautifulSoup
from pprint import  pprint
import json
from nltk.tokenize import sent_tokenize, word_tokenize


with open('/Users/sakshipratap/PycharmProjects/GVU/project/apiai-weather-webhook-sample-master/labData.json') as json_data:
    json_data = json.load(json_data)
    for i in json_data:
        i["description"] = sent_tokenize(i["description"]) if i["description"] else []
    with open('labData.json', 'w') as outfile:
        json.dump(json_data, outfile)

with open(
        '/Users/sakshipratap/PycharmProjects/GVU/project/apiai-weather-webhook-sample-master/peopleData.json') as json_data:
    json_data = json.load(json_data)
    for i in json_data:
        i["description"] = sent_tokenize(i["description"]) if i["description"] else []
    with open('peopleData.json', 'w') as outfile:
        json.dump(json_data, outfile)



# url = "http://www.gvu.gatech.edu/people/gvu-administration"  # change to whatever your url is
#
# page = urllib2.urlopen(url).read()
# soup = BeautifulSoup(page, "html.parser")
#
# faculties = soup.find_all( "td")
#
# labData=[]
# for faculty in faculties:
#     current = {
#         'name': faculty.find ("h2", {"class":"facultyname"} ).text,
#         'title': faculty.find ("div", {"class":"facultytitle"} ).find ("div", {"class":"field-item even"} ).text if faculty.find ("div", {"class":"facultytitle"} ).find ("div", {"class":"field-item even"} ) else None,
#         'dept': faculty.find ("div", {"class":"facultydept"} ).find ("div", {"class":"field-item even"} ).text if faculty.find ("div", {"class":"facultydept"} ).find ("div", {"class":"field-item even"} ) else None,
#         'specialty':faculty.find ("div", {"class":"facultyspecialty"} ).find ("div", {"class":"field-item even"} ).text if faculty.find ("div", {"class":"facultyspecialty"} ).find ("div", {"class":"field-item even"} ) else None,
#         'description':faculty.find ("div", {"class":"facultydescription"} ).find ("div", {"class":"field-item even"} ).text if faculty.find ("div", {"class":"facultydescription"} ).find ("div", {"class":"field-item even"} ) else None,
#
#     }
#     labData.append(current)
#
#
#
# with open('peopleData.json', 'w') as outfile:
#     json.dump(labData, outfile)

#
# url = "http://gvu.gatech.edu/research/labs"  # change to whatever your url is
#
# page = urllib2.urlopen(url).read()
# soup = BeautifulSoup(page, "html.parser")
# labData=[]
# labs=soup.find_all("div", {"class":"labcontainer"} )
# for lab in labs:
#     current = {
#         'name': lab.h2.text,
#         'people':(lab.find("div",{"class":"labcontent"}).text).split(":")[1].split(",") if len((lab.find("div",{"class":"labcontent"}).text).split(":"))>1 else [],
#         'description':(lab.find("div",{"class":"field-items"}).text) if lab.find("div",{"class":"field-items"}) else None,
#         'a': lab.find("a",href=True)["href"]
#     }
#     print(lab.a)
#     labData.append(current)
#
# with open('labData.json', 'w') as outfile:
#     json.dump(labData, outfile)


#
# url = "http://gvu.gatech.edu/research/projects"  # change to whatever your url is
#
# page = urllib2.urlopen(url).read()
# soup = BeautifulSoup(page, "html.parser")
# projectData=[]
# project=soup.find_all("div", {"class":"projectcontainer"} )
# for lab in project:
#     a=lab.find("div",{"class","projectcontent"}).find("a", href=True)
#     current = {
#         'name': lab.h4.text,
#         'link': a["href"],
#         'projectLab': a.text,
#         "description":lab.find("div",{"class","field-item"}).text if lab.find("div",{"class","field-item"}) else None
#
#           }
#     projectData.append(current)
# pprint(projectData)
# with open('projectData.json', 'w') as outfile:
#     json.dump(projectData, outfile)


# url = "http://gvu.gatech.edu/event/upcoming"  # change to whatever your url is
#
# page = urllib2.urlopen(url).read()
# soup = BeautifulSoup(page, "html.parser")
# eventData=[]
# event = soup.find_all("td" )
# for i in xrange(len(event)/2):
#     current ={
#         "name":event[i*2+1].text,
#         "date":event[i*2].text,
#     }
#
#     eventData.append(current)
# pprint(eventData)
# with open('eventData.json', 'w') as outfile:
#     json.dump(eventData, outfile)
#
# url = "http://www.gvu.gatech.edu/event/brown-bag-archive"  # change to whatever your url is
#
# #
# page = urllib2.urlopen(url).read()
# soup = BeautifulSoup(page, "html.parser")
# projectData=[]
# project=soup.find_all("div", {"class":"bb-container"} )
# for lab in project:
#     a=lab.find("a", href=True)
#     current = {
#         'name': lab.h2.text,
#         'link': a["href"],
#         "date":lab.findAll("div",{"class","bb-content"})[1].text if len(lab.findAll("div",{"class","bb-content"}))>1 else None
#
#           }
#     projectData.append(current)
# pprint(projectData)
# with open('brownBagRecentData.json', 'w') as outfile:
#     json.dump(projectData, outfile)
#
#
#
# url = "http://www.gvu.gatech.edu/news"  # change to whatever your url is
#
# #
# page = urllib2.urlopen(url).read()
# soup = BeautifulSoup(page, "html.parser")
# projectData=[]
# project=soup.find("ul", {"class":"hg-feed-list"} )
# for lab in project.findAll("a", href=True):
#     a = lab["href"]
#     projectData.append(a)
# pprint(projectData)
# with open('newsData.json', 'w') as outfile:
#     json.dump(projectData, outfile)
#
