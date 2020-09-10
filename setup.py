from ensurepip import version
import setuptools

with open("README.md", "r", encoding="utf8") as rm:
    desc = rm.read()

setuptools.setup(
    name="whoami",
    version="2.1.7",
    author="Bohan Wang",
    author_email="wbhan_cn@qq.com",
    description=" ✔ A convenient library to get our ip (real public ip or private ip).",
    long_description=desc,
    long_description_content_type="text/markdown",
    url="https://github.com/wangbohan2000/whoami",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    )
)
