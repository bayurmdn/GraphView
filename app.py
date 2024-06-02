from flask import Flask, render_template, request
import spacy

app = Flask(__name__)
nlp = spacy.load('en_core_web_md')  # Use the larger model

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['text']
    print(f"Received text: {text}")
    doc = nlp(text)
    print(f"Tokens: {[token.text for token in doc]}")
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    print(f"Extracted entities: {entities}")
    return render_template('result.html', entities=entities)

if __name__ == '__main__':
    app.run(debug=True)
