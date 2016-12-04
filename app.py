#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
import json
import random


# Flask app should start in global layout
app = Flask(__name__)
with open('data/labData.json') as json_data:
    labData = json.load(json_data)

with open('data/aboutData.json') as json_data:
    aboutData = json.load(json_data)

with open('data/peopleData.json') as json_data:
    peopleData = json.load(json_data)

with open('data/brownBagRecentData.json') as json_data:
    eventData = json.load(json_data)



@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    result = {}

    if req.get("result").get("contexts") and len(req.get("result").get("contexts"))>0:
        context =req.get("result").get("contexts")[-1]
        if context.get("name") == 'people_detail'\
                and len(context.get("parameters").get("first_names")+context.get("parameters").get("last_names"))>0 \
                and (context.get("parameters").get("parameter")) in peopleData[0] \
                and not (req.get("result").get("parameters").get("Organization")):
            req["result"] = context
            req.get("result")["action"] = "people_info_general"

        elif context.get("name") == 'lab_detail' and (context.get("parameters").get("lab_names"))\
                and (context.get("parameters").get("parameter")) in labData[0] and not (req.get("result").get("parameters").get("Organization")):
            req["result"] = context
            req.get("result")["action"]= "lab_info_general"


    #GVU about
    if req.get("result").get("action") == "gvu_about":
        if req.get("result").get("parameters").get("questions")=='where':
            result = getGVUInfo('location')
        elif req.get("result").get("parameters").get("questions")=='how':
            result = getGVUInfo('quality')
        else:
            result = getGVUInfo('about')

    #GVU how to contribute
    elif req.get("result").get("action") == "gvu_info_contribution":
        result = getGVUInfo('contribute')


    # GVU parameters
    elif req.get("result").get("action") == "gvu_info_general":
        param = req.get("result").get("parameters").get("parameter")
        result = getGVUInfo(param)

    # GVU event
    elif req.get("result").get("action") == "gvu_events":
        result = getGVUEvents()

    #Lab basic
    elif req.get("result").get("action") == "lab_basic":
        result = getLabBasic()

    # Lab work
    elif req.get("result").get("action") == "lab_detail":
        key = req.get("result").get("parameters").get("lab_names")
        result = getInfo("description",key,"lab")

    # Lab params
    elif req.get("result").get("action") == "lab_info_general":
        key = req.get("result").get("parameters").get("lab_names")
        param = req.get("result").get("parameters").get("parameter")
        result = getInfo(param, key, "lab")


    #People basic
    elif req.get("result").get("action") == "people_basic":
        result = getPeopleBasic()

    # People work
    elif req.get("result").get("action") == "people_detail":
        key = req.get("result").get("parameters").get("first_names")+" "+req.get("result").get("parameters").get("last_names")
        result = getInfo("description",key,"people")

    # People params
    elif req.get("result").get("action") == "people_info_general":
        key = req.get("result").get("parameters").get("first_names") + " " + req.get("result").get("parameters").get(
            "last_names")
        param = req.get("result").get("parameters").get("parameter")
        result = getInfo(param,key,"people")

    #Research Info
    elif req.get("result").get("action") == "research_lab_matching":
        param = req.get("result").get("parameters").get("research_areas")
        result  =getResearchInfo(param)

    res = makeWebhookAboutResult(result)


    print res
    return res


def getInfo(param, key, type):
    line1 = "Sorry, I am unable to find any information about "+key.strip()+"'s "+param+". Sometimes the variation in words confuses me"
    line2 = ""
    if type == 'lab':
        data = labData
    else:
        data = peopleData

    index = next((index for (index, d) in enumerate(data) if
                  key.lower() in d["name"].lower() or d["name"].lower() in key.lower()), -1)
    if index >= 0:
        if param == "description":
                line1 = data[index].get(param)[0] if data[index].get(param) else line1
                count = len(data[index].get(param))
                if count > 1:
                    indexes = random.sample(range(1, count), (count+3)/4)
                    results = []
                    for i in indexes:
                        results.append(data[index].get(param)[i])
                    line2 = " ".join(results)
        elif data[index].get(param):
            if not param  == "people":
                line1 = key.strip()+"'s "+param+" is "+data[index].get(param)
            else:
                line1 = ", ".join(data[index].get(param))+ " work at "+key


    return {"result":line1+line2}


def getGVUInfo(param):
    line1 = aboutData.get(param)['main']
    line2 = ""
    count = len(aboutData.get(param)['description'])
    if count>0:
        index = random.randint(0,count-1)
        line2 = "\n"+aboutData.get(param)['description'][index]
    return {"result":line1+line2}


def getGVUEvents():
    line1 = "GVU hosts seminars like the Brown Bag Series to talk about the research. "
    count = len(eventData)
    index = random.randint(0, count - 1)
    data  = eventData[index]
    print data
    line2 = "A session on "+data["date"]+" was part of the "+data["name"]+"\n Here is the link: http://gvu.gatech.edu"+data.get("link")
    return {"result":line1+line2}


def getLabBasic():
    count = len(labData)
    indexes = random.sample(range(1, count), 3)
    results=[]
    line1 = "We have " + str(count) + " labs in GVU working on the next computing revolution. "
    for i in indexes:
        results.append(labData[i]["name"])
    line2 = "Some of the labs include the " + ", ".join(results)

    return {"result":line1+line2}


def getPeopleBasic():
    count = len(peopleData)
    indices = random.sample(range(1, count), 3)
    results = []
    line1 = "We have more than " + str(count) + " researchers and administrators associated with GVU working on the next computing revolution. "
    for i in indices:
        results.append(peopleData[i]["name"])
    line2 = ", ".join(results)+"  are all part of GVU"

    return {"result": line1 + line2}

def getResearchInfo(param):
    results = []
    line1 = "Unfortunately, I cannot find anyone working in that area. We have researchers working in AI, HCI, Ubicomp among others."
    indices = [i for i, x in enumerate(labData) if param.lower() in " ".join(x["description"]).lower()]
    if len(indices)>0:
        for i in indices:
            results.append(labData[i]["name"])

        line1 = "Some of the labs working in this area include the " + ", ".join(results)

    return {"result": line1}


def makeWebhookAboutResult(data):
    speech = "Sorry I am not sure what you are looking for."
    if  data.get("result"):
        speech = data.get("result")
    return {
            "speech": speech,
            "displayText": speech,
            # "data": data,
            # "contextOut": [],
            "source": "apiai-weather-webhook-sample"
        }




if __name__ == '__main__':
    with open('data/temp.json') as json_data:
        req = json.load(json_data)
    processRequest(req)
    # port = int(os.getenv('PORT', 5000))
    #
    # print "Starting app on port %d" % port
    #
    # app.run(debug=False, port=port, host='0.0.0.0')
    #
    # app.run(debug=True, port=port, host='0.0.0.0')
