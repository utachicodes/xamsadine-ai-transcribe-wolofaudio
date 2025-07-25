import requests
import json
import os
from pathlib import Path

def transcribe_audio(url, audio_file_path):
    
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
    
   
    files = {
        'file': (os.path.basename(audio_file_path), open(audio_file_path, 'rb'), 'audio/mp3')
    }
    
 
    try:
        print(f"Sending request to {url} with file {audio_file_path}...")
        response = requests.post(url, files=files)
        print(f"Response status code: {response.status_code}")
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return None
    finally:
        
        files['file'][1].close()

def save_transcription_to_file(result, output_file):
    """
    Save the transcription text to a file.
    
    Args:
        result (dict): The JSON response from the transcription service.
        output_file (str): Path to the output text file.
    """
    if not result or "predictions" not in result or not result["predictions"]:
        print("No transcription data to save.")
        return False
    
    prediction = result["predictions"][0]
    if "transcription" not in prediction or prediction["transcription"] is None:
        print("Transcription is null, nothing to save.")
        return False
        
    transcription_text = prediction["transcription"].get("text", "")
  
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(transcription_text)
        print(f"Transcription saved to {output_file}")
        return True
    except Exception as e:
        print(f"Error saving transcription to file: {e}")
        return False

if __name__ == "__main__":
   
    transcription_url = "http://34.71.182.226:8082/predict"
    audio_file = "testt.mp3"
    output_file = "transcription.txt"
    

    print(f"Current working directory: {os.getcwd()}")
    print(f"Looking for audio file: {Path(audio_file).absolute()}")
    
    if os.path.exists(audio_file):
        file_size = os.path.getsize(audio_file)
        print(f"File size: {file_size} bytes")
        if file_size == 0:
            print("Warning: File is empty!")
    
    result = transcribe_audio(transcription_url, audio_file)
    
    if result:
        print(json.dumps(result, indent=2))

        save_transcription_to_file(result, output_file)
    else:
        print("Failed to get transcription.")
>>>>>>> parent of 7ac6c80 (Update transcribe.py)
