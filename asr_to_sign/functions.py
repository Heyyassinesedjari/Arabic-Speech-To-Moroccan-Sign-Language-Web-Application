import json
# Load model directly
from transformers import AutoProcessor, AutoModelForCTC
import torch
import librosa
import arabic_reshaper
from bidi.algorithm import get_display
import os


def query(audio_path='application\static\\audio.mp3'):
    processor = AutoProcessor.from_pretrained("jonatasgrosman/wav2vec2-large-xlsr-53-arabic")
    model = AutoModelForCTC.from_pretrained("jonatasgrosman/wav2vec2-large-xlsr-53-arabic")

    # Load the audio file
    speech, rate = librosa.load(audio_path, sr=16000) # The model expects a sampling rate of 16kHz

    # Process the audio
    input_values = processor(speech, return_tensors="pt", sampling_rate=rate).input_values

    # Get the logits from the model
    with torch.no_grad():
        logits = model(input_values).logits

    # Get the predicted ids
    predicted_ids = torch.argmax(logits, dim=-1)

    # Decode the transcription
    transcription = processor.batch_decode(predicted_ids)[0]

    ## Rendering arabic text

    # Your unconnected Arabic text
    arabic_text = transcription

    # Reshape the text to connect letters properly
    reshaped_text = arabic_reshaper.reshape(arabic_text)

    # Apply RTL direction
    proper_arabic = get_display(reshaped_text)

    return proper_arabic


def getFilePath(directory):
    files = os.listdir(directory)
    if len(files) == 1:
        filename = files[0]
        if directory.endswith("/"):
            return directory+filename
        else:
            return directory+"/"+filename
    else:
        print("The directory does not contain a single file.")