import streamlit as st
from PIL import Image
import requests
from PIL import ImageDraw
import io

st.title('Face Detective App')

subscription_key = '15fd3b5ae5f040f79640b80d8655b02d'
assert subscription_key
face_api_url = "https://20210526-kuzumi.cognitiveservices.azure.com/face/v1.0/detect"

uploaded_file = st.file_uploader("Choose an Image...", type='jpg')

if uploaded_file is not None:
    
    img = Image.open(uploaded_file)

    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_img = output.getvalue() #バイナリ取得

    headers = {
        #画像をURLからでなく直接指定する
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key}

    params = {
        'returnFaceId': 'true',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion'
    }

    res = requests.post(face_api_url, params=params, headers=headers, data=binary_img )

    results = res.json()
    for result in results:
        rect = result['faceRectangle']
        
        draw = ImageDraw.Draw(img)
        draw.rectangle([(rect['left'], rect['top']), (rect['left']+rect['width'], rect['top']+rect['height'])], fill=None, outline='green', width=2)
    
    st.image(img, caption='Uploaded Image.', use_column_width=True)
