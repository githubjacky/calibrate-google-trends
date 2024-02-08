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
