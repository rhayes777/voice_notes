import glob
import os
from threading import Thread

from flask import Flask, render_template, request
import datetime as dt
import whisper
import openai

from pathlib import Path

output_directory = Path("output")

app = Flask(__name__)

model = whisper.load_model("small")

completion = openai.Completion()

openai.api_key = os.environ["OPENAI_API_KEY"]


header = """
Summarize what is said in the above statements.
"""


def summarize(notes):
    text = "\n".join(notes)
    response = completion.create(
        engine="text-davinci-003",
        max_tokens=1024,
        temperature=0.1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        prompt=text,
    )
    return response["choices"][0]["text"]


def transcribe(filename):
    new_text = model.transcribe(audio=str(filename), language="english")["text"]
    with open(filename.with_suffix(".txt"), "w") as f:
        f.write(new_text)


def get_notes():
    notes = []
    for filename in glob.glob("output/*.txt"):
        with open(filename) as f:
            notes.append(f.read())
    return notes


@app.route('/')
def index():
    notes = get_notes()
    return render_template('index.html', notes=get_notes(), summary=summarize(notes))


@app.route('/upload', methods=['POST'])
def upload():
    audio = request.files.get('audio')
    name = dt.datetime.now().isoformat()
    filename = output_directory / f'{name}.wav'
    audio.save(filename)
    thread = Thread(target=transcribe, args=(filename,))
    thread.start()
    return 'OK'


app.run(debug=True)
