from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    audio = request.files.get('audio')
    audio.save('audio.wav')
    return 'OK'


app.run(debug=True)
