from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask', 'PyMySQL', 'PyMySQL[rsa]', 'pycrypto', 'pycryptodome', 'bcrypt',
        'jsonschema', 'jsonschema[format]', 'pytest', 'requests', 'jwcrypto', 'passlib'
    ],
)
