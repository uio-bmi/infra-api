import os
from git import Repo

def get_repo_name_from_github_url(url):
	return url.split("/")[-1].split(".git")[0]


def clone_github_repo(clone_url):
	repo_name = get_repo_name_from_github_url(clone_url)
	repo_dir = "/home/github-repos/%s" % repo_name	
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
	
	return True
	


