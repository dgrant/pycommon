"""
Setup script
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = '0.3.5'
setuptools.setup(
    name='pycommon',
    packages=['pycommon'],
    version=VERSION,
    description='Useful functions missing from the standard libraries',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='David Grant',
    author_email='davidgrant@gmail.com',
    url='https://github.com/dgrant/pycommon',
    download_url='https://github.com/dgrant/pycommon/tarball/' + VERSION,
    keywords=['utility', 'miscellaneous', 'library'],
    classifiers=[],
)
