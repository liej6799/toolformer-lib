import setuptools
from pathlib import Path

base_path = Path(__file__).parent
long_description = (base_path / "README.md").read_text()

setuptools.setup(
  name="toolformer-lib",
  version="0.0.1",
  author="liej6799",
  description="toolformer",
  long_description=long_description,
  long_description_content_type="text/markdown",
  packages=setuptools.find_packages('toolformer-lib/src'),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Operating System :: OS Independent"
  ],
  python_requires=">=3.6",
  py_modules=["toolformer"],
  package_dir={"": "toolformer-lib/src"},
  install_requires=["openplayground-api", "newsapi-python"],
  url="https://github.com/liej6799/toolformer-lib"
)