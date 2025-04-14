import requests
import json
import os
from pathlib import Path

def transcribe_audio(url, audio_file_path):
    """
    Send an audio file to the transcription service and get the response.
    
    Args:
        url (str): The URL of the transcription service.
        audio_file_path (str): Path to the audio file to be transcribed.
    
    Returns:
        dict: The JSON response from the transcription service.
    """
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
    
   
    files = {
        'file': (os.path.basename(audio_file_path), open(audio_file_path, 'rb'), 'audio/mp3') // Change mp3 to whatever audio type you are using.
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

if __name__ == "__main__":
   
    transcription_url = "http://34.71.182.226:8082/predict"
    audio_file = "testt.mp3" // Replace with actual audio file name if it in the same directory, if not put the path to the audio file.

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
    else:
        print("Failed to get transcription.")
