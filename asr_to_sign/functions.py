# Load model directly
from transformers import AutoProcessor, AutoModelForCTC
import torch
import librosa
import arabic_reshaper
from bidi.algorithm import get_display




class SpeechRecognizer:
    def __init__(self, model_name="jonatasgrosman/wav2vec2-large-xlsr-53-arabic"):
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = AutoModelForCTC.from_pretrained(model_name)

    def transcribe(self, audio_path):
        # Load the audio file
        speech, rate = librosa.load(audio_path, sr=16000)
        # Process the audio
        input_values = self.processor(speech, return_tensors="pt", sampling_rate=rate).input_values
        # Get the logits from the model
        with torch.no_grad():
            logits = self.model(input_values).logits
        # Get the predicted ids
        predicted_ids = torch.argmax(logits, dim=-1)
        # Decode the transcription (unconnected Arabic text)
        transcription = self.processor.batch_decode(predicted_ids)[0]
        ## Rendering arabic text
        # Reshape the text to connect letters properly
        reshaped_text = arabic_reshaper.reshape(transcription)
        # Apply RTL direction
        proper_arabic = get_display(reshaped_text)
        return proper_arabic