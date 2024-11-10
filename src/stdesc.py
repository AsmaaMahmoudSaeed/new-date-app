
# to run application 
# use Python 3.12.3
# instal all reuriments found in requriments.txt

# use cd command to goto project directory then type"streamlit run stdesc.py" in termenal
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import base64
from inference_sdk import InferenceHTTPClient
from ultralytics import YOLO
import os
from docx import Document  # Import the Document class from python-docx

# Function to read docx file content
def read_docx(file_path):
    doc = Document(file_path)
    content = []
    for paragraph in doc.paragraphs:
        content.append(paragraph.text)
    return "\n".join(content)

# Roboflow API credentials
API_URL = "https://detect.roboflow.com"
API_KEY = "XexX78s9cRtMgqjMnYRf"

# Initialize Roboflow client
CLIENT = InferenceHTTPClient(api_url=API_URL, api_key=API_KEY)

# YOLOv5 model initialization
yolo_model = YOLO('best.pt')

# Set background image using base64 encoding
def set_background_image(image_file):
    with open(image_file, "rb") as file:
        encoded_image = base64.b64encode(file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Call the function to set the background image
set_background_image("bg.jpg")

def overlay_text_on_image(image, predictions):
    """Overlay top predictions as text on the top-left of the image."""
    draw = ImageDraw.Draw(image)
    text = "\n".join([f"{pred['class']} {pred['confidence']:.2f}" for pred in predictions])
    font = ImageFont.load_default()  # You can load a custom font if needed
    text_position = (10, 10)
    text_color = (255, 255, 255)  # White text
    draw.text(text_position, text, fill=text_color, font=font)
    return image
# Streamlit app
# Function to display text with a background color
def display_text_with_background(text, height=150):
    st.markdown(f"""
    <div style="background-color: #f0f0f5; padding: 10px; border-radius: 5px;">
        <textarea style="width: 100%; height: {height}px; border: none; background-color: transparent; resize: none; overflow-y: auto;" readonly>{text}</textarea>
    </div>
    """, unsafe_allow_html=True)

# Streamlit app
st.title("Date Disease Detection")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    try:
        # Ensure the uploaded file is opened correctly
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Save the image locally if needed (e.g., for Roboflow)
        img_buffer = BytesIO()
        image.save(img_buffer, format="JPEG")
        img_buffer.seek(0)

        # Roboflow API Prediction
        if st.button("Predict with Roboflow API"):
            img_buffer.seek(0)  # Reset buffer position
            image.save("uploaded_image.jpg")
            
            # Get Roboflow prediction
            result = CLIENT.infer("uploaded_image.jpg", model_id="date-final/1")

            # Extract the top 5 predictions
            predictions = sorted(result["predictions"], key=lambda x: x["confidence"], reverse=True)[:5]

            # Display the top class separately
            top_prediction = predictions[0]
            predicted_class = top_prediction['class']
            confidence = top_prediction['confidence']
            st.write(f"Roboflow API Prediction: {predicted_class} (Confidence: {confidence:.2f})")

            # Overlay predictions on the image
            img_with_text = overlay_text_on_image(image.copy(), predictions)
            st.image(img_with_text, caption="Roboflow API Prediction with Top 5 Classes", use_column_width=True)

            # Read and display content from corresponding docx file
            docx_file_path = os.path.join("details", f"{predicted_class}.docx")
            if os.path.exists(docx_file_path):
                description = read_docx(docx_file_path)
                st.write("Description:")
                display_text_with_background(description)  # Use the new function
            else:
                st.warning("No description available for this class.")

        # YOLO Model Prediction
        if st.button("Predict with YOLO Model"):
            img_resized = image.resize((640, 640))

            # Perform YOLO prediction
            results = yolo_model(img_resized, show=False)

            # Get the top 5 predictions and their confidences
            top5_classes = results[0].probs.top5
            top5_confidences = results[0].probs.top5conf.tolist()

            # Prepare the list of predictions to match the Roboflow format
            predictions = [{"class": results[0].names[cls], "confidence": conf} for cls, conf in zip(top5_classes, top5_confidences)]

            # Display the top class separately
            top1_class = results[0].probs.top1
            top1_confidence = results[0].probs.top1conf.item()
            predicted_class = results[0].names[top1_class]
            st.write(f"YOLO Model Prediction: {predicted_class} (Confidence: {top1_confidence:.2f})")

            # Overlay predictions on the image
            img_with_text = overlay_text_on_image(image.copy(), predictions)
            st.image(img_with_text, caption="YOLO Model Prediction with Top 5 Classes", use_column_width=True)

            # Read and display content from corresponding docx file
            docx_file_path = os.path.join("details", f"{predicted_class}.docx")
            if os.path.exists(docx_file_path):
                description = read_docx(docx_file_path)
                st.write("Description:")
                display_text_with_background(description)  # Use the new function
            else:
                st.warning("No description available for this class.")

    except Exception as e:
        st.error(f"Error: {e}")
