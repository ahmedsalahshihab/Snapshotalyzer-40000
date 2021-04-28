from setuptools import setup

# https://setuptools.readthedocs.io/en/latest/userguide/quickstart.html
# https://setuptools.readthedocs.io/en/latest/references/keywords.html
# entry_points --> what I specified means: run the cli function inside the module called shotty (the py function) inside the package called shotty (the folder) 

setup(
	name="snapshotalyzer-40000",
	version="0.1",
	author="Ahmed Shihab",
	author_email="ahmed.salah.shihab@gmail.com",
	description="snapshotalyzer-40000 is a tool to manage AWS EC2 snapshots",
	packages=["shotty"],
	url="https://github.com/ahmedsalahshihab/Snapshotalyzer-40000",
	install_requires=["boto3","click"],
	entry_points='''
		[console_scripts]
		shotty=shotty.shotty:cli
	'''
)