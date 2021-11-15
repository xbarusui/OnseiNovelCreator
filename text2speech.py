import hmac
import requests
import hashlib
import json
from datetime import datetime, timezone

import streamlit as st

def text2speech(speaker,text):

  date: str = str(int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()))
  data: str = json.dumps({
    'coefont': speaker,
    'text': text
  })
  signature = hmac.new(bytes(st.secrets["onsei"]["access_secret"], 'utf-8'), (date+data).encode('utf-8'), hashlib.sha256).hexdigest()

  response = requests.post('https://api.coefont.cloud/v1/text2speech', data=data, headers={
    'Content-Type': 'application/json',
    'Authorization': st.secrets["onsei"]["accesskey"],
    'X-Coefont-Date': date,
    'X-Coefont-Content': signature
  })

  if response.status_code == 200:
#    with open('response.wav', 'wb') as f:
#      f.write(response.content)
    return response.content
  else:
    st.error(response.json())