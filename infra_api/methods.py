import os
from git import Repo
from virtualenvapi.manage import VirtualEnvironment

def get_repo_name_from_github_url(url):
	return url.split("/")[-1].split(".git")[0]


def get_repo_dir(project_name):
	return "/home/github-repos/%s/" % project_name


def install_project_dependencies_into_virtual_env(project_name):
	# Install dependencies defined in requirements.txt (if exists) into virtualenv
	repo_dir = get_repo_dir(project_name)
	env = VirtualEnvironment('%s/virtual_env' % repo_dir, python='python3')
	
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
	


