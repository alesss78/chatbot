from flask import Flask,request,make_response
import os,json
import pyowm
import os

# Flask is used to develop a REST Api.
app = Flask(__name__)

#geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
def webhook():

    # get request from DialogFlow
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))
    
    # Handle the request from DialogFlow
    res = processRequest(req)
    print(res)

    # Response to the DialogFlow.
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#processing the request from dialogflow
def processRequest(req):
    print("IntentName :" + req.get("queryResult").get("intent").get("displayName"))
    result = req.get("queryResult")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")

    ### TODO: Simulate BackEnd
    # 1. Read the data from Sorgenia
    # 2. Retrieve information
    # 3. Formaulate a response to DialogFlow
    # END

    speech = "Hi Aless, Today the weather in Rome is sunny."
    data = {}
    test = {}
    test2 = {}
    data['fulfillmentText'] = speech
#   test2['test'] = "test"
#   test['card'] = {test2['test']}
#   data['fulfillmentMessages'] = [test]

    json_data = json.dumps(data)
    return json_data

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
