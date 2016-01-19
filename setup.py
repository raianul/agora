from setuptools import setup, find_packages

requirements_to_requires = lambda fn: [req.strip() for req in open(fn, 'rb')]

def get_version():
    try:
        return open('version.txt').read().strip()
    except IOError:
        return ''

setup(name='agora',
      version=get_version() or '0.0-dev',
      packages=find_packages(exclude=('tests', 'tests.*')),
      install_requires=requirements_to_requires('requirements.txt'),
      setup_requires=[
          'wheel==0.24.0',
      ],
      zip_safe=False,
      )
