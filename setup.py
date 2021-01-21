from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='SqueakyClean',
    url='https://github.com/Vincent-Chung/SqueakyClean',
    author='Vincent Chung',
    #author_email='NeedToMakePublicEmail@SomeEmail.com',
    # Needed to actually package something
    packages=['measure'],
    # Needed for dependencies
    install_requires=['numpy','pandas'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license
    license='TO BE DETERMINED',
    description='Simple functions for pandas users to make life easier'
)
