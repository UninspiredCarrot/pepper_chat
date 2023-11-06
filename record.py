import pyaudio
import wave
import time

def rec(output_file, duration):
    current = round(time.time() * 1000)
    # Parameters for audio recording
    FORMAT = pyaudio.paInt16  # Sample format
    CHANNELS = 1              # Number of audio channels (1 for mono, 2 for stereo)
    RATE = 44100              # Sample rate (samples per second)
    RECORD_SECONDS = duration       # Duration of the recording in seconds
    OUTPUT_FILE = output_file  # Output WAV file

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Create an audio stream
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=1024)

    #print("Recording..." + output_file)
    # print("Started Recording " + output_file, 1699270000000 - round(time.time() * 1000))
    frames = []

    # Record audio
    for i in range(0, int(RATE / 1024 * RECORD_SECONDS)):
        data = stream.read(1024)
        frames.append(data)

    #print("Finished recording." + output_file)
    # print("Ended Recording" + output_file, 1699270000000 - round(time.time() * 1000))

    # Stop and close the audio stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio to a WAV file
    with wave.open(OUTPUT_FILE, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    #print(f"Audio saved to {OUTPUT_FILE}")
    