import requests
import json
import os
from pathlib import Path
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import io

# By default, Flask serves from a 'static' folder for CSS/JS
# and 'templates' for HTML.
# If index.html and style.css are in the root, and script.js too,
# we tell Flask to serve static files from the root directory '.'
# and templates from the root directory '.'
app = Flask(__name__, template_folder='.', static_folder='.')

UPLOAD_FOLDER = 'uploads'
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# This is the new global variable for the transcription URL
TRANSCRIPTION_URL = "http://34.71.182.226:8082/predict"

def transcribe_audio_cli(url, audio_file_path):
    """Sends an audio file to the transcription service (CLI version)."""
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

    # Correctly open the file for binary read and pass it to requests
    with open(audio_file_path, 'rb') as f_audio:
        files = {
            # Use the actual filename for the server part
            'file': (os.path.basename(audio_file_path), f_audio, 'audio/mpeg') # Assuming mpeg, adjust if it's mp3 or other
        }
        try:
            # Make the POST request
            response = requests.post(url, files=files)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during CLI request: {e}")
            return None

def transcribe_audio_web(url, audio_data_stream, filename):
    """Sends audio data (bytes stream) to the transcription service (Web version)."""
    # The 'files' parameter for requests expects a file-like object.
    # audio_data_stream is already a BytesIO object, which is file-like.
    files = {
        'file': (filename, audio_data_stream, 'audio/mpeg') # Ensure correct MIME type
    }
    try:
        response = requests.post(url, files=files)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        error_message = f"Error during web request: {e}"
        status_code = response.status_code if 'response' in locals() and hasattr(response, 'status_code') else 500
        print(error_message) # Log for server records
        return {"error": error_message, "status_code": status_code}


def save_transcription_to_file_cli(result, output_file):
    """Saves transcription result to a file (CLI version)."""
    if not result or "predictions" not in result or not result["predictions"]:
        print("No transcription data to save for CLI.")
        return False

    prediction = result["predictions"][0]
    if "transcription" not in prediction or prediction["transcription"] is None:
        print("CLI: Transcription is null, nothing to save.")
        return False

    transcription_text = prediction["transcription"].get("text", "")

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(transcription_text)
        print(f"CLI: Transcription saved to {output_file}")
        return True
    except Exception as e:
        print(f"CLI: Error saving transcription to file: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def handle_transcribe_web():
    if 'audioFile' not in request.files: # Name attribute from <input type="file" name="audioFile">
        return jsonify({"error": "No file part"}), 400

    file = request.files['audioFile']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)

        audio_data_stream = io.BytesIO(file.read())
        audio_data_stream.seek(0)

        result = transcribe_audio_web(TRANSCRIPTION_URL, audio_data_stream, filename)

        if result and "error" in result and "status_code" in result:
             return jsonify({"error": result["error"]}), result["status_code"]

        if result and "predictions" in result and result["predictions"]:
            # Ensure robust access to deeply nested text
            try:
                transcription_text = result["predictions"][0]["transcription"]["text"]
                return jsonify({"transcription": transcription_text})
            except (IndexError, KeyError, TypeError) as e:
                 # Log the error and the problematic result for debugging
                print(f"Error parsing transcription result: {e}. Result: {result}")
                return jsonify({"error": "Error parsing transcription result."}), 500
        else:
            error_message = "Failed to get transcription or transcription data is not in the expected format."
            if result and "error" in result:
                error_message = result["error"]
            # Log the result if it's not in the expected format or an error occurred
            print(f"Transcription failed or unexpected result format: {result}")
            return jsonify({"error": error_message}), 500

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'cli':
        # CLI execution
        # Use a default audio file if no argument is provided after 'cli'
        audio_file_param = sys.argv[2] if len(sys.argv) > 2 else "testaudio.mp3"
        output_file_param = "transcription.txt" # Default output file name

        # Check if the specified audio file exists
        if not os.path.exists(audio_file_param):
            print(f"Error: Audio file '{audio_file_param}' not found for CLI execution.")
            # Optionally, provide a way to list available .mp3 files or guide the user
            # For example, by listing files in the current directory:
            print("Available files in current directory:", [f for f in os.listdir('.') if os.path.isfile(f)])
        else:
            file_size = os.path.getsize(audio_file_param)
            print(f"CLI: Processing file '{audio_file_param}', size: {file_size} bytes")
            if file_size == 0:
                print("Warning: CLI: File is empty!")

            # Use the CLI-specific transcription function
            cli_result = transcribe_audio_cli(TRANSCRIPTION_URL, audio_file_param)

            if cli_result:
                # Optionally print the full JSON result for debugging or verbose output
                # print(json.dumps(cli_result, indent=2))

                # Save the transcription text to a file
                save_success = save_transcription_to_file_cli(cli_result, output_file_param)
                if not save_success:
                    print("CLI: Failed to save transcription.")
            else:
                print("CLI: Failed to get transcription.")
    else:
        # Web server execution
        # Consider making host and port configurable, e.g., via environment variables
        app.run(debug=True, host='0.0.0.0', port=8080) # Changed port for wider compatibility
