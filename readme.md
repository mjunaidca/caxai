# CaX: Applied GenAI Multi User Todo GPT App

Implementation of Microservices GenUI Architecture. The Current Microservices are:

- auth-server: Auth Server to manage Authentication & Authorization
- todo-server: Simple ToDo Server to authenticate using auth-server & perform TODOs Crud.
- nextjs-client: Conversational GenUI & TODOs Manager platform for you.



# Deployment

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
