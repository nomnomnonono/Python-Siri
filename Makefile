format:
	poetry run pysen run format
lint:
	poetry run pysen run lint
setup:
	poetry install
	poetry run pip install git+https://github.com/openai/whisper.git
run:
	poetry run python app.py
