# Arabic-Speech-To-Moroccan-Sign-Language-Web-Application

![conda](https://img.shields.io/badge/conda-4.12.0-orange)
![python](https://img.shields.io/badge/Python-3.9.12-green)
![MIT License](https://img.shields.io/badge/MIT_License-blue)

## An operational web application capable of responding to respond to Arabic Speech with Moroccan Sign Language Videos.

This project is a part of my end of 2nd year project at [ENSIAS](https://fr.wikipedia.org/wiki/%C3%89cole_nationale_sup%C3%A9rieure_d%27informatique_et_d%27analyse_des_syst%C3%A8mes), [Mohammed V University](https://en.wikipedia.org/wiki/Mohammed_V_University). When exploring potential project ideas, Professor M. Naoum suggested creating a mobile app to facilitate communication between the Moroccan deaf community and individuals who can hear. After a brief review on platforms like Github and Google Scholar, I noticed a focus on converting sign language videos into written or spoken English using CNNs in existing projects. However, there were limited solutions in the reverse—translating spoken language into sign language, especially addressing Arabic speech and Moroccan Sign Language.

July 21, 2015: Few resources exist for deaf students in Morocco, making assistive devices important for classrooms.
<p align="center">
  <img src="https://github.com/Heyyassinesedjari/Arabic-Speech-To-Moroccan-Sign-Language-Web-Application/assets/94799575/e74f0f28-f607-4800-b218-9d4b54aedfc6" width="50%" height="50%">
</p>

 <br>
Image Source: https://www.nsf.gov/news/mmg/mmg_disp.jsp?med_id=78950&from=

Motivated by this observation, I decided to take on the project myself. My initial step was to create a basic web application containing a small set of words in Moroccan Sign Language, providing a starting point for open-source contributors in Morocco. I plan to expand this into a mobile application, incorporating a more comprehensive range of Moroccan signs that represent everyday spoken vocabulary.

Furthermore, beyond the scope of sign language, I also see potential in training an automatic speech recognition model specifically on the Moroccan dialect. This broader approach aims to accommodate individuals who speak the dialect but not formal Arabic, potentially reaching around 40 million potential users. The goal is to create a holistic solution tailored to meet the communication needs of the Moroccan market.

Every part of this project is sample code which shows how to do the following:

* Create a speech to video translating arabic speech to Moroccan Sign Language (MSL) using Python.
* Implement a Document Retriever using wikipedia api.
* Implement a Document Reader using Transformers including both [distilbert-base-cased-distilled-squad](https://huggingface.co/distilbert-base-cased-distilled-squad) and [AraElectra-Arabic-SQuADv2-QA](https://huggingface.co/ZeyadAhmed/AraElectra-Arabic-SQuADv2-QA) through api calls to the HuggingFace server.
* Create a Messenger like web application using Flask, HTML, CSS and JavaScript.

## Getting Started (Ubuntu/Debian)
* Install Git
  ```bash
  sudo apt update
  sudo apt install git
* Navigate to the Directory
  ```bash
  cd path/to/desired/location
  
* Clone this repository
  ```bash
  git clone https://github.com/Heyyassinesedjari/QuestionAnsweringWebApp.git
* Install Conda
  ```bash
  wget https://repo.anaconda.com/miniconda/Miniconda3-4.12.0-Linux-x86_64.sh
  bash Miniconda3-4.12.0-Linux-x86_64.sh
  source ~/.bashrc

* Creating a Conda Environment
  ```bash
  conda create --name myenv python=3.9.12
* Activate Conda Environment and Install all requirements
  ```bash
  conda activate myenv
  conda install --file path_to_requirements.txt
* Run the App
  ```bash
  python app.py

## High-level functional explanation

### Q&A System Architecture Diagram
<img src="https://github.com/Heyyassinesedjari/QuestionAnsweringWebApp/assets/94799575/ced251a7-9413-4dc0-8f0e-beac07ba3668" width="70%" height="70%">

### Document Retriever Architecture Diagram
<img src="https://github.com/Heyyassinesedjari/QuestionAnsweringWebApp/assets/94799575/602dad7c-bbd6-42a4-837d-a90e797ab187" width="70%" height="70%">

### Document Reader Architecture Diagram
<img src="https://github.com/Heyyassinesedjari/QuestionAnsweringWebApp/assets/94799575/ced251a7-9413-4dc0-8f0e-beac07ba3668" width="70%" height="70%">

### Application Sequence Diagram
<img src="https://github.com/Heyyassinesedjari/QuestionAnsweringWebApp/assets/94799575/83f19996-94c1-4be5-ba6f-ef1ff1329bbd" width="70%" height="70%">

###  Video Demo
https://drive.google.com/file/d/1ZiisKXhRhfLi_eq9hodVj76eoho48SiF/view?usp=sharing

### Project Defense Presentation (Google Slides)
https://docs.google.com/presentation/d/1QeCDO2vUxfz9T6sB_55cypJruRIxJTm-/edit?usp=sharing&ouid=100061785569173216725&rtpof=true&sd=true

