# calibrate-google-trends
*This project fork from GoogleTrendsAnchorBank with the aim to integrate with mongodb.*


## Set up the environment, and Install dependencies
1. Install [docker](https://docs.docker.com/get-docker/)
2. modify the `.env.example`, assigning the environment variables and rename it as `.env`
3. create the docker image:
```bash
make build
```
To clean up the docker image:
```sh
make clean
```


## Container Services
```sh
# unit test
make pytest

# project documentation
make doc

# development IDE - Jupyter Lab
make jupyter
```


## Usage
1. download the [MongoDB](https://www.mongodb.com/try/download/community) and start the server
2. modify the `.env.example`, assigning the environment variables and rename it as `.env`
3. modify the configuration file - `config/main.yaml`
4. run the program
```sh
# Note: the log file will be stored under `log/{db_name}/{collection_name}`
make up
```
5. stop the container
```sh
make down
```
