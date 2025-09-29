from flask import request, jsonify,render_template, send_from_directory
from asr_to_sign import app
from asr_to_sign.functions import SpeechRecognizer
from asr_to_sign.sign_language_translator import SignLanguageTranslator
import os
from .file_manager import FileManager



import arabic_reshaper
from bidi.algorithm import get_display

file_manager = FileManager()
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
        print("original typed text: ",data["question"])
        if data["question"]=="":
            raise Exception("This is a forced exception")
        

        ## Rendering arabic text
        # Reshape the text to connect letters properly
        reshaped_text = arabic_reshaper.reshape(data["question"])
        # Apply RTL direction
        proper_arabic = get_display(reshaped_text)
        print("proper_arabic", proper_arabic)

        sign_language_translator = SignLanguageTranslator()
        sign_language_translator.text_to_video(text=proper_arabic)
        filepath="/static/database/concatenated_MSL_video.mp4"
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
        audio_file_path='static/audio.mp3'
        global file_manager
        file_manager.save_audio_file_sent_by_browser(output_path=audio_file_path)
        if file_manager.file_exists(audio_file_path):
            # Convert audio to text
            print("audio file found!")
            try:
                speech_recognizer = SpeechRecognizer()
                text = speech_recognizer.transcribe(audio_path=audio_file_path).strip()
                print("audio file converted to text!")
            except:
                text = ""
                print("Error in converting the audio file!")
            if  text!="":
                sign_language_translator = SignLanguageTranslator()
                print("text2video conversion started")
                sign_language_translator.text_to_video(text)
                print("text2video conversion finished")
                filepath="/static/database/concatenated_MSL_video.mp4"
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
