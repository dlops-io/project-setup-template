from setuptools import find_packages, setup

# Packages the prebuilt training image does not have. TensorFlow is already in it: do not list it
# here, or pip may replace the image's build with another version.
REQUIRED_PACKAGES = []

setup(
    name="mlops-app-trainer",
    version="0.1.0",
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    description="Trainer for the MLOps app, run as a Vertex AI training job",
)
