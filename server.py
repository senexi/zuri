# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response
import requests
import json


# Flask app should start in global layout
app = Flask(__name__)


def get_rating():
    url = "https://api.insurhack.com/gi/PolicyPeriod_Set/zde.actions.GetRating"
    headers = {'KeyId': 'b4d1ee3b-3abf-41bb-97c7-80ba3a34fa87', 'Content-Type':'application/json'}

    with open('household_rating.json') as json_data:
	f=json_data.read()

    r=requests.post(url, headers=headers, data=f)
    print(r.text)
    res = json.loads(r.text)
    return res

@app.route('/', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("resolvedQuery") != ":house:":
        return {}
    data  = get_rating() 
    res = makeWebhookResult(data)
    return res


def makeWebhookResult(data):
    amount = data.get("CostsSummary").get("GrossPremium").get("Amount")
    speech = "Your price is " + str(amount)


    print("Response:")
    print(speech)

    j = {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        #"source": "apiai-weather-webhook-sample",
	"followupEvent": {"name":"houseInsuranceRating","data":{"price": str(amount)}},
	
    }
    print(json.dumps(j))
    return json.loads(json.dumps(j))


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    get_rating()
    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
