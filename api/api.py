from flask import Flask, request, jsonify
from dotenv import load_dotenv
from PIL import Image
import os
import io
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)
key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(prompt, image_data):
    response = model.generate_content([prompt, image_data])
    return response.text

@app.route('/api/process-image', methods=['POST'])
def process_image():
    if 'image' not in request.files or 'prompt' not in request.form:
        return jsonify({'error': 'Image and prompt are required.'}), 400

    uploaded_file = request.files['image']
    prompt = request.form['prompt']

    if uploaded_file.filename == '':
        return jsonify({'error': 'No selected file.'}), 400

    try:
        image = Image.open(uploaded_file.stream)
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes.seek(0)
        image_data = {
            'mime_type': uploaded_file.content_type,
            'data': image_bytes.getvalue()
        }

        response = get_gemini_response(prompt, image_data)
        return jsonify({'response': response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
