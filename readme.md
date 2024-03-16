# CaX: Applied GenAI Multi User Todo GPT App

Implementation of Microservices GenUI Architecture. The Current Microservices are:

- auth-server: Auth Server to manage Authentication & Authorization
- todo-server: Simple ToDo Server to authenticate using auth-server & perform TODOs Crud.
- nextjs-client: Conversational UI & TODOs Manager platform for you.

# Running Locally & Development:

You can setup & run the project locally on your machine or on docker. Firstly let'e setup the env vars.

- In auth-server
` Rename .env.example to .env and add DB_URL, TEST_DB_URL, SECRET_KEY `

- In todo-server add DB_URL & TEST_DB_URL. They can be same as above or different

- For nextjs-client run pnpm install - no need to update them

### 1. Local Machine

Open root dir i.e: cax in terminal and run 

1. Terminal 1: `make auth` & visit `http://localhost:8080/api/docs`
2. Terminal 2: `make todo` & visit `http://localhost:8000/api/docs`
3. Terminal 3: `make next` & visit `http://localhost:3000`


### 2. Docker

Rename root .env.example to .env and add the missing env vars (DB_URL=, TEST_DB_URL=, SECRET_KEY=)

Run: `docker compose -d up`

# Deployment:

We will be deploying FastAPI Microservices to Google Cloud Run and NextJS CUI to Vercel.

0. Ensure your have gcloud and vercel cli installed & authenticated

1. auth-server

```
cd auth-server

gcloud run deploy auth-server --source . --port 8080 --env-vars-file .env.gcp.yaml --allow-unauthenticated --region us-central1 --min-instances 1
```

2. todo-server
```
cd todo-server

gcloud run deploy todo-micro-server --source . --port 8000 --env-vars-file .env.gcp.yaml --allow-unauthenticated --region us-central1 --min-instances 1
```

3. nextjs-client

```
cd nextjs-client

vercel link
```

Then visit vercel and add all env vars to your project and in terminal run:

`vercel --prod`
