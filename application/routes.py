from flask import request, jsonify,render_template, send_from_directory
from application import app
from application.functions import query2
from application.processing import text2video, name_dir
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
    result={}
    try:
        data = request.get_json()
        print(data["question"])
        if data["question"]=="":
            raise Exception("This is a forced exception")
        text2video(data["question"],name_dir)
        print(data["question"])
        filepath="/static/database/output/converted_output123.mp4"
        result["message"]=200
        result["filepath"]=filepath
    except:
        result["filepath"]=errorpath
        result["message"]=400
    return jsonify(result)


@app.route('/process_audio', methods=['POST'])
def process_audio():
    try:
        result={}
        audio = request.files['audio']

        # Specify the output file path with .mp3 extension
        output_path = 'application/static/audio.mp3'

        # Save the audio in mp3 format
        audio_segment = AudioSegment.from_file(audio)
        audio_segment.export(output_path, format='mp3')

        print(f"Audio saved as {output_path}")
        audio_file = 'application/static/audio.mp3'
        with open(audio_file, 'rb') as file:
            audio_data = file.read()
        
        if audio_data is not None:
        # Convert audio to text
            response = query2(audio_data)
            if response:
                print(response)
               
                try:
                    print("request sent to Hugging Face")
                    text = response["text"]
                    print("response reveived from HuggingFace")
                except:
                    print("Hugging Face returned None")
                    text = None
                print("text:     ",text)
                if (text is not None) and (text!=""):
                    print("text2video conversion started")
                    text2video(text,name_dir)
                    print("text2video conversion finished")
                    filepath="/static/database/output/converted_output123.mp4"
                    result["message"]=200
                    result["filepath"]=filepath
                else:
                    print("Hugging face website returned a None conversion")
                    result["filepath"]=errorpath
                    result["message"]=400
            else:
                print("got no response from hugging face website")
                result["filepath"]=errorpath
                result["message"]=400
        else:
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
