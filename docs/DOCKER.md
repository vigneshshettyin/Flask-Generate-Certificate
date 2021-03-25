## Using Docker

* Install [Docker](https://docs.docker.com/engine/install/) according to your machine type and requirements

* Once Docker is installed, use the following two commands to run the app in the root dicrectory:
  * `docker-compose build` , This command will build the project
  * `COMPOSE_HTTP_TIMEOUT=200 docker-compose up`, This command will run the container.

* You can open the project on `localhost:5000` on the machine.

Note: If you are using `docker-desktop` on Windows Or [WSL2](https://www.omgubuntu.co.uk/how-to-install-wsl2-on-windows-10) i.e Windows Subsystem For Linux, you can use the GUI Options to run the containers
