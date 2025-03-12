run:
	py .\src\main.py

reload_mainUi:
	pyside6-uic .\src\views\ui\main.ui > .\src\views\ui\mainUi.py

reload_cameraUi:
	pyside6-uic .\src\views\ui\camera.ui > .\src\views\ui\cameraUi.py 

reload_resources:
	pyside6-rcc .\src\assets\resource.qrc -o .\src\assets\resource_rc.py
	xcopy .\src\assets\resource_rc.py .\src\resource_rc.py /y
	

old_compile_windows:
	pyinstaller --onefile --add-binary="ffmpeg/ffmpeg.exe;ffmpeg" main.py

compile:
	pyinstaller main.spec

old_compile:
	pyinstaller --onefile --windowed --icon=".\src\assets\icon.ico" .\src\main.py

install:
	pip install -r requirements.txt