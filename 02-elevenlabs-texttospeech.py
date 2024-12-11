import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("ELEVENLABS_API_KEY")

# Print the API key for debugging (remove this in production)
# print(f"API Key: {api_key}")

# ElevenLabs API endpoint
url = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

# Replace {voice_id} with an actual voice ID from ElevenLabs
# voice_id = "q8qwd1jY2jS3AWOBeq25"  # Pratama
# voice_id = "lFjzhZHq0NwTRiu2GQxy"  # Tri Nugraha (gaya semangat pitch tinggi)
# voice_id = "MCbAOnEVCtn6noXdBIo0"  # Pramoedya Chandra (gaya resmi orang tua)
# voice_id = "OKanSStS6li6xyU1WdXa"  # Meraki
voice_id = "OKanSStS6li6xyU1WdXa"  # Meraki

# Text to be converted to speech
# text = "Halo, Akhmad Guntar, apa kabar? Kita akan berdiskusi tentang Kurikulum dan Silabus untuk PLN Pusdiklat."
# text = """
# Di tengah kesibukan PLN Pusdiklat Jakarta, para pedagang kaki lima menjajakan aneka kuliner tradisional dengan semangat. Keragaman budaya Indonesia terlihat dari berbagai cita rasa yang menggugah selera.

# """

text = "tes suara"

# Adjust the speaking_rate value to make the speech slower
# 0.5 is half speed, 1.0 is normal speed, 2.0 is double speed
speaking_rate = 0.75  # Adjust this value to make it slower or faster

payload = {
    "text": text,
    "model_id": "eleven_turbo_v2_5",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5,
        "use_speaker_boost": True,
        "speaking_rate": speaking_rate
    }
}

headers = {
    "Content-Type": "application/json",
    "xi-api-key": api_key
}

def get_unique_filename(base_name):
    counter = 0
    name, ext = os.path.splitext(base_name)
    while True:
        if counter == 0:
            file_name = f"{name}{ext}"
        else:
            file_name = f"{name}({counter}){ext}"
        
        if not os.path.exists(file_name):
            return file_name
        counter += 1

try:
    response = requests.post(url.format(voice_id=voice_id), json=payload, headers=headers)
    
    # Print the full response for debugging
    # print(f"Response Status Code: {response.status_code}")
    # print(f"Response Content: {response.text}")
    
    response.raise_for_status()  # Raise an exception for bad status codes

    # Check if the request was successful
    if response.status_code == 200:
        # Get a unique filename
        output_filename = get_unique_filename(f"{voice_id}_output.mp3")

        # Save the audio content to a file
        with open(output_filename, "wb") as audio_file:
            audio_file.write(response.content)
        print(f"Audio file saved as '{output_filename}'")
    else:
        print(f"Error: {response.status_code} - {response.text}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")