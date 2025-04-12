# https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
activate:
	# windows
	.venv/Scripts/activate

start:
	python ./overlay.py

process:
	python -O ./detection.py

process-debug:
	python ./detection.py

dev:
	python -m jurigged -v overlay.py