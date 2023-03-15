from setuptools import setup, find_packages

exec(open("termgpt/version.py").read())

setup(
    name="termgpt",
    packages=find_packages(),
    version=__version__,
    license="MIT",
    description="A chatGPT client on the terminal",
    author="Thomas Capelle",
    author_email="tcapelle@pm.me",
    url="https://github.com/tcapelle/termgpt",
    long_description_content_type="text/markdown",
    keywords=[
        "artificial intelligence",
        "generative models",
        "natural language processing",
        "openai",
    ],
    install_requires=[
        "rich",
        "openai",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={"console_scripts": ["gpt3=termgpt.chat:gpt3",
                                      "gpt4=termgpt.chat:gpt4"]},
)
