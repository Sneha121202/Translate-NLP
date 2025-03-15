from flask import Flask, render_template, request
from googletrans import Translator

import csv


def load_translationS(csv_file):
    translations = {}

    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        languages = next(reader)  # First row contains language codes

        for row in reader:
            key = row[0]  # English phrase as the key
            translations[key] = {languages[i]: row[i] for i in range(len(row))}

    return translations


def translate_sentence(sentence, lang_from, lang_to, csv_file="translations.csv"):
    translations = load_translations(csv_file)

    # Find the translation if available
    for key, value in translations.items():
        if key.lower() == sentence.lower() and lang_from in value and lang_to in value:
            return value[lang_to]  # Return the translated text

app = Flask(__name__)

# Function to translate sentences
def translate_sentence(sentence, lang_from, lang_to):
    translator = Translator()
    translated = translator.translate(sentence, src=lang_from, dest=lang_to)
    return translated.text

# Route to render the HTML form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle translation requests
@app.route('/translate', methods=['POST'])
def translate():
    sentence = request.form['sentence']
    direction = request.form['direction']

    # Set source and target language based on the checkbox
    if direction == 'english_to_hindi':
        translated_text = translate_sentence(sentence, 'en', 'hi')
    elif direction == 'hindi_to_english':
        translated_text = translate_sentence(sentence, 'hi', 'en')
    else:
        translated_text = "Invalid translation direction!"

    return render_template('index.html', translated_text=translated_text)

if __name__ == "__main__":
    app.run(debug=True)
