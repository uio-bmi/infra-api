from flask import Flask
from flask import request
from flask import jsonify
import json
import logging
from logging.handlers import RotatingFileHandler
from methods import *

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There... asdf........</h1>"

@app.route("/github_push", methods=['POST', 'GET'])
def github_push():

	if request.method == "POST":
		payload = json.loads(request.data)
		repo_meta = {
	        'name': payload['repository']['name'],
	        'owner': payload['repository']['owner']['name'],
	    }

		app.logger.info("Recived post.")

		clone_url = payload['repository']['clone_url']
		app.logger.info("Clone url: %s" % clone_url)
		handle_push_to_github(clone_url)

		return str(request)
		
	elif request.method == "GET":
		f = open('log.txt', "w")
		f.writelines(["Received: " + str(request) + ""])
		f.close()
		return "Recieved get : " + str(request), 200

	return "<h1 style='color:blue'>Test</h1>"


@app.route("/projects", methods=['GET'])
def get_projects():
	return jsonify(get_projects_list())

@app.route("/project_overview", methods=['GET'])
def project_overview():
	project_name = request.args.get('project')
	return jsonify(get_project_overview_as_html(project_name))

	
@app.route("/test_report", methods=['GET'])
def test_report():
	project_name = request.args.get('project')
	return jsonify(get_report_html(project_name))
	
	
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response	

if __name__ == "__main__":
	handler = RotatingFileHandler('api.log', maxBytes=10000, backupCount=1)
	handler.setLevel(logging.INFO)
	app.logger.addHandler(handler)
	app.run(host='0.0.0.0')

   
