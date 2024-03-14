import RPi.GPIO as GPIO
import time
from cam import Eyecatch
import asyncio
import threading
import wave
import pyaudio
# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)
 
# Set the GPIO pin for reading
input_pin = 17 
output_pin = 27 

# Set the GPIO pin as an input
GPIO.setup(input_pin, GPIO.IN)
GPIO.setup(output_pin, GPIO.OUT)
def play_audio():
    wf = wave.open("/home/Vyshnavi/Desktop/new1/response.wav", 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)

    stream.stop_stream()
    stream.close()
    p.terminate()

try:
	GPIO.output(output_pin, GPIO.LOW)
	while True:
          # Read the state of the GPIO pin
          pin_state1 = GPIO.input(input_pin)
          if pin_state1:
               print("am activated...")
               audio_thread = threading.Thread(target=play_audio)
               audio_thread.start()
               GPIO.output(output_pin, GPIO.HIGH)
               asyncio.run(Eyecatch())
               print("DONE>>>")
               GPIO.output(output_pin, GPIO.LOW)
               time.sleep(1)
except KeyboardInterrupt:
    # Clean up GPIO on exit
    GPIO.cleanup()
    
finally:
	GPIO.cleanup()
