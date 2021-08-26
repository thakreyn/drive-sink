from setuptools import setup, find_packages

def readme():
    with open('readme.md') as f:
        return f.read()




setup(
    name = 'sink',
    version = '1.0.1',
    description = "Sink is a CLI synchronisation app for Google Drive",
    long_description = readme(),
    author = 'Yash Thakre',
    license = 'MIT',
    packages = find_packages(),
    entry_points = {
        'console_scripts' : ['sink = src.main:cli']
    },

    install_requires = [
        'click',
        'termcolor',
        'google-api-core==1.31.2',
        'google-api-python-client==2.17.0',
        'google-auth==1.35.0',
        'google-auth-httplib2==0.1.0',
        'google-auth-oauthlib==0.4.5',
        'googleapis-common-protos==1.53.0',
        'oauthlib==3.1.1'
    ],

    include_package_data = True
)

