# lambda-serverless-flask
********************************


Python code to deploy REST Flask app with serverless on AWS lambda. 
The cfn stack includes Lambda, API Gateway, Dynamo DB, IAM roles, S3 bucket to store deployment packages.
   

## Running it

Runtime Python3.6

To start (just init notes, not necessary for run):

Initialize package.json file, install dependencies:

`npm init -f`

`npm install --save-dev serverless-wsgi serverless-python-requirements`

Create serverless.yml

Note: for dockerizing set propertie in serverless.yml as:
 
`dockerizePip: true` or `dockerizePip: non-linux`
 
Start virtual env (this is to run it):
 
`virtualenv venv --python=python3`
 
`source venv/bin/activate`
 
Note: on Windows you might need to point to python.exe: `virtualenv env -p C:/Python36/python.exe` and `env\Scripts\activate`

## Requirements


`pip install -r requirements.txt`


## Deply with serverless: 

`sls deploy`

### Update stack:  `sls deploy`

### Remove stack: `sls remove`


## Tests

Run from root directory `python -m unittest discover tests`

Once `sls deploy` complete, the end point in output.
 
Test from Postman.

Or:

`export BASE_DOMAIN=<endpoint from output>`

Run test for POST e.g. `curl -H "Content-Type: application/json" -X POST ${BASE_DOMAIN}/users -d '{"userId": "user1", "name": "Some Name1"}'`

Run test for GET e.g `curl -H "Content-Type: application/json" -X GET ${BASE_DOMAIN}/users/user1`


## ToDo
This is a draft, work in progress, help welcome
 - build tests
 - add dockerization
 - add to app (login, authorization, screens, widgets)
 
 ## Adding new sites/functionalities


