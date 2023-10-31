import json, pyaudio, pyttsx3
from vosk import Model, KaldiRecognizer
from pygame import mixer
from fuzzywuzzy import fuzz


lang = 'Please Specify A Language (ru/en)'
lang = 'en'



# -- Text-To-Speech --
# engine = pyttsx3.init()
# engine.setProperty('rate', 220)

model = Model(f'models/{lang}')
recognizer = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, 
				channels=1, 
				rate=16000, 
				input=True, 
				frames_per_buffer=8192)
stream.start_stream()

mixer.init()
mixer.music.load('sound.mp3')
mixer.music.play()

def listenAudio():
	while True:
		data = stream.read(4096)
		if recognizer.AcceptWaveform(data):
			answer = json.loads(recognizer.Result())
			yield answer['text']

enIntents = {
	'hi': ['hi', 'hello', 'good afternoon', 'good evening'],
    'bye': ['bye', 'goodbye', 'see you soon', 'all the best']
}

ruIntents = {
    'привет': ['привет', 'здравствуйте', 'добрый день', 'добрый вечер'],
    'пока': ['пока', 'до свидания', 'до скорого', 'всего доброго']
}

def detectIntent(intents, text):
	for intent, queries in intents.items():
		for q in queries:
			chance = fuzz.ratio(text, q)
			if chance >= 50: return intent
	return None

for text in listenAudio():
	if lang == 'en':
		if 'jarvis' in text:
			intent = detectIntent(enIntents, text.replace('jarvis ', ''))
			if intent == 'hi':
				print('Hi!')
			elif intent == 'bye':
				print('Bye-Bye..')
			else:
				print('None Request')

	elif lang == 'ru':
		if 'джарвис' in text:
			intent = detectIntent(ruIntents, text.replace('джарвис ', ''))
			if intent == 'привет':
				print('Привет-привет!')
			elif intent == 'пока':
				print('Пока..')
			else:
				print('Неизвестный запрос')

	else:
		print('Please Specify A Correct Language!')