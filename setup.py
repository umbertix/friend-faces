from setuptools import setup

VERSION = "0.0.1"

requirements = [
    "websocket-client",
    "pusher",
    "pysher",
    "neopixel",
    "gpiozero",
]


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name="FriendFaces",
    version=VERSION,
    description="Project to control LED ring and interconnect 2 of the same using pusher service free tier.",
    long_description=readme(),
    keywords="faces interconnected lamps raspberry",
    author="Umbert Pensato",
    license="MIT",
    url="https://github.com/umbertix/friend-faces",
    install_requires=requirements,
)
