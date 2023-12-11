import os
import json

import requests

with open('config.json') as config_file:
    config = json.load(config_file)

MODEL_DIRECTORY = config['downloaded_models_path']
COQUI_GITHUB_URL = config['coqui_github_models_url']
COQUI_MODEL_JSON_FILENAME = config['coqui_model_json_filename']

def collect_coqui_models_json_file() -> str:
    """
    Automatically download models.json file from Coqui GitHub page.
    """

    if not os.path.exists(MODEL_DIRECTORY):
        os.makedirs(MODEL_DIRECTORY)

    json_model_path = os.path.join(MODEL_DIRECTORY, COQUI_MODEL_JSON_FILENAME)
    if os.path.exists(json_model_path):
        return json_model_path

    response = requests.get(COQUI_GITHUB_URL)
    if response.status_code == 200:

        # Grab all tts models from json
        file_content = response.json()
        file_content = file_content['payload']['blob']['rawLines'][:]
        tts_models = json.loads(' '.join(file_content))

        # Save the data to a JSON file in the specified directory
        with open(json_model_path, 'w') as f:
            json.dump(tts_models, f, indent=4)

        return json_model_path

    else:
        print(f"Failed to fetch the file: {response.status_code}")