# HackCU-2019-Attention-Monitor

## Usage
All Dependencies for Server side are satisfied in the folder called venv.

1. Install virtualenv
	sudo apt install python-virtualenv

2. source the virtual env
	source ./serverside/venv/bin/activate

3. To deactivate (at the end) run
	deactivate

The virtual env covers:
	
	opencv
	django
	pandas
	numpy
	gps

## Run the server

1. Go to ./serverside/hackcu/

2. Start the server

	python3 manage.py runserver

3. paths:

	/				-- home
	/admin/				-- admin page - login included in groupme 
	/users/<username>/		-- User page
	/rendergraph/<username>/	--Bokeh Graph
