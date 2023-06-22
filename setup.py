from setuptools import setup


def read_description():
    with open("README.md") as file:
        return file.read()


setup(
    name="leekbot_moderation",
    version="0.0.1",
    description="Moderation Tools for Leek",
    long_description=read_description(),
    long_description_content_type="text/markdown",
    author="Lemon",
    author_email="justlemoncl@gmail.com",
    url="https://github.com/LeekByLemon/LeekModeration",
    packages=[
        "leek_moderation"
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Communications",
        "Topic :: Communications :: Chat",
    ],
    install_requires=[
        "leekbot>=0.0.1,<1.0.0"
    ],
    python_requires=">=3.8",
    package_data={
        "": [
            "*.json"
        ]
    },
    include_package_data=True
)
