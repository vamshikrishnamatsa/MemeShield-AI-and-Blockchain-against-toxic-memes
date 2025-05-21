import moondream as md
from PIL import Image, ImageDraw
import cv2
import numpy as np
import pytesseract
import os

# Initialize Moondream model (Replace with your API key)
model = md.vl(api_key="")

def process_meme(image_path):
    image = Image.open(image_path)

    # Encode & analyze the meme
    encoded_image = model.encode_image(image)

    # Generate caption
    caption = model.caption(encoded_image)["caption"]

    # Ask the cyberbullying question
    question = "Is this meme cyberbullying? If yes, why? Explain."
    answer = model.query(encoded_image, question)["answer"]

    # Detect objects
    detect_result = model.detect(image, "subject")

    # -----------------------------------------
    # Highlight Detected Objects in Image
    # -----------------------------------------
    
    # Convert PIL image to OpenCV format
    image_cv = np.array(image)
    image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)

    # Draw bounding boxes for detected objects
    for box in detect_result["objects"]:
        x_min, y_min, x_max, y_max = int(box["x_min"] * image.width), int(box["y_min"] * image.height), \
                                     int(box["x_max"] * image.width), int(box["y_max"] * image.height)
        cv2.rectangle(image_cv, (x_min, y_min), (x_max, y_max), (0, 255, 0), 3)  # Green box

    # Convert back to PIL Image for text annotation
    highlighted_image = Image.fromarray(cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB))

    # -----------------------------------------
    # Detect & Highlight Cyberbullying Text
    # -----------------------------------------

    # Extract text using OCR
    extracted_text = pytesseract.image_to_string(image)

    # Ask Moondream for cyberbullying text analysis
    text_analysis = model.query(image, "Does this text contain cyberbullying? If yes, highlight offensive words.")["answer"]

    # Draw bounding boxes around offensive words
    draw = ImageDraw.Draw(highlighted_image)
    ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    offensive_words = [word.strip().lower() for word in text_analysis.split() if len(word) > 3]

    for i in range(len(ocr_data["text"])):
        word = ocr_data["text"][i].strip().lower()
        if word in offensive_words:
            (x, y, w, h) = (ocr_data["left"][i], ocr_data["top"][i], ocr_data["width"][i], ocr_data["height"][i])
            draw.rectangle([(x, y), (x + w, y + h)], outline="red", width=3)

    # Save processed image
    output_path = os.path.join("processed", os.path.basename(image_path))
    os.makedirs("processed", exist_ok=True)
    highlighted_image.save(output_path)

    return output_path, caption, answer, extracted_text, text_analysis
