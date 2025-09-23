from flask import request, jsonify,render_template, send_from_directory
from asr_to_sign import app
from asr_to_sign.functions import SpeechRecognizer
from asr_to_sign.processing import SignLanguageTranslator
from pydub import AudioSegment
import os

errorpath = "/static/database/error.mp4"

@app.route("/Question_Answering_AR", methods=['GET','POST'])
def home_page_ar():
    return render_template("indexar.html")

@app.route("/", methods=['GET','POST'])
@app.route("/Question_Answering_EN", methods=['GET','POST'])
def home_page_en():
    return render_template("index.html")


@app.route('/process_data', methods=['POST'])
def process_data():
    print("process data called")
    result={}
    try:
        print("try block entered")
        data = request.get_json()
        print(data["question"])
        if data["question"]=="":
            raise Exception("This is a forced exception")
        sign_language_translator = SignLanguageTranslator()
        sign_language_translator.text_to_video(text=data["question"])
        print(data["question"])
        filepath="/static/database/output/converted_output123.mp4"
        result["message"]=200
        result["filepath"]=filepath
    except Exception as e:
        result["filepath"]=errorpath
        result["message"]=400
        print("Exception:", e)
    return jsonify(result)


@app.route('/process_audio', methods=['POST'])
def process_audio():
    try:
        result={}
        audio = request.files['audio']

        # Specify the output file path with .mp3 extension
        output_path = 'static/audio.mp3'

        # Save the audio in mp3 format
        audio_segment = AudioSegment.from_file(audio)
        audio_segment.export(output_path, format='mp3')

        print(f"Audio saved as {output_path}")
        audio_file = output_path
        if os.path.exists(audio_file):
            # Convert audio to text
            print("audio file found!")
            try:
                speech_recognizer = SpeechRecognizer()
                text = speech_recognizer.transcribe(audio_path=audio_file).strip()
                print("audio file converted to text!")
            except:
                text = ""
                print("Error in converting the audio file!")
            if  text!="":
                sign_language_translator = SignLanguageTranslator()
                print("text2video conversion started")
                sign_language_translator.text_to_video(text)
                print("text2video conversion finished")
                filepath="/static/database/output/converted_output123.mp4"
                result["message"]=200
                result["filepath"]=filepath
            else:
                print("Error in converting the audio file!")
                result["filepath"]=errorpath
                result["message"]=400
        else:
            print("Can't find audio file!")
            result["filepath"]=errorpath
            result["message"]=400
    except:
        result["filepath"]=errorpath
        result["message"]=400
    return jsonify(result)


@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static'), filename)
