# Task Management System (TMS)

## Overview

The Task Management System (TMS) is a web application built with Django, designed to help teams efficiently manage projects, tasks, and comments. The system is role-based, providing different access levels for users, including Admin, Project Manager, Project Lead, Developer, and Client.

---

### Features:
- **User Management**: Role-based access control.
- **Project Management**: Creation, viewing, and management of projects.
- **Task Management**: Assignment of tasks, setting of task statuses (To Do, In Progress, Done).
- **Commenting System**: Each task has a commenting feature for team collaboration.
- **Email Notifications** : User will be notified with an email when a task is assigned.

    ![email_notification](https://github.com/user-attachments/assets/7e9161a8-88ea-4729-b51a-7398260d065d)


## GitHub Clone Instructions

### Step 1: Clone the Repository
To clone this repository, run the following command in your terminal:
```bash
git clone https://github.com/sjameerbasha/TMS-DjangoRest.git
```

### Step 2: Set Up the Virtual Environment
Navigate to the below directory:
```bash
cd TMS-DjangoRest-main
```
Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
Run the following command to install the required Python packages:
```bash
pip install -r requirements.txt
```

### Step 4: Navigate to the project directory
Navigate to the project directory:
```bash
cd tms_backend
```

### Step 5: Migrate the Database
Run the following commands to apply database migrations:
```bash
python manage.py migrate
```

### Step 6: Create a Superuser
To access the admin panel and perform CRUD operations, create a superuser account:
```bash
python manage.py createsuperuser
```

### Step 7: Run the Development Server
Start the development server with:
```bash
python manage.py runserver
```
The application will be running at `http://127.0.0.1:8000/`.

---

## Project Structure
```bash
        TMS-DjangoRest/
        │
        ├── tms_backend/
        │   ├── manage.py                 # Django project management script
        │   ├── core/                     # Core app for models and user management               
        │   ├── api/                      # App for API views and serializers
        │   ├── templates/                # HTML templates (if needed for views)
        │   ├── static/                   # Static files (CSS, JS)
        │   └── settings.py               # Django settings configuration
        │
        ├── output/                       # Output Screenshots
        │   ├── api_endpoint_requests     # Various API Requests Responses
        │   ├── email_notifications/      # Email Notification               
        │   └── tests_output/             # Tests Cases Result
        ├── venv/                         # Virtual environment
        ├── sample_data.json              # Sample data 
        ├── requirements.txt              # List of Python dependencies
        └── README.md                     # Project documentation
```

The project is structured into several core applications, each responsible for specific tasks:

1. **Core App (core/)**: Contains the essential models for the application such as User, Project, Task, and Comment.
2. **API App (api/)**: Handles the Django REST Framework views, serializers, and URL routing for the Task Management API.
3. **Output Folder (output/)**: This folder contains all the output screenshots.
4. **Sample Data (sample_data.json)**: This file contains sample data to populate the system and test various functionalities.

---

## Models and Role-Based Access

### User Model
The `User` model inherits from Django’s `AbstractUser` and includes additional fields for user roles. The roles are:

- **Admin**: Full access to all resources.
- **Project Manager**: Manage projects and tasks but cannot modify user roles.
- **Project Lead**: Limited task management within assigned projects.
- **Developer**: View and comment on assigned tasks.
- **Client**: View and comment on tasks within their projects.

### Project Model
The `Project` model defines the structure of projects and their relationships with users and tasks. Permissions are role-dependent.

### Task Model
The `Task` model describes tasks within a project. Permissions allow managing tasks only within authorized projects.

### Comment Model
The `Comment` model supports comments on tasks. Permissions depend on user roles and their involvement in tasks.

---

## API Endpoints

### Authentication Endpoints:
- **POST** `/api/auth/login/`: Logs in a user and returns a token.
- **POST** `/api/auth/register/`: Registers a new user.

### User Endpoints:
- **GET** `/api/users/`: List all users (Admin only).
- **POST** `/api/users/`: Create a new user (Admin only).
- **GET** `/api/users/{id}/`: Get a user's details.
- **PUT/PATCH** `/api/users/{id}/`: Update a user's details (Admin only).
- **DELETE** `/api/users/{id}/`: Delete a user (Admin only).

### Project Endpoints:
- **GET** `/api/projects/`: List all projects (Admin, Project Manager).
- **POST** `/api/projects/`: Create a new project (Admin, Project Manager).
- **GET** `/api/projects/{id}/`: Get details of a specific project.
- **PUT/PATCH** `/api/projects/{id}/`: Update a project (Admin, Project Manager).
- **DELETE** `/api/projects/{id}/`: Delete a project (Admin, Project Manager).

### Task Endpoints:
- **GET** `/api/tasks/`: List all tasks (Admin, Project Manager, Project Lead).
- **POST** `/api/tasks/`: Create a new task (Admin, Project Manager, Project Lead).
- **GET** `/api/tasks/{id}/`: Get details of a specific task.
- **PUT/PATCH** `/api/tasks/{id}/`: Update a task (Admin, Project Manager, Project Lead).
- **DELETE** `/api/tasks/{id}/`: Delete a task (Admin, Project Manager).

### Comment Endpoints:
- **GET** `/api/comments/`: List all comments.
- **POST** `/api/comments/`: Create a new comment (Authenticated user).
- **GET** `/api/comments/{id}/`: Get details of a specific comment.
- **PUT/PATCH** `/api/comments/{id}/`: Update a comment (Admin, Project Manager, Project Lead).
- **DELETE** `/api/comments/{id}/`: Delete a comment (Admin, Project Manager).

---

## Authentication

The system uses Token-based Authentication for secure API access. Users must log in via the `/api/auth/login/` endpoint and include the generated token in the `Authorization` header of subsequent requests:

```bash
Authorization: Token <token_value>
```

---

## Sample Data

For initial testing and seeding the system with data, the `sample_data.json` file can be used. This file contains predefined sample data for users, projects, tasks, and comments that you can load into the database.

---

## Conclusion

The Task Management System is an efficient solution for managing projects, tasks, and team collaboration. With role-based access control and robust permissions, it ensures that only authorized users can perform specific actions. The system is scalable and flexible, making it suitable for a variety of use cases in different industries.

This README provides a detailed guide on how to clone, set up, and run the Task Management System. Feel free to extend and modify it based on your project's specific needs.

```bash
Happy Coding!!!
```



