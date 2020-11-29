import setuptools

with open("README.md", "r") as read_me:
    long_description = read_me.read()

setuptools.setup(
    name="langtools-NuriAmari",
    version="0.0.1",
    author="Nuri Amari",
    author_email="nuri.amari99@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NuriAmari/Language-Tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    packaged_data={"langtools": ["py.typed"]},
    zip_safe=False,
)
