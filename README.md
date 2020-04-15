# Mutual Monitoring Server

## Pre-requisites
* Docker must be installed on your machine (see https://docs.docker.com/get-docker/)

## How to deploy the server
1. Using the terminal/command line, Git Clone this repository into a directory
2. Navigate to that directory
3. Type `docker build -t mm_server` and press enter to execute. This will build the Docker image on your machine.
4. Type `docker run -it -p8080:80 mm_server` and press enter to execute. This will run the Mutual Monitoring Server for as long as the terminal remains open.

## How to use / test the server
* First, find out the IP address of your machine. Please consult your OS manual on how to do this.
* Bring up your browser and type the following (replace the part in < > with your IP address): `http://<YOUR IP ADDRESS HERE>:8080/api`
* Your browser should receive some JSON formatted information.

## How to shutdown the server
* Bring up the terminal where the Mutual Monitoring Server is running. Press `CTRL+C`.

