from setuptools import setup, find_packages

setup(name='PDFDataExtractor',
      version='0.1',
      description='Extract data from a pdf file',
      url='',
      author='Mo',
      author_email='mnokhb@gmail.com',
      license='MIT',
      install_requires=[
            'PyPDF2==1.26.0',
            'PyYAML==3.11'
      ],
      packages=find_packages(),
      zip_safe=False)
