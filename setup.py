from setuptools import setup, find_packages

setup(
    name='dharaai-core',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'rasterio',
        'tensorflow',
        'Pillow'
    ],
    description='Dhara.AI Core precision agriculture pipeline (clean rebuild)',
    author='Suresh Jogur',
    author_email='sureshjogur@gmail.com',
    entry_points={'console_scripts': ['dhara=dhara.dhara_cli:main']},
)
