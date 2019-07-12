import pprint
import random
import requests
from decouple import config
from flask import Flask, request


app = Flask(__name__)
token = config('TELEGRAM_TOKEN')
base_url = f'https://api.telegram.org/bot{token}'

naver_client_id = config('NAVER_CLIENT_ID')
naver_client_secret = config('NAVER_CLIENT_SECRET')
naver_url = 'https://openapi.naver.com/v1/papago/n2mt'

 
headers = {'X-Naver-Client-ID': naver_client_id,
    'X-Naver-Client-Secret' : naver_client_secret
}

@app.route(f'/{token}',methods=['POST'])
def telegram():
    response = request.get_json()
    pprint.pprint(response)
    # 사진 파일이 온다면,
    if response.get('message').get('photo'):
        # 사진 파일의 id를 가져온다.
        file_id = response.get('message').get('photo')[-1].get('file_id')
        # 텔레그램 서버에 파일의 경로를 받아온다.
        file_response = requests.get(f'{base_url}/getFile?file_id={file_id}').json()
        # 파일 경로를 통해 URL 만든다.
        file_path = file_response.get('result').get('file_path')
        file_url = f'https://api.telegram.org/file/bot{token}/{file_path}' 
        print(file_url)
        # 2. URL 설정
        naver_url = 'https://openapi.naver.com/v1/vision/celebrity'

       
        response = requests.post(naver_url,
                                headers=headers,
                                files={'image':image}).json()

        best = response.get('faces')[0].get('celebrity')

        if best.get('confidence') > 0.2:
            text = f"{best.get('confidence')*100}%만큼 {best.get('value')}를 닮으셨네요"
        else:
            text = '사람 아닌듯..'
        api_url = f'{base_url}/sendMessage?chat_id={chat_id}&text={text}'
        requests.get(api_url) # 메시지 전송
    # text가 온다면,
    elif response.get('message').get('text'):
       


















if __name__ =='__main__':
    app.run(debug=True)