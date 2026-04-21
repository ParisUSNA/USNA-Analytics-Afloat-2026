SHELL := /bin/bash
.DEFAULT_GOAL := build

build: run_app.py app.py
	@source ~/Capstone/venv/bin/activate && pyinstaller --noconsole --onefile --windowed --additional-hooks-dir=./hooks --collect-all streamlit --collect-all flaskwebgui --add-data="app.py:." --add-data="icon.png:." run_app.py &> /dev/null && deactivate && echo "Build Complete"

loud: run_app.py app.py
	source ~/Capstone/venv/bin/activate && pyinstaller --noconsole --onefile --windowed --additional-hooks-dir=./hooks --collect-all streamlit --collect-all flaskwebgui --add-data="app.py:." --add-data="icon.png:." run_app.py && deactivate && echo "Build Complete"
	