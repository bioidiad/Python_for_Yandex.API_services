import base64, json, io
import requests as req
from requests.exceptions import Timeout


def encode_file(url):
    # url = "https://i.pinimg.com/originals/e3/cf/7d/e3cf7d04683ad6f349c4861b5729a60f.jpg" # paste your url here or pass it as argument
    try:
        file = req.get(url, allow_redirects=True)
    except Timeout:
        print('The request timed out')
    file_content = file.content
    result = base64.b64encode(file_content)
    return(result.decode('utf-8'))

def provide_json(data): # add yur yande folder ID below:
    res = json.dumps({'folderId': 'b1gqeorb....', 'analyze_specs': [{'content': data, 'features': [{'type': 'TEXT_DETECTION', 'text_detection_config': {'language_codes': ['*']}}]}]})
    return(res)

def request_analyze(jayson):
    vision_url = 'https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze'
    api_token= api_token # you api token here (not safe)/enviorment varibale with key (more safe)
    response = req.post(vision_url, headers={'Authorization': f'Bearer {api_token}',
                                         'Content-Type': 'application/json'}, data=jayson)
    # print(response.status_code, response.reason) # prints 200 Ok if fine
    return(response.text)

def parser(jayson):
    text = json.loads(jayson)
    # fd = io.open("output.txt", mode='w', encoding='utf-8')
    buffer = ""

    if not 'results' in text['results'][0]:
        return "Your file is shit!"

    pages = text['results'][0]['results'][0]['textDetection']['pages']
    for page in range(len(pages)):
        for block in range(len(pages[page]['blocks'])):
            current_block = pages[page]['blocks'][block]
            for line in current_block['lines']:
                buffer += '\n' if buffer != "" else ''
                for word in line['words']:
                    buffer += word['text']
                    buffer += " "
    return buffer


def main(event, context):
    data = encode_file(event['url']) # encoding image to bytes
    result = provide_json(data) # prepare .json request
    jayson = request_analyze(result) # send a request and return answer
    ret = parser(jayson) # parsing .json answer to pure text string aligned left (that should be improoved with your requrements)  
    # print(ret)
    return ret

# if __name__=='__main__':
#     url = { "url": ""}
#     context = {}
#     main(url, context)


