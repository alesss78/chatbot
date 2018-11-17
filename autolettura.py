from flask import Flask,request,make_response
import os,json
import os
import pandas as pd
import datetime
from stringsimilarity import stringsimilarity

class autolettura:
  counter = 0  
  
  def __init__(self, request):
    self.request = request   
    self.result = request.get("queryResult")
    self.intentName = request.get("queryResult").get("intent").get("displayName")
    global address_in
    
    
    
  def contextChatbot(self):
    speech = ''
    
    print("IntentName: " + self.intentName)
    if self.intentName=='autolettura':
        speech = self.checkaddress()
    elif self.intentName=='autolettura_confirm_address':
        autolettura.counter = 0
        speech = self.confirmAddress();
    elif self.intentName=='autolettura_value':
        autolettura.counter = 0
        speech = self.sendnumber();
    elif self.intentName=='getclientcode':
        speech = self.checkaddress();    
    return speech


  def confirmAddress(self):
    global address_in
    speech = ''
    
    
    strsim = stringsimilarity();
    result = self.result
    print(result)
    outputContexts = result.get("outputContexts")
    address_in = outputContexts[0].get("parameters").get("street_address")
    clientcode = outputContexts[0].get("parameters").get("client_code")
    clientcode=int(clientcode)
    print('address_in:' + address_in)
    auto_data = pd.read_csv('Autolettura_table_clean.csv', sep=';')
    client_filter1=auto_data['client_code']==clientcode 
    client_filter2=auto_data['supplytype']=='GAS'
    adds= list(auto_data[client_filter1 & client_filter2]['address'])
    address1 = adds[0]
    address2 = adds[1]
      
    add_1_dist = strsim.levenshtein_distance(address_in, address1)
    add_2_dist = strsim.levenshtein_distance(address_in, address2)
    if (add_1_dist < add_2_dist and add_1_dist < 8):
        address_in=address1
        # TODO: confirm add1
    elif (add_1_dist > add_2_dist and add_2_dist < 8):
        address_in=address2
    add_filter=auto_data['address']==address_in
    supply_filtered=auto_data[add_filter]['supplytype']
    print('distance 1:' + str(add_1_dist))
    print('distance 2:' + str(add_2_dist))
    print('address_in:' + address_in)
    if any(supply_filtered=='GAS'):
        speech='Come vuoi comunicare i dati dell\'autolettura di ' + address_in +'? Vuoi insere i valori o scattare una foto del contatore del gas?'
    else:
        speech='Gentile cliente, per l\'utenza di tipo luce l\'autolettura non é richiesta, vuoi compiere altre operazioni?'
    data = {}
    data['fulfillmentText'] = speech
    json_data = json.dumps(data)
    return json_data


#processing the request from dialogflow
  def checkaddress(self):
    global address_in
    
    
    print(autolettura.counter)
    autolettura.counter = autolettura.counter + 1
    if autolettura.counter > 2:
        speech = 'Caro utente, e\' il terzo tentativo di inserimento di codice cliente non riuscito. Per favore contatta il customer care di Sorgenia' 
        data = {}
        data['fulfillmentText'] = speech
        json_data = json.dumps(data)
        return json_data
    
    print("IntentName : " + self.intentName)
    result = self.result
    print(result)
    outputContexts = result.get("outputContexts")
    clientcode = outputContexts[0].get("parameters").get("client_code")
    clientcode=int(clientcode)
    auto_data = pd.read_csv('Autolettura_table_clean.csv', sep=';')
         
    if not clientcode in list(auto_data['client_code']):
        speech='Ciao, purtroppo il tuo codice cliente non e\' presente nel database. Prova a scegliere una nuova operazione e a digitare nuovamente il tuo codice cliente'
    else:
        client_filter1=auto_data['client_code']==clientcode 
        client_filter2=auto_data['supplytype']=='GAS'
        adds= list(auto_data[client_filter1 & client_filter2]['address'])
#        address1 = adds[0]
#        address2 = adds[1]
#        print('self1' + address1)
#        print('self2' + address2)
        
        if len(adds)==0:
            speech='Caro utente, per questo numero cliente non eistono utenze di tipo gas e quindi non e\' necessario effettuare l\'autolettura. Vuoi compiere altre operazioni?'
        elif len(adds)>1:
            speech='vedo che con questo account gestisci 2 indirizzi: '+ adds[0] + ' e ' + adds[1] + ', su quale vuoi fare l\'autolettura?'
        else:
            speech='vedo che con questo account sei servito in '+ adds[0] + ' , l\'autolettura verrà eseguita per questo indirizzo. Vuoi inserire i numeri o scattare una foto del contatore?'
            address_in=adds[0]
    data = {}
    data['fulfillmentText'] = speech
    json_data = json.dumps(data)
    return json_data


  def sendnumber(self):
    global address_in
    speech = ''
    strsim = stringsimilarity();
    result = self
    print("IntentName : " + self.intentName)
    result = self.result
    print(result)
    outputContexts = result.get("outputContexts")
    gasvalue= str(outputContexts[0].get("parameters").get("number1.original"))
    
    if len(gasvalue)!=5:
        speech='Caro utente, hai inserire un numero di cifre errato: \n devi inserire tutte le cifre che compaiono nelle caselle a sfondo nero del tuo contatore. \n zeri compresi'
    else: 
        speech='i tuoi dati dell\'autolettura sono stati inviati a Sorgenia. Hai bisogno di altro?'
        auto_data = pd.read_csv('Autolettura_table_clean.csv', sep=';')
        gasvalue_filter1=auto_data['address']==address_in 
        gasvalue_filter2=auto_data['supplytype']=='GAS'
        ind=auto_data[gasvalue_filter1 & gasvalue_filter2].index[0]
        now = datetime.datetime.now()
        auto_data.iloc[ind,4]=now.year
        auto_data.iloc[ind,5]=now.month
        auto_data.iloc[ind,6]=now.day
        auto_data.iloc[ind,7]=now.hour
        auto_data.iloc[ind,8]=now.minute
        auto_data.iloc[ind,9]=gasvalue
        auto_data.to_csv('Autolettura_table_clean.csv', sep=';', index=False)
        print('gasvalue'+ gasvalue)
    
    data = {}
    data['fulfillmentText'] = speech
    json_data = json.dumps(data)
    return json_data 

#  def confirmaddress(self):
#    print("IntentName : " + self.intentName)
#    result = self.result
#    print(result)
#    outputContexts = result.get("outputContexts")
#    address = outputContexts[0].get("parameters").get("street_address")
    
#    auto_data = pd.read_csv('Autolettura_table_clean.csv', sep=';')
#    address_filter=auto_data['address']==address 
#    supplies=auto_data[address_filter]['supplytype']
#    if any(supplies=='GAS'):
#        speech='Caro utente, per questo numero cliente non eistono utenze di gas quindi non e\' possibile effettuare l\'autolettura. Vuoi compiere altre operazioni?'
        
  def clientInfoQuery(self, clientCode):
    #TODO: Query information form database
    clientAddress = ''
    clientSupplyType = ''
    return [clientCode, clientAddress, clientSupplyType]

  def makeResponseFormat(self, speech):
    data = {}
    data['fulfillmentText'] = speech
    json_data = json.dumps(data)
    return json_data
