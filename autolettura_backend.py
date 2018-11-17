from flask import Flask,request,make_response
import os,json
import os
import pandas as pd 
import numpy as np

class autolettura_backend:
  def __init__(self, request):
    self.request = request   
    self.result = request.get("queryResult")
    self.intentName = request.get("queryResult").get("intent").get("displayName")

  #processing the request from dialogflow
  def checkaddress(self):
    print("IntentName : " + self.intentName)
    result = self.result
    print(result)
    outputContexts = result.get("outputContexts")
    supplytype = outputContexts[0].get("parameters").get("supply_type")
    clientcode = outputContexts[0].get("parameters").get("client_code")
    clientcode=round(clientcode)
    if supplytype =='luce': 
        speech='Caro utente, per l\'utenza di tipo luce l\'autolettura non é richiesta, vuoi compiere altre operazioni?'
    else:
        auto_data = pd.read_csv('Autolettura_table_clean.csv', sep=';')
        client_filter1=auto_data['client_code']==clientcode 
        client_filter2=auto_data['supplytype']=='GAS'
        adds=auto_data[client_filter1 & client_filter2]['address']
        if len(adds)==0:
            speech='Caro utente, per questo numero cliente non eistono utenze di gas quindi non e\' possibile effettuare l\'autolettura. Vuoi compiere altre operazioni?'
        elif len(adds)>1:
            speech='vedo che con questo account gestisci 2 indirizzi: '+ adds[0] + ' e ' + adds[0] + ', su quale vuoi fare l\'autolettura?'
        else:
            speech='vedo che con questo account sei servito in '+ adds[0] + ' ,L\'autolettura verrà eseguita per questo indirizzo'
                    

    ### TODO: Simulate BackEnd
    # 1. Read the data from Sorgenia
    # 2. Retrieve information
    # 3. Formaulate a response to DialogFlow
    # END
   
    data = {}
    test = {}
    test2 = {}
    data['fulfillmentText'] = speech
    json_data = json.dumps(data)
    return json_data

