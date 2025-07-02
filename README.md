python -m venv env

env\Scripts\activate
.\env\Scripts\Activate.ps1

deactivate

pip install -r requirements.txt

python -m spacy download en_core_web_sm