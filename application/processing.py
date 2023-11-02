import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import re
import os
import cv2
import json
import subprocess

nltk.download('arabic')  
nltk.download('stopwords')
nltk.download('punkt')


# File path to the JSON file
file_path = "application/static/video_encoder.json"

# Load the JSON file
with open(file_path, 'r') as file:
    name_dir = json.load(file)

name_dir


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

def concat_videos(video_paths):
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
        

        # Calculate the dimensions for each frame
        max_height = max(frame.shape[0] for frame in frames)
        max_width = max(frame.shape[1] for frame in frames)

        # Resize frames to the maximum dimensions
        resized_frames = []
        for frame in frames:
            resized_frame = cv2.resize(frame, (max_width, max_height))
            resized_frames.append(resized_frame)

        file_path = 'application/static/database/output/output123.mp4'  

        try:
            os.remove(file_path)
            print(f"File '{file_path}' has been deleted.")
        except OSError as e:
            print(f"Error occurred while deleting file")


        # Create an output video writer
        output_path = 'application/static/database/output/output123.mp4'
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, 25, (max_width, max_height))

        # Write frames to the output video
        
        print("="*1000)
        print(len(frames))
        print("="*1000)
        for frame in resized_frames:
            out.write(frame)

        # Release the output video writer
        out.release()

        file_path = 'application/static/database/output/converted_output123.mp4'  # Replace with the actual path of the file you want to delete

        try:
            os.remove(file_path)
            print(f"File '{file_path}' has been deleted.")
        except OSError as e:
            print(f"Error occurred while deleting file '{file_path}': {e}")

        # Convert the output video to H.264 encoding
        converted_output_path = 'application/static/database/output/converted_output123.mp4'
        command = f'ffmpeg -i {output_path} -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k {converted_output_path}'
        subprocess.call(command, shell=True)

        return converted_output_path

    except Exception as e:
        print(f"Error occurred during video concatenation: {str(e)}")
        return None

def preprocess_text(text, name_dir, is_name_dir=False):

    alphabet = "ا ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م  ن ه و ن ه و ي".split()

    # Define a list of Arabic stop words.
    arabic_stopwords = stopwords.words('arabic')
    print(arabic_stopwords)

    # Define a list of Arabic punctuation marks.
    arabic_punctuation = string.punctuation + '،؛؟'

    possessif_suffixes = ["ي","ه","ك","هم","نا","هن","ها","كن","هن","كما"]

    # Tokenize the text into words.
    words = word_tokenize(text)
    # Remove stop words and punctuation marks
    filtered_words = [word for word in words if word not in arabic_stopwords and word not in arabic_punctuation]
    print("filtered_words  ",filtered_words )
    processed_string = re.sub(r'\bال(\w+)\b', r'\1', " ".join(filtered_words))
    print("processed_string  ",processed_string )
    text_list = processed_string.split()
    print("text_list ",text_list)
    
    #remove possessif suffixes
    new_list=[]
    for i in range(len(text_list)):
        for suff in possessif_suffixes:
            if len(text_list[i]) == 1:
                continue
            if text_list[i].endswith(suff):
                text_list[i] = text_list[i].replace(suff,"")
                break
        new_list.append(text_list[i])
    n=len(new_list)

    if  not is_name_dir:
        ll=[]
        for word in new_list:
            if word not in name_dir:
                for char in word:
                    ll.append(char)
            else:
                ll.append(word)                    
        lll = [string for string in ll if (string in alphabet) or (len(string)>1)]                  
        return lll
    else:
        lll = [string for string in new_list if (string in alphabet) or (len(string)>1)] 
        return lll

def find_indexes(large_list, small_list):
    return {element:index for index, element in enumerate(large_list) if element in small_list}

def text2video(text,name_dir):
    print("text", text)
    videos_names = preprocess_text(text,name_dir)
    print(videos_names)
    hm = find_indexes(name_dir, videos_names)
    video_indexes = videos_names.copy()
    for i in range(len(videos_names)):
        video_indexes[i] = hm[video_indexes[i]]
    print(video_indexes)
    path = "application/static/database/"
    video_paths  = [path+str(index) for index in video_indexes]
    video_paths = [getFilePath(vp) for vp in video_paths]
    print(video_paths)
    concat_videos(video_paths)