# Cal AI: MultiUser AI Powered Personal ToDo Web App

## Project Structure

The project is developed and deployed under different cloud architectures. Each follows a modular and organized structure to ensure maintainability and scalability. Here is an overview of the main directories:

- `nextjs_app_fastapi`: A Complete API Microservice and Web App deployed on VERCEL. Active development to add Applied GenAI features is continued for it :D
    - Visit it's readme for all development, getting started, features and deployment details

- `fastapi_cloud_msa`: 
    - Contains the FastAPI backend code, including API routes, models, and database configurations.
    - Containorized using Docker and Deployed on Google Run
- `nextjs_msa_fe`: Frontend developed for the `fastapi_cloud_msa` backend and deplyed on Vercel
- `streamlit_mjs_prototype`: Frontend prototype developed in streamlit and deployed on streamlit cloud.

The project structure is designed to promote code organization, separation of concerns, and ease of collaboration among team members.

## Overview

Cal AI is an end-to-end cloud GenAI multi-user project that showcases the architecture for an API-first modern web application. It utilizes a layered architecture development approach and includes a Gen AI powered API microservice, a NextJS14 frontend, and a serverless PostgreSQL database powered with SQLAlchemy ORM. The project also includes unit tests, API tests, and end-to-end tests using Pytest.

## Inspiration

Cal AI started as a simple todo app but has evolved to include all the features the developer wanted in a task management web app. It is a personal project that has been open-sourced for others to learn from and potentially use.

**Note: The project is still a work in progress.**

## Run Database Migrations with Alembic

To run migrations using Alembic, follow these steps:

1. Run `alembic init migrations` to initialize the migrations directory.

2. In `alembic.ini`, remove the URL in the `sqlalchemy.url` field.

3. In `migrations/env.py`, import `dotenv` and add the following code:


## Pre Development Planned Features

- A Notion-like weekly to-do list where users can add todos for each week. At the end of the week, the sheet is deleted while the todos are saved in the database.
- AI-powered text-based daily task notifications or reminders.
- Weekly analysis of tasks completed, including time spent on learning and recursive tasks.
- Integration with messaging platforms like WhatsApp, Skype, or Slack for daily work notifications.

## Future GenAI Personalization Features

### Adaptive Task Prioritization

- Problem: Users struggle with constantly changing priorities and task overload.
- AI Solution: Implement an AI algorithm that learns from the user's task completion patterns and adjusts task priorities accordingly. For example, if a user consistently prioritizes work-related tasks in the mornings, the app could automatically adjust future task priorities.

### Predictive Scheduling and Reminders

- Problem: Users often underestimate the time required for tasks or forget deadlines.
- AI Solution: AI could analyze past task completion times and suggest realistic timeframes for new tasks. It could also anticipate and remind users of recurring tasks based on historical data.

### Integration with Other Tools

- Problem: Current apps often exist in isolation, not syncing well with other productivity tools.
- AI Solution: Develop AI capabilities to integrate and sync data with other apps (like calendars, emails) to provide a unified task management system. For example, AI can suggest to-do items from emails or meetings scheduled in the calendar.

### Context-Aware Suggestions

- Problem: Users receive generic task suggestions that might not align with their current context or needs.
- AI Solution: Utilize AI to offer context-aware suggestions, like recommending grocery shopping when the user is near a supermarket, based on location data and past behavior.

### Voice-Activated Controls

- Problem: Manual entry of tasks can be cumbersome.
- AI Solution: Implement sophisticated voice recognition to allow users to add tasks hands-free, enhancing accessibility and convenience.

## Running Locally 
Refer to nextjs_app_fastapi dir readme.md for all setup, configuration and development details. Or feel free to reach out if you face any issues whiles testing or running it locally.