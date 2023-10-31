from fuzzywuzzy import fuzz

intents = {
    'привет': ['привет', 'здравствуйте', 'добрый день', 'добрый вечер'],
    'пока': ['пока', 'до свидания', 'до скорого', 'всего доброго']
}

def intent(text):
	for intent, queries in intents.items():
		for q in queries:
			if fuzz.ratio(text, q) >= 50: return intent
	return None

text = 'Привет, Анфиса'
print(intent(text))