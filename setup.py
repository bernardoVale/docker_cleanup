from setuptools import setup

install_requires = [
    'docker >= 2.0.0'
]

setup(name='docker_cleanup',
      version='0.1',
      description='Provides housekeeping for Docker host',
      author='Bernardo Vale',
      author_email='bvale@avenuecode.com',
      packages=['docker_cleanup', 'docker_cleanup.main'],
      scripts=[
          'bin/docker_cleanup'
      ],
      install_requires=install_requires,
      )
