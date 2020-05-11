import json
import requests as req

def translate(string, lang):
	#create .json request with your variables first:
    jayson = json.dumps({
    "folder_id": "b1gqeorbaiqp3.......", # your Yandex folder here
    "texts": [string],
    "targetLanguageCode": lang
    })
    translate_url = 'https://translate.api.cloud.yandex.net/translate/v2/translate'
    api_token = api_token # your token env variable
    response = req.post(translate_url, headers={'Authorization': f'Bearer {api_token}',
                                         'Content-Type': 'application/json'}, data=jayson)
    # print(response.status_code, response.reason) #test with this string firstly, the "200 OK" response means everything is fine  
    key = json.loads(response.text)["translations"][0]['text'] # this parse the .json answer into pure text
    return(key.encode('utf-8'))

def main(event, context):
    ret = translate(event["string"], event["lang"])
    return(ret)

