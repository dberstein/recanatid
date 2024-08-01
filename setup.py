from setuptools import setup, find_packages

setup(
    name="recanatid",
    version="0.1",
    description="Recanati REST API daemon",
    url="http://github.com/dberstein/recanati-api",
    author="Daniel Berstein",
    author_email="daniel@basegeo.com",
    license="MIT",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "recanatid=recanatid:main",
        ]
    },
)
