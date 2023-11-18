![image](https://github.com/netprouz/liber-backend/assets/89244992/098497c6-9752-4129-8800-977968ec6ed9)


![image](https://github.com/netprouz/liber-backend/assets/89244992/cf2d5e04-8a50-4c35-9e02-f0d1ee2f9e3e)


![image](https://github.com/netprouz/liber-backend/assets/89244992/234a9df7-f2de-4da4-8091-797e881db891)


![image](https://github.com/netprouz/liber-backend/assets/89244992/c64d7a5f-237a-4baf-a79e-1bc92f2fc17c)



Backend test project for RochWin
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
