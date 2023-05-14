"""
Spotify Project.

Mazen Mirza <jazenjirza@gmail.com>
"""

from setuptools import setup, find_packages

setup(
    name="spotifyTracker",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "requests",
        "setuptools",
        "mysql.connector",
        "Flask",
        "Flask-RESTful ",
        "Flask-Limiter",
        "flask_sse",
        "Flask-WTF",
    ],
    python_requires=">=3.8",
    entry_points={"console_scripts": ["spotifyTracker = spotifyTracker.__main__:main"]},
)
