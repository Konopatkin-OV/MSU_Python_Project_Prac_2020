from setuptools import setup, find_packages

# cruthes forever!
import os
os.system("pipreqs --force")

requirements = list(map(lambda s: s.strip(), open("requirements.txt").readlines()))
print(requirements)

setup(
    name="Sokoban",
    version="0.1",
    packages=find_packages(),

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=requirements,

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "Sokoban": ["*.rst", "*.po", os.path.join("ru", "LC_MESSAGES", "*.mo"), 
                    os.path.join("images", "*.png"), os.path.join("levels", "*.lvl")],
        # And include any *.msg files found in the "hello" package, too:
        # "hello": ["*.msg"],
    },

    # metadata to display on PyPI
    author="Me",
    author_email="me@example.com",
    description="Совместная разработка приложений на Python3, семестровый проект, 2020",
    url="https://github.com/Konopatkin-OV/MSU_Python_Project_Prac_2020/",   # project home page
    # project_urls={
        # "Bug Tracker": "https://bugs.example.com/HelloWorld/",
        # "Documentation": "https://docs.example.com/HelloWorld/",
        # "Source Code": "https://code.example.com/HelloWorld/",
    # },
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License"
    ]

    # could also include long_description, download_url, etc.
)
