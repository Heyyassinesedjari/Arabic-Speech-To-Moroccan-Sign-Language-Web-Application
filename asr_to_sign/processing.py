import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import re
import os
import cv2
import json
import subprocess
import unicodedata
from file_manager import FileManager



class SignLanguageTranslator:
    def __init__(self, video_base_path="static/database/", video_encoder_path="static/video_encoder.json"):
        self.video_base_path = video_base_path
        self.file_manager = FileManager()
        self.name_dir = self.file_manager.json_load(video_encoder_path)
        self.alphabet = "ا ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه و ي ".split()
        # Define a list of Arabic stop words.
        self.arabic_stopwords = stopwords.words('arabic')
        # Define a list of Arabic punctuation marks.
        self.arabic_punctuation = string.punctuation + '،؛؟'
        self.possessif_suffixes = ["ي","ه","ك","هم","نا","هن","ها","كن","هن","كما"]

    def preprocess_text(self, text, is_name_dir=False):

        # Tokenize the text into words.
        print("start tokenizing the text into words")
        words = word_tokenize(text)
        print("end tokenizing the text into words")
        # Remove stop words and punctuation marks
        filtered_words = [word for word in words if word not in self.arabic_stopwords and word not in self.arabic_punctuation]
        print("filtered_words  ",filtered_words )
        processed_string = re.sub(r'\bال(\w+)\b', r'\1', " ".join(filtered_words))
        print("processed_string  ",processed_string )
        text_list = processed_string.split()
        print("text_list ",text_list)
        
        #remove possessif suffixes
        new_list=[]
        for i in range(len(text_list)):
            for suff in self.possessif_suffixes:
                if len(text_list[i]) == 1:
                    continue
                if text_list[i].endswith(suff):
                    text_list[i] = text_list[i].replace(suff,"")
                    break
            new_list.append(text_list[i])
        n=len(new_list)
        print("test list without suffixes: ",new_list)

        if not is_name_dir:
            ll=[]
            for word in new_list:
                if word not in self.name_dir:
                    for char in word:
                        # NFKC: Normalization Form KC (compatibility composed)
                        normalized_char = unicodedata.normalize('NFKC', char)
                        ll.append(normalized_char)
                else:
                    ll.append(word)
                print("word: ", word)
                print("word list: ", ll)                  
            lll = [string for string in ll if (string in self.alphabet) or (len(string)>1)]                  
            return lll
        else:
            lll = [string for string in new_list if (string in self.alphabet) or (len(string)>1)] 
            return lll
        
    def text_to_video_paths(self, text):
        print("text", text)
        print("started preprocessing text!")
        videos_names = self.preprocess_text(text,self.name_dir)
        print("ended preprocessing text!")
        print("list of word aka video names: ",videos_names)
        #find indicies of videos names in name_dir
        
        hm = {element:index for index, element in enumerate(self.name_dir) if element in videos_names}
        print("hm: ",hm)
        video_indexes = [hm[name] for name in videos_names if name in hm]
        print("video_indexes: ",video_indexes)
        #get video directory paths
        video_paths = [os.path.join(self.video_base_path, str(index)) for index in video_indexes]
        print("video_paths: ",video_paths)
        #get video paths
        video_paths = [self.file_manager.get_file_path(directory=vp) for vp in video_paths]
        print("video_paths before filtering: ",video_paths)
        #filter out None values
        video_paths = [vp for vp in video_paths if vp is not None]
        print("video_paths after filtering: ",video_paths)
        return video_paths
    
    def concat_videos(self, video_paths, output_path="static/database/output/converted_output123.mp4"):
        frames = []
        try:
            # Load and append frames from each video to the frames list
            for path in video_paths:
                video = cv2.VideoCapture(path)
                while True:
                    ret, frame = video.read()
                    #print("frame: ",frame)
                    if not ret:
                        break
                    frames.append(frame)
                video.release()
            if not frames:
                print("No frames to concatenate.")
                return None
            # Calculate the dimensions for each frame
            max_height = max(frame.shape[0] for frame in frames)
            max_width = max(frame.shape[1] for frame in frames)
            # Resize frames to the maximum dimensions
            resized_frames = [cv2.resize(frame, (max_width, max_height)) for frame in frames]
            temp_output = 'static/database/output/output123.mp4'  
            if os.path.exists(temp_output):
                            os.remove(temp_output)
            # Create an output video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(temp_output, fourcc, 25, (max_width, max_height))
            # Write frames to the output video
            print("="*1000)
            print(len(frames))
            print("="*1000)
            for frame in resized_frames:
                out.write(frame)
            # Release the output video writer
            out.release()
            if os.path.exists(output_path):
                os.remove(output_path)
            # Convert the output video to H.264 encoding
            command = f'ffmpeg -i {temp_output} -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k {output_path}'
            subprocess.call(command, shell=True)
            return output_path
        except Exception as e:
            print(f"Error occurred during video concatenation: {str(e)}")
            return None
        
    def text_to_video(self, text):
        video_paths = self.text_to_video_paths(text)
        if not video_paths:
            print("No video paths found for the given text.")
            return None
        return self.concat_videos(video_paths)

