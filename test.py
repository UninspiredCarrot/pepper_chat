import os
import record
import re
import threading
import speech_recognition as sr
import requests
import json
from pydub import AudioSegment
import time
import sys
import tts


if sys.version_info[0] < 3:
	#for python2.7:
	from Queue import Queue
else:
	#python python 3+:
	from queue import Queue

api_url = "http://13.42.27.138:8080"
record_path = "/Users/pratyushsingh/Desktop/VIP4SD/repo/audio/"

def combine(audio_file1, audio_file2, output_file):

    audio1 = AudioSegment.from_wav(audio_file1)
    audio2 = AudioSegment.from_wav(audio_file2)

    combined_audio = audio1 + audio2
    combined_audio = combined_audio.set_channels(1)

    combined_audio.export(output_file, format="wav")

def mono(input_file, output_file):
	
	sound = AudioSegment.from_wav(input_file)
	sound = sound.set_channels(1)
	sound.export(output_file, format="wav")

def ask(user_input):

    # Create a dictionary with the question
    data = {
        "question": user_input
    }


    # Encode the data as JSON
    data_json = json.dumps(data)
    headers = {
        'Content-Type': 'application/json'
    }

    # Send a POST request to the API to ask the question
    req = requests.post(api_url+"/ask", data=data_json, headers=headers)

    # Print the answer
    return req.json()["answer"]

def scribe(path):
    files = {
        'audio_file': (path, open(path, 'rb'), 'audio/wav')
        }

    response = requests.post(api_url+"/listen", files=files)
    return response.json()["transcript"]

def check(file, hyperaware=False, curious=False):
	r = sr.Recognizer()
	r.energy_threshold = 1500
	r.language = 'en-US'
	# print("Check started at:", time.ctime(time.time()))
	# Initialize the recognizer
	with sr.WavFile(file) as source:
		#use "test.wav" as the audio source
		audio = r.record(source)
	try:
		words = r.recognize(audio)

		print("I heard: ")
		print(words)
		
		if hyperaware:
			whisper_words = set(re.split(r"[, .]+", scribe(file)["text"]))
			##print(whisper_words)
			for word in whisper_words:
				if re.findall(r"(pep|per)", word, re.IGNORECASE):
					print("awake Check ended at:", time.ctime(time.time()))
					return "awake"
			print("not awake Check ended at:", time.ctime(time.time()))
			return "heard asleep"
		else:
			words = set(re.split(r"[, .]+", words))
			##print(words)
			if curious:
				whisper_words = set(re.split(r"[, .]+", scribe(file)["text"]))
				##print(whisper_words)

			for word in words:
				if re.findall(r"(pep|per)", word, re.IGNORECASE):
					print("Awake at: ", time.ctime(time.time()))
					return "awake"
			print("Heard at: ", time.ctime(time.time()))
			return "heard"


	except LookupError:
		print("Silent at:", time.ctime(time.time()))
		return "silence"

def checker(file, q, word, output_file=None):

	value = check(file) == word
	q.put(value)

	if word=="silence":

		if value:
			os.rename(output_file, output_file)

		else:
			combine(output_file, record_path + '3.wav', output_file)

def threader(target1, args1, target2, args2):

	thread1 = threading.Thread(target=target1, args=args1)
	thread2 = threading.Thread(target=target2, args=args2)

	thread1.start()
	thread2.start()

	thread1.join()
	thread2.join()

	mono(record_path + '3.wav', record_path + '3.wav')

def record_heys(output_file):

	record.rec(record_path + "1.wav", 4)
	record.rec(record_path + "2.wav", 4)
	combine(record_path + '1.wav',record_path + '2.wav', output_file)

	awake_queue = Queue()
	silence_queue = Queue()

	while True:

		threader(checker, (output_file, awake_queue,"awake"), record.rec, (record_path + '3.wav',4,))

		if awake_queue.get():

			while True:

				threader(checker, (record_path + '3.wav',silence_queue,"silence",output_file), record.rec, (record_path + '3.wav',5,))

				if silence_queue.get():

					break

			break

		else:

			os.remove(record_path + "1.wav")
			os.rename(record_path + "2.wav", record_path + "1.wav")
			os.rename(record_path + "3.wav", record_path + "2.wav")
			combine(record_path + '1.wav',record_path + '2.wav', output_file)

def cleanup(path):

	files = ["1.wav", "2.wav", "3.wav", "cf.wav", "speech.mp3"]

	for file in files:
		if os.path.exists(record_path + file):
			os.remove(record_path + file)

	if os.path.exists(path):
		os.remove(path)

	if os.path.exists(record_path[:41] + "ec2/wav_files/audio.wav"):
		os.remove(path)
	
	# # Stop and close the audio stream
	# record.stream.stop_stream()
	# record.stream.close()
	# record.audio.terminate()
	
	print("cleanup done")

if __name__ == "__main__":
	try:
		while True:

			path = record_path + "full.wav"

			record_heys(path)

			try:
				question = re.split(r"[, .]+", scribe(path)["text"])
				position = 0
				for i in range(len(question)):
					if re.findall(r"(pep|per)", question[i], re.IGNORECASE):
						position = i+1
						break

				question = "User: "+ " ".join(question[position:])
				print(question)
				answer = ask(question)
				print(answer)
				tts.speak(answer)

			except requests.exceptions.ConnectionError:
				r = sr.Recognizer()
				r.energy_threshold = 1500
				r.language = 'en-US'
				print("Could not connect to API")
				with sr.WavFile(path) as source:
					audio = r.record(source)
				words = r.recognize(audio)
				print("Google thinks you said: " + words)

			cleanup(path)

	except KeyboardInterrupt:
		cleanup(path)

