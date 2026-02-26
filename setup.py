from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="ca_firm_management",
    version="1.0.0",
    description="CA Firm Management System - Phase 1: Practice Management",
    author="Your Firm",
    author_email="admin@yourfirm.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
