from flask import Flask, request, jsonify
import os
from PIL import Image
import google.generativeai as genai

# Load the Gemini model (assuming you have the necessary setup)
model = genai.GenerativeModel('gemini-pro-vision')

app = Flask(__name__)

def get_gemini_response(input_text, image_path, prompt):
    """Generates a response using the Gemini model and a given image path.

    Args:
        input_text (str): The user's question or input.
        image_path (str): The path to the floor plan image.
        prompt (str): The prompt to guide the model's generation.

    Returns:
        dict: A JSON dictionary containing the generated response.
    """

    # Load the image from the specified path
    image = Image.open(image_path)

    # Prepare image data for the model
    image_data = [{
        "mime_type": image.format,  # Get the image format
        "data": open(image_path, 'rb').read()
    }]

    # Generate the response using the model
    response = model.generate_content([input_text, image_data, prompt])
    return {"response": response.text}

@app.route('/analyze_floor_plan', methods=['POST'])
def analyze_floor_plan():
    """API endpoint to analyze a floor plan image.

    Expects a JSON request with the following fields:
        - image_path (str): Path to the floor plan image on the server.
        - question (str): The user's question about the floor plan.

    Returns a JSON response with:
        - response (str): The generated response from the model.
        - error (str, optional): Any error message if encountered.
    """

    try:
        data = request.get_json()
        image_path = data['image_path']
        question = data['question']

        # Error handling for missing fields
        if not image_path or not question:
            raise ValueError("Missing required fields in request data.")

        response = get_gemini_response(question, image_path, input_prompt)
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run the API on port 5000
