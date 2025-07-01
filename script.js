document.addEventListener('DOMContentLoaded', () => {
    const audioFileInput = document.getElementById('audioFile');
    const transcribeButton = document.getElementById('transcribeButton');
    const transcriptionOutputDiv = document.getElementById('transcriptionOutput');

    transcribeButton.addEventListener('click', async () => {
        const file = audioFileInput.files[0];

        if (!file) {
            transcriptionOutputDiv.textContent = 'Please select an audio file first.';
            return;
        }

        transcriptionOutputDiv.textContent = 'Transcribing...';

        const formData = new FormData();
        formData.append('audioFile', file); // Ensure 'audioFile' matches the name expected by Flask

        try {
            const response = await fetch('/transcribe', { // Endpoint defined in Flask
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                // Try to get error message from server response
                const errorData = await response.json().catch(() => null); // Gracefully handle non-JSON error responses
                let errorMessage = `Error: ${response.status} ${response.statusText}`;
                if (errorData && errorData.error) {
                    errorMessage = `Error: ${errorData.error}`;
                }
                throw new Error(errorMessage);
            }

            const result = await response.json();

            if (result.transcription) {
                transcriptionOutputDiv.textContent = result.transcription;
            } else if (result.error) {
                transcriptionOutputDiv.textContent = `Server error: ${result.error}`;
            } else {
                // Fallback for unexpected response structure
                transcriptionOutputDiv.textContent = 'Failed to get transcription. Unexpected response format.';
            }

        } catch (error) {
            console.error('Transcription request failed:', error);
            transcriptionOutputDiv.textContent = `Request failed: ${error.message}`;
        }
    });
});
