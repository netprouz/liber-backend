![Django project](https://gitlab.com/Bobur/book.git)

Online book retailer application backend
============================



Folder Structure Conventions
============================

> Folder structure options and naming conventions for the current project

### A typical top-level directory layout

    .
    ├── .envs                   # Environment veriables
    ├── compose                 # Docker files and bash commands
    ├── requirements            # Third party libraries
    ├── config                  # Project configuration files 
    ├── src                     # Project applicateions directory ('lib' or 'apps') 
    ├── local.yml               # docker-compose (running in local)
    ├── production.yml          # docker-compose (to deploy in production)
    └── README.md

### Outline

- Prerequisites
- Setup
    - Development
    - Production
- Documentation

## Prerequisites

> This project has the following prerequisites

- python 3.9.8
- docker 20.10.12
- docker-compose 1.29.2

### Setup (development)


> Install virtual environment (optional):

```
git clone git@github.com:ArtelCyberspaceUZ/online_marketplace.git
cd online_marketplace
python -m venv --prompt="v" .env
```

>If *pre commit* has not been installed please install by running following command (optional):

```
pip install pre-commit
pre-commmit install
```

> Type the command below to run the project locally:

```
docker-compose -f local.yml up -d
```

- You should be good to go now
