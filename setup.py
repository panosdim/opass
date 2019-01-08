import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="opass",
    version="1.0.6",
    author="Panagiotis Dimopoulos",
    author_email="panosdim@gmail.com",
    description="Calculate toll costs in Olympia Odos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/panosdim/opass",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={
        'opass': ['toll.png', 'Tolls.json'],
    },
    entry_points={
        'console_scripts': [
            'opass=opass.opass:main',
        ],
    },
    install_requires=['ttkthemes', 'Pillow', 'numpy'],
)
