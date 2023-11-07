# Import the required module for text  
# to speech conversion 
from gtts import gTTS 
import playsound

# wait for the sound to finish playing?
blocking = True



# This module is imported so that we can  
# play the converted audio 
import os 

def speak(text):  
	# The text that you want to convert to audio 
	mytext = text
	  
	# Language in which you want to convert 
	language = 'en'
	  
	# Passing the text and language to the engine,  
	# here we have marked slow=False. Which tells  
	# the module that the converted audio should  
	# have a high speed 
	myobj = gTTS(text=mytext, lang=language, slow=False) 
	  
	# Saving the converted audio in a mp3 file named 
	# welcome  
	myobj.save("/Users/pratyushsingh/Desktop/VIP4SD/repo/audio/speech.mp3") 
	  
	# Playing the converted file 
	playsound.playsound("/Users/pratyushsingh/Desktop/VIP4SD/repo/audio/speech.mp3", block=blocking)

# import naoqi
# from naoqi import ALProxy
# myBroker = naoqi.ALBroker("myBroker", "0.0.0.0", 0, "10.1.32.201", 9559)

# tts = ALProxy("ALTextToSpeech")

# def speak(text):
# 	tts.say(text)