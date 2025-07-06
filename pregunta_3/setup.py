from setuptools import setup, find_packages

setup(
    name="medical-image-processing-api",
    version="1.0.0",
    description="RESTful API for managing medical image processing results",
    author="Developer",
    author_email="developer@example.com",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0",
        "sqlalchemy>=2.0.23",
        "psycopg2-binary>=2.9.9",
        "pydantic>=2.5.0",
        "python-multipart>=0.0.6",
        "python-dotenv>=1.0.0",
        "alembic>=1.12.0",
    ],
    extras_require={
        "dev": [
            "black>=23.0.0",
            "flake8>=6.0.0",
            "isort>=5.12.0",
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "requests>=2.31.0",
        ]
    },
    python_requires=">=3.11",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
