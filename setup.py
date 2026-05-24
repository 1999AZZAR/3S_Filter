from setuptools import setup, find_packages

setup(
    name="three_s_filter",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "transformers",
        "sentence-transformers",
        "scikit-learn",
        "numpy",
        "onnxruntime",
        "pyyaml",
        "flask"
    ],
    author="Gemini CLI",
    description="Triple-layer safety monitor for autonomous AI agents",
    license="MIT",
)
