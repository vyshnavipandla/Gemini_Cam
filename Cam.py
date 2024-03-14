import base64
import requests
import os
import asyncio
import cv2
from py_voice import*
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

async def Eyecatch():
    capture = cv2.VideoCapture(0)
    print("Camera opened")
    if not capture.isOpened():
        print("Error: Unable to access the camera.")
        exit()
    print("Capturing...")
    ret, frame = capture.read()
    if not ret:
        print("Error: Unable to capture a frame.")
        exit()
    capture.release()
    cv2.imshow("Captured Image", frame)
    cv2.imwrite("captured_image.jpg", frame)
    cv2.destroyAllWindows()
    _, encoded_image = cv2.imencode('.png', frame)
    encoded_string = base64.b64encode(encoded_image).decode('utf-8')
    #print(encoded_string)
    cv2.destroyAllWindows()
    base64_image = encoded_string
 
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }
 
    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
    {
        "role": "user",
        "content": [
        {
            "type": "text",
            "text": "Describe the objects captured in this image."
        },
        {
            "type": "image_url",
            "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
            }
        }
        ]
    }
    ],
    "max_tokens": 50
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    #print(f"rsponse is {response}")
    try:
        x = response.json()
        #print(x)
        message_content = x['choices'][0]['message']['content']
        print(message_content)
        speech_audio(message_content)
    except KeyError as e:
        print(f"KeyError: {e}")
        print("Error: Unexpected response format. Check the response structure.")
    
 
#asyncio.run(main())


   

   
