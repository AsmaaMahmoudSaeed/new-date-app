
# Date Disease Detection Application

This application allows users to upload an image of a date fruit palm to predict potential diseases using two different models: the Roboflow API and a YOLO model. The app also displays additional descriptions if a relevant `.docx` file is available for the detected disease.
#### The application is deployed on Streamlet Community Cloud, you can try it from this link.
[Date Disease Detection App](https://new-date-app-iuaicwurcrzzedvjneqqj4.streamlit.app/)
#### Demo

https://www.youtube.com/watch?v=6bVO9EREVy0
#### You can read more about the diseases predicted by this model and the whole project idea through the PDF file.
## Requirements

- **Python**: 3.12.3
- **Required Libraries**: All required libraries are listed in `requirements.txt`. Install them using the following command:

```bash
pip install -r requirements.txt
```
## Dataset
* The data includes 9 different diseases in addition to the healthy samples class.
* [Dataset](https://www.kaggle.com/datasets/computeracademy/dataset-10-classas?select=test)

## Installation and Setup


1. Clone the Repository (or download the project files).
2. Install Dependencies:

```bash
pip install -r requirements.txt
```
3. Navigate to the Project Directory
```code block
cd path/to/project-directory
```
## Running the Application
To start the application, run the following command from the project directory:
```bash
streamlit run stdesc.py
```
This will launch the Streamlit application in your default web browser.

## Application Features
1. Image Upload: Users can upload images in .jpg, .jpeg, or .png format for analysis.
2. Disease Detection:
   * Roboflow API Prediction: Uses the Roboflow API to predict disease with a list of the top 5 predictions.
   * YOLO Model Prediction: Uses a locally initialized YOLO model to detect diseases with the top 5 predictions displayed.
3. Overlay Predictions: Predictions are displayed as an overlay on the uploaded image.
4. Description Display: If available, additional information is loaded from a .docx file that matches the predicted class. This description is shown in a formatted text box.

## Project Structure
* stdesc.py: Main Streamlit application file.
* requirements.txt: List of Python dependencies.
* details/: Directory containing .docx files with disease descriptions (e.g., disease_name.docx).
* bg.jpg: Background image for the application interface.

## Configuration
* Roboflow API: The Roboflow API is initialized with an API URL and an API Key. Replace the API Key (API_KEY) with your own if different from the placeholder provided in the code.
* YOLO Model File: Ensure the YOLO model file best.pt is in the project directory or specify its path in the code.
## Example Usage
1. Start the Streamlit app as described above.
2. Upload an image of a date fruit with suspected disease.
3. Choose either the Roboflow API or YOLO Model for prediction.

4. View results, including disease class, confidence score, and additional description (if available).

5. View results, including disease class, confidence score, and additional description (if available).

