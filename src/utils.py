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
    return f'{language}-{model_group}-{model}'

def coqui_gather_and_download_model_by_selection(language: LanguageCodes,
                                                 model_group: CoquiModelGroup,
                                                 model: TTSModels) -> str:
    """
    Given a Coqui language, model group, and model, function downloads model.
    """
    response = requests.get(COQUI_GITHUB_URL)

    if response.status_code == 200:

        # Grab all tts models from json
        file_content = response.json()
        file_content = file_content['payload']['blob']['rawLines'][:]
        tts_models = json.loads(' '.join(file_content))['tts_models']

        # Find exact model that is wanted
        language_models = tts_models[language.value]
        model_group_models = language_models[model_group.value]
        specified_model = model_group_models[model.value]
        specified_model_url = specified_model['github_rls_url']
        
        # Generate filename for model to be saved
        model_path = coqui_model_path_generator(language=language.value,
                                                model_group=model_group.value,
                                                model=model.value)

        # Send a GET request to the URL
        response = requests.get(specified_model_url)

        # Create a ZipFile object from the response content
        zip_file = zipfile.ZipFile(io.BytesIO(response.content))

        # Extract all files into the current working directory
        zip_file.extractall(MODEL_DIRECTORY)

        print(model_path)

    else:
        print(f"Failed to fetch the file: {response.status_code}")