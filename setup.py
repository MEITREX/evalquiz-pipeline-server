import pathlib
import pkg_resources

with pathlib.Path("requirements.txt").open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement in pkg_resources.parse_requirements(requirements_txt)
    ]

from distutils.core import setup

setup(
    name="Evalquiz Pipeline Server",
    version="1.0",
    author_email="st170001@stud.uni-stuttgart.de",
    packages=["evalquiz_pipeline_server"],
    install_requires=install_requires,
)
