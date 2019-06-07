from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='open_mlstat',
      use_scm_version=True,
      setup_requires=['setuptools_scm'],
      install_requires=required,
      description='Open machine learning statistics saver (using google drive api)',
      url='http://github.com/ostfor/open_mlstat',
      author='Denis Brailovsky',
      author_email='denis.brailovsky@gmail.com',
      license='MIT',
      data_files=[('', ['LICENSE', 'CHANGELOG'])],
      packages=["open_mlstat.{}".format(pkg) for pkg in find_packages("open_mlstat")] + ["open_mlstat"],
      zip_safe=False)