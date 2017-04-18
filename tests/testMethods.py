import unittest
from infra_api.methods import *
import os
import shutil
from virtualenvapi.manage import VirtualEnvironment

class testMethods(unittest.TestCase):
	
	def test_clone_github(self):
		test_clone_url = 'https://github.com/ivargr/pythontest.git'
		expected_clone_into_dir = get_repo_dir("pythontest")		

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
		
	def test_install_package_dependencies(self):
		test_repo_name = "__testrepo__"
		repo_dir = get_repo_dir(test_repo_name)
		
		if os.path.exists(repo_dir):
			shutil.rmtree(repo_dir)
		
		os.makedirs(repo_dir)
   			
   		requirements = 	["virtualenv-api==2.1.16", "six"]
   		requirements_file = open(repo_dir + "requirements.txt", "w")
   		requirements_file.write('\n'.join(requirements))
   		requirements_file.close()
   		
   		install_project_dependencies_into_virtual_env(test_repo_name)
   		
   		self.assertTrue(os.path.isdir(repo_dir + "virtual_env"))
   		
   		# Check that requirements are installed
   		env = VirtualEnvironment(repo_dir + "virtual_env")
   		for req in requirements:
   			self.assertTrue(env.is_installed(req))
   		
 
if __name__ == "__main__":
    unittest.main()
