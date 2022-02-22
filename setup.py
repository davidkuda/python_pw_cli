from setuptools import setup, find_packages

setup(
    name="python_pw_cli",
    version="0.3.0",
    license="GPL-3.0-or-later",
    description="Manage passwords and other secrets securely in your command line.",
    author="David Kuda",
    author_email="<firstname> @ <lastname> .ai",
    url="https://www.kuda.ai",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    platforms="any",
    python_requires=">=3.7",
)
