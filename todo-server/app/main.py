from fastapi import FastAPI


app = FastAPI(
    title="Cax",
    description="A multi-user to-do microservice for efficient task management.",
    version="1.0.0",
    terms_of_service="https://cax.vercel.app/terms/",
    contact={
        "name": "Muhammad Junaid",
        "url": "https://www.linkedin.com/in/mrjunaid/",
        "email": "mr.junaidshaukat@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
    ],
    docs_url="/api/docs"
)


