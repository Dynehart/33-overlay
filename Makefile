# https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
activate:
	.venv\Scripts\activate

process:
	python -O ./detection.py

process-debug:
	python ./detection.py