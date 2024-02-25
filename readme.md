<H1>An example project for Prefect running in ECS using EMR to store codebase.</H1>

## Introduction
This project is an example of how to run a Prefect flow in an ECS cluster using ECR to store the codebase.
The project is divided into three main parts: 
* The ETL pipeline itself. The code which pulls data from an API using python and packaging that code in a docker container.
* The infrastructure. Setting up the ECS cluster and connecting it to both Prefect Cloud and the EMR repo.
* The Prefect code. The code which defines the flow and the tasks which are executed in the ECS cluster using the ETL pipeline and running on the infrastructure.

*(N.B. If anyone is reading this for some reason and finds something confusing, please let me know! Technical communication can be hard and I want this to be as useful as possible!)*


The EMR repo will be used to store the codebase for the ECS cluster.
My goal is to show how I have structured a production-ready ETL pipeline using Prefect.
All of our execution will run in a Docker container stored in an EMR repo, and executed on an ECS cluster.


## The ETL Pipeline
The ETL pipeline is a simple API call to get the exchange rate between two currencies.

The code all lives in 

I chose to use the currency exchange rate API from https://github.com/fawazahmed0/currency-api
The API is free and does not require any registration. Please be nice to fawazahmed0 for providing this service for free.

I do not know much about how this particular API works. It could go down tomorrow, so I will try to structure things in a way that makes it easy to drop in any other general ETL flow.

--------------------------------------------

