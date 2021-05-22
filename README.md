# Datenbanken 3857223
## Get the project running
To get the project running you have to install all the requirements. They are all in the requirements.txt. To install it you have to "cd" in the project folder and run: 
````
pip install -r requirements.txt
````
After that you can run the `app.py` in the `src` folder. This will load a while, because the database is created (1-2 min). When finished, you will get the following output in your console:
````
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 ````
 Then you have to go to `http://127.0.0.1:8050/`.

 
## Tests
The tests are in the `test` folder.
To run the tests the you have to run the `app.py`once. Also the players LeBron James and Michael Jordan need to be downloaded. (To download them, you need to compare them)
To run the tests you need to run:
````
python -m pytest --cov-config=tests/.coveragerc --cov=. tests/
````
You are able to see the coverage then.

When experiencing any problems getting the project working, you can contact me at: timweiss01@gmx.de.
