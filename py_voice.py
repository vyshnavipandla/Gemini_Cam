import boto3
import pyaudio
import base64
import os
polly = boto3.client('polly', aws_access_key_id="",aws_secret_access_key="",region_name="")
def speech_audio(text):
    response = polly.synthesize_speech(Text=text, OutputFormat='pcm', VoiceId='Brian')
    audio_data = response['AudioStream'].read()
    audio_str=base64.b64encode(audio_data).decode("utf-8")
    audio_str=base64.b64decode(audio_str.encode("ascii"))
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=15000, output=True)
    stream.write(audio_str)
    stream.close()
    pa.terminate()
