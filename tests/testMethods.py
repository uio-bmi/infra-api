import unittest
from infra_api.methods import *
import os
import shutil

class testMethods(unittest.TestCase):
	
	def test_clone_github(self):
		test_clone_url = 'https://github.com/ivargr/pythontest.git'
		expected_clone_into_dir = "/home/github-repos/pythontest"		

		if os.path.isdir(expected_clone_into_dir):
			shutil.rmtree(expected_clone_into_dir)

		clone_github_repo(test_clone_url)		

		self.assertTrue(os.path.isdir(expected_clone_into_dir))
		self.assertTrue(os.path.isfile(expected_clone_into_dir + "/README.md"))
		self.assertTrue(os.path.isdir(expected_clone_into_dir + "/.git"))

	def test_get_repo_name_from_github_url(self):
		
		self.assertEquals(
			get_repo_name_from_github_url("https://github.com/uio-bmi/bmi_python_sample_project.git"),
			"bmi_python_sample_project"
		)
		
	def test_pull_github_repo(self):
		pull_github_repo("/home/github-repos/pythontest")
		self.assertTrue(True)
