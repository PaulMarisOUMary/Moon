from setuptools import setup
import re

VERSION = ''
with open("moon/__init__.py") as f:
    tmp = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE)
    if tmp:
        VERSION = tmp.group(1)

if not VERSION:
    raise RuntimeError("version is not set")

PACKAGES = [
    "moon"
]

setup(
    name="moon",
    author="PaulMarisOUMary",
    url="https://github.com/PaulMarisOUMary/MOONSHOT",
    project_urls=
    {
        "Issue tracker": "https://github.com/PaulMarisOUMary/MOONSHOT/issues"
    },
    version=VERSION,
    packages=PACKAGES,
    license="CC BY-NC-SA 4.0",
    description="An interpreter for the Moon Programming Language",
)