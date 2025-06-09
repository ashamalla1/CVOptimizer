from flask import Flask, render_template, request
import fitz #PyMuPDF
from docx2txt import process
import re
from nltk.corpus import stopwords
import spacy

app= Flask (__name__)
nlp =spacy.load("en_core_web_sm", disable =["parser","tagger"])

def clean_text(text):
    text = re.sub(r'\s+','',text)#remove extra spaces
    text = text.lower ()#Lowercase
    return ' '.join([word for word in text.split() if word not in stopwords.words('english')])

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/analyze', methods= ['POST'])
def analyze():
    file =request.files['resume']
    if file.filename.endswith('.pdf'):
        text= fitz.open(stream=file.read(),filetype="pdf").get_text()
    elif file.filename .endswith('.docx'):
        text = process(file)
    else:
        return "Unsupported file type",400
    cleaned_text =clean_text(text [:1000])#process first 1000 chars for demo
    doc =nlp (cleaned_text)
    skills=[ent.text for ent in doc.ents if ent.label_ == "SKILL"]
    return render_template('results.html',
                           skills= skills[:5], #show top 5skills
                           snippet =cleaned_text[:200])
if __name__ =='__main__':
    app.run(debug=True)

