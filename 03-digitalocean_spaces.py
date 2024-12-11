import os
import boto3
from botocore.client import Config
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# DigitalOcean Spaces Configuration
SPACES_REGION = os.getenv('SPACES_REGION')
SPACES_NAME = os.getenv('SPACES_NAME')
FOLDER_NAME = os.getenv('FOLDER_NAME')
SPACES_ENDPOINT = f"https://{SPACES_REGION}.digitaloceanspaces.com"

# Your DigitalOcean Spaces credentials
ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

def upload_file_to_spaces(file_path, folder="kursil/webresources"):
    """
    Upload a file to DigitalOcean Spaces in the specified folder
    :param file_path: File to upload
    :param folder: Folder in the Space to upload the file to
    :return: True if file was uploaded, else False
    """
    # Get the file name from the file path
    file_name = os.path.basename(file_path)
    
    # Create the object name with the desired folder structure
    object_name = f"{folder}/{file_name}"

    # Create a session with DigitalOcean Spaces
    session = boto3.session.Session()
    client = session.client('s3',
                            region_name=SPACES_REGION,
                            endpoint_url=SPACES_ENDPOINT,
                            aws_access_key_id=ACCESS_KEY,
                            aws_secret_access_key=SECRET_KEY,
                            config=Config(signature_version='s3v4'))

    try:
        client.upload_file(file_path, SPACES_NAME, object_name)
        file_url = f"https://{SPACES_NAME}.{SPACES_REGION}.digitaloceanspaces.com/{object_name}"
        print(f"File uploaded successfully. URL: {file_url}")
        return file_url
    except Exception as e:
        print(f"Error uploading file: {str(e)}")
        return None

if __name__ == "__main__":
    file_to_upload = "output.mp3"
    uploaded_url = upload_file_to_spaces(file_to_upload)
    if uploaded_url:
        print(f"File is accessible at: {uploaded_url}")