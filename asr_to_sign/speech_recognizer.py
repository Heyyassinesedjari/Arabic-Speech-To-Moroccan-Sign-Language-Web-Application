from transformers import AutoProcessor, AutoModelForCTC
import torch
import librosa
import arabic_reshaper
from bidi.algorithm import get_display

class SpeechRecognizer:
    """
    Handles Arabic speech recognition using a pretrained wav2vec2 model.
    Loads the model and processor, transcribes audio files, and returns properly rendered Arabic text.
    """

    def __init__(self, model_name="jonatasgrosman/wav2vec2-large-xlsr-53-arabic"):
        """
        Initialize the speech recognizer with the specified model.

        Args:
            model_name (str): HuggingFace model name for wav2vec2 Arabic.
        """
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = AutoModelForCTC.from_pretrained(model_name)

    def transcribe(self, audio_path):
        """
        Transcribe an audio file to Arabic text.

        Loads the audio, processes it, runs inference with the model,
        decodes the output, and reshapes the text for proper Arabic rendering.

        Args:
            audio_path (str): Path to the audio file (.mp3 or .wav).

        Returns:
            str: Transcribed and properly rendered Arabic text.
        """
        # Load the audio file and resample to 16kHz
        speech, rate = librosa.load(audio_path, sr=16000)
        # Process the audio for the model
        input_values = self.processor(speech, return_tensors="pt", sampling_rate=rate).input_values
        # Run inference to get logits
        with torch.no_grad():
            logits = self.model(input_values).logits
        # Get the predicted token IDs
        predicted_ids = torch.argmax(logits, dim=-1)
        # Decode the token IDs to unconnected Arabic text
        transcription = self.processor.batch_decode(predicted_ids)[0]
        # Reshape the text to connect letters properly
        reshaped_text = arabic_reshaper.reshape(transcription)
        # Apply right-to-left direction for proper display
        proper_arabic = get_display(reshaped_text)
        return proper_arabic