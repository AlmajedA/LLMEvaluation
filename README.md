# LLM Evaluation Web Application

## Project Overview
This project is a web application designed to evaluate the responses of different Large Language Models (LLMs) in a Question and Answering task. The application allows users to compare and analyze the performance of various LLMs by inputting questions and observing the responses generated.

## How to Run

### Step 1: Create a .env File
First, create a `.env` file using the `.env.sample` file as a template. This file should contain all necessary environment variables required for the application to run.

### Step 2: Deploy with Docker Compose
Run the deploy docker compose to set up and start the application. Use the following command:

```sh
docker-compose -f docker-compose-deploy.yml up --build
```

### Step 3: Access the Application
Once the application is up and running, you can access it locally by navigating to [link](http://127.0.0.1/) in your web browser.

Alternatively, you can try the hosted version of the application at [link](https://llmevaluation.up.railway.app/).


## Structure of the Code

### Scraping Folder
The `scraping` folder contains the logic for data scraping. This process is performed independently before implementing the application, ensuring that all necessary data is collected and processed beforehand.

### Backend Folder
The `backend` folder contains a Django application structured into two main apps:
* LLMs App: Manages the logic and operations related to Large Language Models.
* VectorDB App: Handles the vector database operations.

#### Vector DB
For the vector database, ChromaDB is used to create embeddings and perform searches for similar documents. This enhances the application's ability to find relevant information efficiently.

### Nginx
Nginx serves as the proxy server for the application and also contains the frontend logic. It manages incoming requests and directs them appropriately to the backend services, ensuring smooth operation and performance.