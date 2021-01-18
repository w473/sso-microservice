from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask', 'PyMySQL', 'PyMySQL[rsa]', 'bcrypt',
        'jsonschema', 'jsonschema[format]', 'pytest',
        'requests', 'jwcrypto', 'passlib', 'python-dotenv',
        'git+git://github.com/lobocode/flask-graylog'
    ],
)
