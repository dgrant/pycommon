"""
Setup script
"""
from distutils.core import setup

VERSION = '0.3.3'
setup(
    name='pycommon',
    packages=['pycommon'],
    version=VERSION,
    description='Useful functions missing from the standard libraries',
    author='David Grant',
    author_email='davidgrant@gmail.com',
    url='https://github.com/dgrant/pycommon',
    download_url='https://github.com/dgrant/pycommon/tarball/' + VERSION,
    keywords=['utility', 'miscellaneous', 'library'],
    classifiers=[],
)
