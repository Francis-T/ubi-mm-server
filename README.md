# Mutual Monitoring Server

## Pre-requisites
* Docker

## How to use / deploy
1. Using the terminal/command line, Git Clone this repository into a directory
2. Navigate to that directory
3. Type `docker build -t mm_server` and press enter to execute. This will build the Docker image on your machine.
4. Type `docker run -it -p8080:80 mm_server` and press enter to execute. This will run the Mutual Monitoring Server for as long as the terminal remains open.

## How to shutdown the server
* Bring up the terminal where the Mkutual Monitoring Server is running. Press 'CTRL+C'

