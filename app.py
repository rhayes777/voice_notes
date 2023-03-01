import glob

from flask import Flask, render_template, request
import datetime as dt
import whisper

from pathlib import Path

output_directory = Path("output")

app = Flask(__name__)

model = whisper.load_model("base")


def transcribe(filename):
    new_text = model.transcribe(audio=str(filename), language="english")["text"]
    with open(filename.with_suffix(".txt"), "w") as f:
        f.write(new_text)


@app.route('/')
def index():
    notes = []
    for file in sorted(glob.glob(str(output_directory / "*.txt"))):
        with open(file) as f:
            notes.append(f.read())
    return render_template('index.html', notes=notes)


@app.route('/upload', methods=['POST'])
def upload():
    audio = request.files.get('audio')
    name = dt.datetime.now().isoformat()
    filename = output_directory / f'{name}.wav'
    audio.save(filename)
    transcribe(filename)
    return 'OK'


app.run(debug=True)
