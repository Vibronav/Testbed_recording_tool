from pathlib import Path

from setuptools import find_packages, setup


try:
    with open('requirements.txt', encoding='utf-16') as fp:
        install_requires = fp.read()
except:
    with open('requirements.txt') as fp:
        install_requires = fp.read()

setup(
    name="testbed-recording-tool",
    version="0.1.0",
    description="Command-line tools for testbed recordings.",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    packages=find_packages(),
    install_requires=install_requires,
    python_requires=">=3.9",
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={
        "console_scripts": [
            "testbed-recording-tool=testbed_recording_tool.main:main",
        ],
    },
)
