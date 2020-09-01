from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='video_player',
    version='0.0.1',
    description='Service to generate endpoint for video output',
    long_description=readme(),
    classifiers=[
        'License :: OSI Approved :: MIT Licence',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],

    keywords='',
    url='',
    author='Fernando Herrera',
    author_email='fernando.j.herrera@gmail.com',
    license='MIT',

    python_requires='>=3.7',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "opencv_contrib_python==4.1.0.25",
        "imutils==0.5.3",
        "flask==1.1.1",
        "gunicorn==19.9.0",
        "nose==1.3.7",
        "coverage==4.5.4",
        "pytest==5.1.1",
    ],

    include_package_data=True,
    zip_safe=False,

    entry_points={
        'console_scripts': ['start-player=video_player:main']
    }
)
