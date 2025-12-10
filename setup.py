from setuptools import setup, find_packages

setup(
    name="tataco-mvp",
    version="0.4.0",
    description="Hand Gesture Controlled Remote System",
    author="Tataco Team",
    packages=find_packages(),
    install_requires=[
        "opencv-python>=4.8.0",
        "mediapipe>=0.10.0",
        "pyserial>=3.5",
        "numpy>=1.24.0",
    ],
    entry_points={
        "console_scripts": [
            "tataco=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
)
