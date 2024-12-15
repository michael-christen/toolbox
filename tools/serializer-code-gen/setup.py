import setuptools

setuptools.setup(
    name="serializer-code-gen",
    version="0.1.0",
    url="https://github.com/michael-christen/serializer-code-gen",

    author="Michael Christen",
    author_email="mchristen96@gmail.com",

    description="A code generation tool for switching between serialization frameworks.",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
