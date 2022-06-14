from setuptools import setup, find_packages

# noinspection PyPackageRequirements
setup(
    name='grandid',
    version='0.1',
    description='GrandID Client',
    author='Datatrion AB',
    author_email='info@datatrion.se',
    url='https://www.datatrion.se',
    packages=find_packages(),
    keywords=[],
    classifiers=[],
    install_requires=[
        'requests',
    ],
    extras_require={
        'testing': [
            'requests_mock',
        ],
    },
    test_suite='grandid',
)
