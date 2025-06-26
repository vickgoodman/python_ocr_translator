# ocr.py

import keras_ocr
import cv2

pipeline = keras_ocr.pipeline.Pipeline()

def extract_text(image_path):
    image = keras_ocr.tools.read(image_path)
    prediction = pipeline.recognize([image])[0]
    return prediction  # list of (text, box)
