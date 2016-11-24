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
with open('labData.json') as json_data:
    labData = json.load(json_data)

with open('aboutData.json') as json_data:
    aboutData = json.load(json_data)

with open('peopleData.json') as json_data:
    peopleData = json.load(json_data)



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
# @app.route('/webhook2')
# def processRequest():
#     with open('temp.json') as json_data:
#         req = json.load(json_data)
    res = {}
    if req.get("result").get("action") == "lab_basic":
        data = getLabBasic()
        res = makeWebhookLabResult(data)

    elif req.get("result").get("action") == "gvu_about":
        data = getGVUInfo('about')
        res = makeWebhookAboutResult(data)

    elif req.get("result").get("action") == "gvu_info_contribution":
        data = getGVUInfo('contribute')
        res = makeWebhookAboutResult(data)

    elif req.get("result").get("action") == "gvu_info_general":
        param = req.get("result").get("parameters").get("parameter1")
        data = getGVUInfo(param)
        res = makeWebhookAboutResult(data)

    elif req.get("result").get("action") == "people_about":

        key = req.get("result").get("parameters").get("given-name")+" "+req.get("result").get("parameters").get("last-name")
        data = getInfo("description",key,"people")
        res = makeWebhookAboutResult(data)

    elif req.get("result").get("action") == "lab_about":
        key = req.get("result").get("parameters").get("lab_names")
        data = getInfo("description",key,"lab")
        res = makeWebhookAboutResult(data)

    # res = json.dumps(res, indent=4)
    # r = make_response(res)
    # r.headers['Content-Type'] = 'application/json'
    # return r
    return res


def getInfo(param,key,type):

    line1 = "Sorry the "+param+" does not exist"
    line2 = ""
    if type == 'lab':
        data = labData
    else:
        data = peopleData
    if param == "description":
        index = next((index for (index, d) in enumerate(data) if key.lower() in d["name"].lower() or d["name"].lower() in key.lower()),-1)
        if index>=0:
            line1 = data[index].get(param)[0] if data[index].get(param) else line1
            count = len(data[index].get(param))
            if count > 1:
                indexes = random.sample(range(1, count), (count+3)/4)
                results = []
                for i in indexes:
                    results.append(data[index].get(param)[i])
                line2= " ".join(results)

    return {"result":line1+line2}



def getGVUInfo(param):
    line1 = aboutData.get(param)['main']
    line2 = ""
    count = len(aboutData.get(param)['description'])
    if count>0:
        index = random.randint(0,count-1)
        line2 = "\n"+aboutData.get(param)['description'][index]
    # rand = random.randint(0, 1)
    # if rand == 1:
    #     line1,line2 =line2,line1
    return {"result":line1+line2}



def makeWebhookAboutResult(data):
    speech = data.get("result")
    return {
            "speech": speech,
            "displayText": speech,
            # "data": data,
            # "contextOut": [],
            "source": "apiai-weather-webhook-sample"
        }


def getLabBasic():
    count = len(labData)
    indexes = random.sample(range(1, count), 3)
    results=[]
    for i in indexes:
        print labData[i]["name"]
        results.append(labData[i]["name"])
    return {"count":str(count),"result":results}



def makeWebhookLabResult(data):
    speech = "We have " + data.get("count") + " labs in GVU. Some of the labs include the " + ", ".join(data.get("result"))
    return {
            "speech": speech,
            "displayText": speech,
            # "data": data,
            # "contextOut": [],
            "source": "apiai-weather-webhook-sample"
        }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    # app.run(debug=False, port=port, host='0.0.0.0')

    app.run(debug=True, port=port, host='0.0.0.0')
