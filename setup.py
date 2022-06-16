from setuptools import setup, find_packages

setup(
    name='grandid',
    version='0.1.3',
    description='GrandID Client',
    author='Datatrion AB',
    author_email='info@datatrion.se',
    url='https://www.datatrion.se',
    packages=find_packages(),
    license="MIT",
    keywords=[],
    classifiers=[],
    install_requires=[
        'requests',
        'six'
    ],
    extras_require={
        'testing': [
            'requests_mock',
        ],
    },
    test_suite='grandid',
)
