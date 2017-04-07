from setuptools import setup

setup(name='infra_api',
      version='0.1',
      description='Infrastructure api',
      license='MIT',
      packages=['infra_api'],
      zip_safe=False,
      install_requires=['pymysql', 'numpy', 'future', 'gitpython']

)

