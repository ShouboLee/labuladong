import setuptools


setuptools.setup(
    name='sentseg',
    version='0.0.1',
    author='lishoubo',
    author_email='lishoubo@intern.langboat.com',
    description='Kensho sentence split tool',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)

print(setuptools.find_packages())
