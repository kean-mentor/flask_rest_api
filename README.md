# flask_rest_api
A simple key-value server using Flask

Install/Deploy:
---------------
Get source: `git clone https://github.com/kean-mentor/flask_rest_api.git`  
_(optional step) Create virtual environment: `virtualenv venv`_  
_(optional step) Activate venv: `source venv\bin\activate`_  
Install requirements: `pip install -r requirements.txt`

Starting:
---------
_(optional step) Activate venv: `source venv\bin\activate`_  

There are 3 different method to start the server
- The simple:  
    - Simply type `python app.py` into the command-line and press ENTER
- Using the Flask development server: 
    - Set environment variables:  
      `export FLASK_APP=app`  
      `export FLASK_DEBUG=1`  
    - Start app:  
      `flask run` (use -p to set port)
- Using a production WSGI server (gunicorn in this case):  
  `gunicorn -b HOST:PORT app:app`  
  
  (_FYI: You can install gunicorn inside a virtualenv and use from there  
  https://docs.gunicorn.org/en/stable/deploy.html#using-virtualenv_)

Running tests:
--------------
- _(optional step) Activate venv: `source venv\bin\activate`_  
- Just type `python tests.py`

Sample requests:
----------------
Get all  
`curl -i http://localhost:5000/values -X GET`

Get by key
`curl -i http://localhost:5000/values/abc123 -X GET`

Add a new key-value pair  
`curl -i -H "Content-Type: application/json" http://localhost:5000/values -X POST -d '{"key": "abc123", "value": "Honda Accord"}'`

Finding keys by value  
`curl -i http://localhost:5000/values?prefix=Honda`
