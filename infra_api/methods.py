import os
from git import Repo
from virtualenvapi.manage import VirtualEnvironment
import subprocess

REPOS_DIR = "/home/github-repos/"

def get_repo_name_from_github_url(url):
	return url.split("/")[-1].split(".git")[0]


def get_repo_dir(project_name):
	return "%s%s/" % (REPOS_DIR, project_name)


def install_project_dependencies_into_virtual_env(project_name):
	# Install dependencies defined in requirements.txt (if exists) into virtualenv
	repo_dir = get_repo_dir(project_name)
	env = VirtualEnvironment('%s/virtual_env' % repo_dir, python='python3')
	
	# Install standard stuff that we want
	env.install("nose")
	env.install("nose-htmloutput")
	
	requirements_file = "%s/requirements.txt" % repo_dir
		
	if os.path.isfile(requirements_file):
		requirements_file = open(requirements_file)
		for line in requirements_file.readlines():
			if not line.startswith("#"):
				try:
					env.install(line)
				except Exception as error:
					print("Error: Could not install package %s. Error: %s" % (line, repr(error)))
					
	else:
		print("Project %s does not have requirements.txt" % project_name)
		
	os.chmod(repo_dir + "/virtual_env/bin/activate", 0o665)


def run_projects_tests(project_name):
	repo_dir = get_repo_dir(project_name)
	tests_dir = repo_dir + "/tests"
	if os.path.isdir(tests_dir):
		print("Running tests")
		command = ["/home/infra-api/infra_api/run_project_tests.sh", project_name]
		process = subprocess.Popen(command)
		process.wait()
	else:
		print("Not running tests. No tests to run")
		 
		 
	
def clone_github_repo(clone_url):
	repo_name = get_repo_name_from_github_url(clone_url)
	repo_dir = get_repo_dir(repo_name)
	
	if os.path.isdir(repo_dir):
		raise Exception("Trying to clone repo that already exists")

	Repo.clone_from(clone_url, repo_dir)
	
	return True


def pull_github_repo(repo_dir):
	repo = Repo(repo_dir)
	assert(len(repo.remotes) == 1)
	
	remote = repo.remotes.origin
	remote.pull()
	

def handle_push_to_github(clone_url):
	"""
	Gets called when a github push is notified
	"""
	
	repo_name = get_repo_name_from_github_url(clone_url)
	repo_dir = "/home/github-repos/%s" % repo_name
	
	if os.path.isdir(repo_dir):
		pull_github_repo(repo_dir)
	else:
		clone_github_repo(clone_url)
	
	install_project_dependencies_into_virtual_env(repo_name)
	
	return True
	

def get_projects_list():
	return os.walk(REPOS_DIR).next()[1]


def get_test_report_html(project_name):
	report_file = get_repo_dir(project_name) + "/nose_report.html"
	if os.path.isfile(report_file):
		f = open(report_file)
		html = f.read()
		
		# Get everything between <body> and </body> and <script> and </script>
		body = html.split("<body>")[1].split("</body>")[0]
		script = html.split("<script>")[1].split("</script>")[0]
		html = body + script
		f.close()
	else:
		html = "No report"
			
	return html
	
	



