# Hackathon-Events

## Overview

This repository contains the source code for Hackathon, which is hosted on github. The development workflow involves two main branches: `main` and `dev`. Changes are developed and tested in the `dev` branch before being merged into `main`. The production deployment of the `main` branch is automatic and is hosted on Stalingo.

## Infrastructure

### Version Control System (VCS)

The project uses github as its version control system. The main branches are:

- `main`: Represents the stable version of the application.
- `dev`: Development branch where new features and bug fixes are implemented.

### Deployment Platform

Stalingo is used for deploying and hosting the application. 

### Continuous Integration (CI)

 is used for automating the build and deployment processes. The CI pipeline is triggered on each push to the `dev` branch. It includes the following steps:

**Trigger**: Activates on push to the Dev branch.

**Python Compatibility**: Tests against Python 3.9, 3.10, 3.11.

**Linting**: Uses Flake8 for code quality checks and syntax errors

**HTML code validation**: Verifies the syntax of the HTML code

**Automated Pull Request Creation**: Creates a pull request from Dev to main after successful checks.

### Development Workflow

1. Developers clone the repository and create feature branches from the `dev` branch.
2. Code changes are made and tested in the feature branches.
3. Pull requests are submitted to merge changes into the `dev` branch.
4. Continuous Integration tests are automatically run on the `dev` branch.
5. Once changes are validated, a pull request is created to merge into the `main` branch.
6. If the pull request is validated. Changes on the `main` branch are automatically deployed with Scalingo.

### Website 

The url linked to our repository is the following : https://hackathon-events.osc-fr1.scalingo.io/
The website is centered around organizing and participating in cultural events in Nantes. 

### Repository structure

This repository is structured for a Python-based web application with Docker support and deployment configurations for Scalingo, a cloud platform. Below are the contents and their respective roles:

- `/.github/workflows/` - Contains GitHub Actions CI workflow definitions, which automate testing  process.
- `/templates/` - Stores HTML templates for the Flask web application, used to render the frontend.
- `app.py` - The main Python script for the Flask web application. It defines routes and server logic.
- `docker-compose.yml` - A Docker Compose file that defines the services, networks, and volumes for a multi-container Docker application.
- `Dockerfile` - Instructions for building a Docker image for the web application.
- `Pipfile` - Defines Python package dependencies for use with Pipenv, which is a packaging tool for Python.
- `Pipfile.lock` - A locked version of dependencies from Pipfile to ensure consistent installations across environments.
- `Procfile` - Used by Scalingo and other platform-as-a-service providers to declare the command that starts the application.
- `requirements.txt` - A list of Python package dependencies for traditional pip installations.
- `scalingo.json` - Contains configurations specific for Scalingo, such as add-ons or environment variables.
- `/tests/test_functionalities.py` - Contains the unit tests for each implemented functionality in the application and ensures that the code is working perfectly fine.

Each file and directory is part of the project's setup, configuration, or the application itself, ensuring smooth deployment and development cycles.

### Security measures

To ensure security, we have put in place a number of measures, such as :
- The "main" branch is protected, you can't push directly into it, and you have to make a pull request to merge the code from the "Dev" branch into the "main" branch
- The API_KEY used to display the movies is hidden.

### Importing new librairies to the repository

If you want to import new python packages into the app.py file, you need to add them to the Pipfile.lock and Procfile files. To do this, install pipenv via pip and run "pipenv lock" in a terminal.
