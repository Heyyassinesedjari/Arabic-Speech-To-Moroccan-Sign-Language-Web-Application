# Arabic Speech To Moroccan Sign Language Web Application

![conda](https://img.shields.io/badge/conda-4.12.0-orange)
![python](https://img.shields.io/badge/Python-3.9.12-green)
![MIT License](https://img.shields.io/badge/MIT_License-blue)

## An operational web application that interprets spoken Arabic into Moroccan Sign Language videos, enabling seamless communication for the hearing-impaired..

This project is a part of my end of 2nd year project at [ENSIAS](https://fr.wikipedia.org/wiki/%C3%89cole_nationale_sup%C3%A9rieure_d%27informatique_et_d%27analyse_des_syst%C3%A8mes), [Mohammed V University](https://en.wikipedia.org/wiki/Mohammed_V_University). When exploring potential project ideas, Professor [M. Naoum](http://ensias.um5.ac.ma/professor/m-mohamed-naoum) suggested creating a mobile app to facilitate communication between the Moroccan deaf community and individuals who can hear. After a brief review on platforms like Github and Google Scholar, I noticed a focus on converting sign language videos into written or spoken English using CNNs in existing projects. However, there were limited solutions in the reverse—translating spoken language into sign language, especially addressing Arabic speech and Moroccan Sign Language.

<p align="center">
  July 21, 2015: Few resources exist for deaf students in Morocco, making assistive devices important for classrooms.
  
  <img src="https://github.com/Heyyassinesedjari/Arabic-Speech-To-Moroccan-Sign-Language-Web-Application/assets/94799575/e74f0f28-f607-4800-b218-9d4b54aedfc6" width="50%" height="50%">
</p>
<p align="center">
  Image Source: https://www.nsf.gov/news/mmg/mmg_disp.jsp?med_id=78950&from=
</p>

Motivated by this insight, I embarked on the project myself, initiating with a basic web application featuring a limited set of Moroccan Sign Language words. This serves as a starting point for open-source contributors in Morocco, a primary focus of this project.

Looking ahead, I plan to evolve this into a mobile application, expanding the range of Moroccan signs to cover more everyday spoken vocabulary.

Additionally, I aim to develop an automatic speech recognition model specifically for the Moroccan dialect. This broader approach could benefit around 40 million potential users, catering to those who speak the dialect but not formal Arabic. The goal remains to create a comprehensive solution meeting the communication needs of the Moroccan market.

Every part of this project is sample code which shows how to do the following:

* Create a speech to video translating Arabic Speech (AS) to Moroccan Sign Language (MSL) using Python.
* Create a Messenger like web application using Flask, HTML, CSS and JavaScript.

### Main Page :
<p align="center">
<img src="https://github.com/Heyyassinesedjari/Arabic-Speech-To-Moroccan-Sign-Language-Web-Application/assets/94799575/7b95eacc-f712-4809-a8fa-21a9293d31e8" width="70%" height="70%">
</p>

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

### AS to MSL System Architecture Diagram

<p align="center">
<img src="https://github.com/Heyyassinesedjari/Arabic-Speech-To-Moroccan-Sign-Language-Web-Application/assets/94799575/5375f2a9-be81-49a6-967e-fd3d8288296e" width="50%" height="50%">
</p>

### Automatic Speech Recognition with Wave2Vec

<p align="center">
<img src="https://github.com/Heyyassinesedjari/Arabic-Speech-To-Moroccan-Sign-Language-Web-Application/assets/94799575/b21f5868-cb19-46bd-ba86-219df3021258" width="50%" height="50%">
</p>

### Arabic Text Preprocessing

<p align="center">
<img src="https://github.com/Heyyassinesedjari/Arabic-Speech-To-Moroccan-Sign-Language-Web-Application/assets/94799575/082bc1c1-0dfb-45bd-ae81-df00e0b4a369" width="50%" height="50%">
</p>

### Video Retrieval and Concatenation

<p align="center">
<img src="https://github.com/Heyyassinesedjari/Arabic-Speech-To-Moroccan-Sign-Language-Web-Application/assets/94799575/88e152d7-e10b-45b1-8a5f-c0cc3b72107f" width="50%" height="50%">
</p>

### Application Sequence Diagram

<p align="center">
<img src="https://github.com/Heyyassinesedjari/Arabic-Speech-To-Moroccan-Sign-Language-Web-Application/assets/94799575/6f2b1db5-d767-4887-816c-eb9b7d49a805" width="50%" height="50%">
</p>

###  Video Demo
https://drive.google.com/file/d/1ZiisKXhRhfLi_eq9hodVj76eoho48SiF/view?usp=sharing

### Project Defense Presentation (Google Slides)
https://docs.google.com/presentation/d/1QeCDO2vUxfz9T6sB_55cypJruRIxJTm-/edit?usp=sharing&ouid=100061785569173216725&rtpof=true&sd=true

