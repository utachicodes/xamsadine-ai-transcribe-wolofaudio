# xamsadine-ai-transcribe-wolofaudio

## Overview
The python script is a automated version of the inference server commnads for the **Xamsadine AI** system, responsible for processing voice-based queries. It receives audio files, performs inference, and returns the processed text output. This code that does the inference through cloud server plays a crucial role in enabling the chatbot to understand and respond to spoken queries.

As part of the setup, 1 test audio file in MP3 format has been provided for testing.

## Features
- **Processes voice-based queries**
- **REST API** for seamless integration.

## Setup & Usage

### Prerequisites
- Python 3.x installed on your system.
- `pip` for installing Python packages.
- A modern web browser.
- Test audio files (e.g., MP3, WAV). One `testaudio.mp3` is provided.

### Installation
1. **Clone the repository or download the files.**
2. **Navigate to the project directory:**
   ```sh
   cd path/to/xamsadine-ai-transcribe-wolofaudio
   ```
3. **Install required Python packages:**
   ```sh
   pip install Flask requests
   ```
   (If you have a `requirements.txt` file, you can use `pip install -r requirements.txt` instead).

### Running the Application

The application can be run in two modes: as a command-line tool or as a web application.

#### 1. Command-Line Interface (CLI)
This mode is useful for quick transcription of a local audio file.
```sh
python transcribe.py cli <audio_file_name>
```
- Replace `<audio_file_name>` with the path to your audio file (e.g., `testaudio.mp3`).
- If no audio file name is provided, it defaults to `testaudio.mp3`.
- The transcription will be printed to the console and saved in `transcription.txt`.

**Example:**
```sh
python transcribe.py cli testaudio.mp3
```

#### 2. Web Application (Browser-based)
This mode allows you to upload audio files through a web interface.
1. **Start the Flask server:**
   ```sh
   python transcribe.py
   ```
2. **Open your web browser** and navigate to:
   ```
   http://127.0.0.1:8080/
   ```
   (Or `http://localhost:8080/`)

3. **Using the Web Interface:**
   - Click "Choose File" to select an audio file from your computer.
   - Click the "Transcribe" button.
   - The transcription will appear on the page.

## License
This project is licensed under the MIT License.

## Contact
For any inquiries:
- **Email:** abdoullahaljersi@gmail.com
- **GitHub:** [utachicodes](https://github.com/utachicodes)
