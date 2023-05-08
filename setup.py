import setuptools

with open('README.md', encoding='utf-8') as f:
    long_desc = f.read()

requirements = ["rich"]

setuptools.setup(
    version="1.0.1",
    name="akane",
    author="zekro",
    author_email="contact@zekro.de",
    description="Simple, stronly typed library to create tests for anything",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/zekrotja/akane",
    download_url='https://github.com/zekrotja/akane/archive/main.tar.gz',
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Topic :: Software Development :: Libraries',
    ],
)
