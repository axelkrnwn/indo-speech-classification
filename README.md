# Indonesia Words Audio Recognition
Predict indonesia word based on single speech audio. Built using python speech libraries (librosa, noisereduce, and scipy), MFCC (Mel Frequency Cepstral Coefficient), and Random forest model with hyperparameter tuning.

## Dataset Information
The dataset used in this repository is an audio dataset and retrieved from kaggle link below.

[Dataset kaggle link](https://www.kaggle.com/datasets/ahmadulfi/indonesian-words-audio-dataset)

## Explanatory Data Analysis
This dataset contains **seven** classes with approximately **210-213** audio wav file for each class. The classes are single word speech that is pronounced in the audio. The words are BEGAL, KEBAKARAN, KECELAKAAN, MALING, PENCURI, RAMPOK, TABRAKAN. Below is the visualization for audio distribution between each classes.

![image](https://github.com/user-attachments/assets/84d3759d-88c5-4c15-a445-1f18b28c71ed)

Each class contains audio file in wav format. Below are the example audios of the dataset.

![image](https://github.com/user-attachments/assets/5aab74db-f3b0-4359-8712-fdcbe32f79f5)

![image](https://github.com/user-attachments/assets/f07e25e7-56d8-4bee-ac17-e96d0d2e04bf)

The dataset also has two types of ambience noise, rain and road ambience. Moreover, the audio also has silent at the start and end of the audio which makes the audio is not clean to be processed further. so, preprocessing is needed to clean the audio from noise and trim the audio silent part.

## Preprocessing
The preprocessing technique that used in this dataset are noise reduction using noisereduce library and silent trim using librosa. Below are the example result of the audio after being preprocessed.

![image](https://github.com/user-attachments/assets/a2fd3535-8fc0-46fb-805e-75f199b7a45f)

## Feature Extraction (MFCC)

## Data Splitting and PCA

## Modelling and Evaluation
