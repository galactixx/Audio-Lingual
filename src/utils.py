import os

import requests
import json
import zipfile
import io

from src.models.models import TTSModels, CoquiModelGroup
from src.models.language_codes import LanguageCodes

with open('config.json') as config_file:
    config = json.load(config_file)

MODEL_DIRECTORY = config['downloaded_models_path']
COQUI_GITHUB_URL = config['coqui_github_models_url']

def coqui_model_path_generator(language: LanguageCodes, model_group: CoquiModelGroup, model: TTSModels) -> str:
    """Generate standardized name for model directory."""
    return f'tts_models--{language.value}--{model_group.value}--{model.value}'

def coqui_gather_and_download_model_by_selection(language: LanguageCodes, model_group: CoquiModelGroup, model: TTSModels) -> str:
    """
    Given a Coqui language, model group, and model, function downloads model.
    """
    existing_models = os.listdir(MODEL_DIRECTORY)
    model_folder_name_expected = coqui_model_path_generator(language=language, model_group=model_group, model=model)
    if model_folder_name_expected in existing_models:
        return os.path.join(MODEL_DIRECTORY, model_folder_name_expected)

    response = requests.get(COQUI_GITHUB_URL)
    if response.status_code == 200:

        # Grab all tts models from json
        file_content = response.json()
        file_content = file_content['payload']['blob']['rawLines'][:]
        tts_models = json.loads(' '.join(file_content))['tts_models']

        # Find exact model that is wanted
        if language.value not in tts_models:
            raise ValueError('specified language does not exist, please check if json format has changed')

        language_models = tts_models[language.value]

        if model_group.value not in language_models:
            raise ValueError('specified model group does not exist, please check if json format has changed')
        
        model_group_models = language_models[model_group.value]

        if model.value not in model_group_models:
            raise ValueError('specified model does not exist, please check if json format has changed')
        
        specified_model = model_group_models[model.value]
        specified_model_url = specified_model['github_rls_url']

        # Send a GET request to the URL
        response = requests.get(specified_model_url)

        # Create a ZipFile object from the response content
        zip_file = zipfile.ZipFile(io.BytesIO(response.content))

        # Extract and rename files
        files_in_zip = zip_file.infolist()

        # Create a set to store the top-level folder names
        top_level_folders = set()

        # Iterate through the ZIP entries and extract the top-level folder names
        for entry in files_in_zip:
            path_parts = entry.filename.split('/')
            if len(path_parts) > 1:
                top_level_folder = path_parts[0]
                top_level_folders.add(top_level_folder)

        if len(top_level_folders) != 1:
            raise Exception('expected only 1 top-level folder in model zip file')
        model_folder_name = list(top_level_folders)[0]
        
        # Extract singular file
        zip_file.extractall(MODEL_DIRECTORY)
        return os.path.join(MODEL_DIRECTORY, model_folder_name)
    else:
        print(f"Failed to fetch the file: {response.status_code}")