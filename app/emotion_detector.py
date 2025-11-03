# app/emotion_detector.py
from transformers import pipeline

emotion_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

def detect_emotion(text):
    result = emotion_model(text)[0]
    return result["label"], result["score"]
