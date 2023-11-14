import naoqi
import subprocess
import os
import json
import select

myBroker = naoqi.ALBroker("myBroker", "0.0.0.0", 0, "10.1.32.201", 9559)
AD = naoqi.ALProxy("ALAudioDevice")
ATTS = naoqi.ALProxy("ALAnimatedSpeech")
openai_api_key = os.environ["API_KEY"]

def record(output_file):
	AD.startMicrophonesRecording(output_file)
	while True:
		instruction = raw_input("When finished talking, enter 'q': ")
		if instruction.lower() == "q":
			break
	AD.stopMicrophonesRecording()


def hear(output_file):
	url = "https://api.openai.com/v1/audio/transcriptions"
	file_path = output_file
	model = "whisper-1"
	language = "en"

	curl_command = [
	    "curl",
	    url,
	    "-H", "Authorization: Bearer {}".format(openai_api_key),
	    "-H", "Content-Type: multipart/form-data",
	    "-F", "file=@{}".format(file_path),
	    "-F", "model={}".format(model),
	    "-F", "language={}".format(language)
	]


	response = subprocess.check_output(curl_command, stderr=subprocess.STDOUT)
	json_response = json.loads(response.splitlines()[-1])
	text_value = json_response.get("text", "")
	print(response)
	return response

def reply(question):
	url = "https://api.openai.com/v1/chat/completions"

	json_payload = {
		"model": "gpt-3.5-turbo",
		"messages": [
			{"role": "system", "content": "You are a helpful cute shopping assistant named Pepper."},
			{"role": "user", "content": question}
		],
		"temperature": 0.3,
		"stream": True
		}
	
	with open("request_payload.json", "w") as json_file:
		json.dump(json_payload, json_file)
	
	curl_command = [
		"curl",
		url,
		"-H", "Content-Type: application/json",
		"-H", "Authorization: Bearer {}".format(os.environ["API_KEY"]),
		"--data-binary", "@request_payload.json"
	]

	process = subprocess.Popen(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)

	dialogue = ""
	word_count = 0

	while process.poll() is None:
		ready_to_read, _, _ = select.select([process.stdout], [], [], 0.1)
		if ready_to_read:
			for line in process.stdout:
				if line.startswith("data: "):
					try:
						json_content = json.loads(line[6:])
						content = json_content.get("choices", [{}])[0].get("delta", {}).get("content", "").encode('ascii', 'ignore')

						if any(char.isalnum() for char in content) or word_count == 10:
							dialogue += content
							word_count += 1
						else:
							print(dialogue)
							speak(dialogue)
							dialogue = ""
							word_count = 0
					except ValueError:
						print("[DONE]")

	# Read any remaining output after the process has finished
	for line in process.stdout:
		if line.startswith("data: "):
			try:
				json_content = json.loads(line[6:])
				content = json_content.get("choices", [{}])[0].get("delta", {}).get("content", "").encode('ascii', 'ignore')

				if any(char.isalnum() for char in content) or word_count == 10:
					dialogue += content
					word_count += 1
				else:
					print(dialogue)
					speak(dialogue)
					dialogue = ""
					word_count = 0
			except ValueError:
				print("[DONE]")

	# Check for errors
	if process.returncode != 0:
		print("Error:", process.stderr.read())

def speak(answer):
	ATTS.say(answer)

def has_text(input_text):
    return any(char.isalnum() for char in input_text)

def main():
	while True:
		instruction = raw_input("When ready to talk, please enter 's', to stop enter 'q': ")

		if instruction.lower() == "q":
			break
		
		if instruction.lower() == "s":
			output_file = "/home/nao/chat_recordings/chat.wav"
			record(output_file)
			question = hear(output_file)
			answer = reply(question)




if __name__ == '__main__':
	main()