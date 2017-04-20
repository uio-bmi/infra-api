import unittest
from infra_api.methods import *
import os
import shutil
from virtualenvapi.manage import VirtualEnvironment
from shutil import copyfile

class testMethods(unittest.TestCase):
	
	def test_clone_github(self):
		print("Test clone github")
		test_clone_url = 'https://github.com/ivargr/pythontest.git'
		expected_clone_into_dir = get_repo_dir("pythontest")		

		if os.path.isdir(expected_clone_into_dir):
			shutil.rmtree(expected_clone_into_dir)

		clone_github_repo(test_clone_url)		

		self.assertTrue(os.path.isdir(expected_clone_into_dir))
		self.assertTrue(os.path.isfile(expected_clone_into_dir + "/README.md"))
		self.assertTrue(os.path.isdir(expected_clone_into_dir + "/.git"))
		print("Finished cloning")

	def test_get_repo_name_from_github_url(self):
		
		self.assertEqual(
			get_repo_name_from_github_url("https://github.com/uio-bmi/bmi_python_sample_project.git"),
			"bmi_python_sample_project"
		)
		
	def test_pull_github_repo(self):
		pull_github_repo("/home/github-repos/pythontest")
		self.assertTrue(True)
		
	def test_install_package_dependencies(self):
		print("test install package dependencies")
		test_repo_name = "__testrepo__"
		repo_dir = get_repo_dir(test_repo_name)
		
		if os.path.exists(repo_dir):
			shutil.rmtree(repo_dir)
		
		os.makedirs(repo_dir)
		self.assertTrue(os.path.isdir(repo_dir))
		
		requirements = ["virtualenv-api==2.1.16"] #, "six"]
		requirements_file = open(repo_dir + "requirements.txt", "w")
		requirements_file.write('\n'.join(requirements))
		requirements_file.close()
		
		install_project_dependencies_into_virtual_env(test_repo_name)
		
		self.assertTrue(os.path.isdir(repo_dir + "virtual_env"))
		
		# Check that requirements are installed
		env = VirtualEnvironment(repo_dir + "virtual_env")
		for req in requirements:
			self.assertTrue(env.is_installed(req))
		
		
	def test_run_project_tests(self):
		test_repo_name = "__testrepo__"
		repo_dir = get_repo_dir(test_repo_name)
		
		if os.path.exists(repo_dir):
			shutil.rmtree(repo_dir)
			
		
		os.makedirs(repo_dir)
		os.makedirs(repo_dir + "/tests")
		install_project_dependencies_into_virtual_env(test_repo_name)	
		# Copy test file
		dest_file_name = repo_dir + "/tests/testSomething.py"
		shutil.copyfile('tests/sample_tests.txt', dest_file_name)
		os.chmod(dest_file_name, 0o665)
		
		run_projects_tests(test_repo_name)
		
		self.assertTrue(os.path.isfile(repo_dir + "/nose_report.html"))


	def test_get_projects_list(self):
		projects = get_projects_list()
		self.assertTrue(isinstance(projects, list))
	

if __name__ == "__main__":
    unittest.main()
