import setuptools

with open("requirements.txt", "r") as req:
    requirements = req.read()

setuptools.setup(
    name="taiga_report",
    version="0.0.1",
    packages=["taiga_report"],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires = requirements,
    zip_safe = False,
    exclude_package_data={'': ['*.md', '*.docx', '*.yaml', '*.yml', '*tests*', '*tests/*', ]}
)