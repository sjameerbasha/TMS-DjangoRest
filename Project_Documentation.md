### **Complete Documentation for Task Management System**

---

### **Overview**

This documentation provides an in-depth understanding of the Task Management System, focusing on the database schema, API endpoints, and role-based access control. The system is designed to facilitate efficient task management and project collaboration by offering a robust structure for managing users, projects, tasks, and comments.

The key components of the system include:

- **User Management**: Users are assigned roles such as Admin, Project Manager, Project Lead, Developer, and Client. Each role has different levels of access and permissions within the system.
- **Project Management**: Projects are created and managed by users with appropriate roles. Projects contain tasks that can be assigned to team members.
- **Task Management**: Tasks are associated with projects and can be assigned to specific users. They can have different statuses such as "To Do," "In Progress," or "Done."
- **Commenting System**: Each task allows comments from users, enabling better communication and collaboration.

---

### **User Model** (Inherits from Django's AbstractUser)

#### **Fields:**
- **username**: `CharField`, unique, max length 150.
- **password**: `CharField`, hashed.
- **email**: `EmailField`, unique.
- **role**: `CharField`, choices: `Admin`, `Project Manager`, `Project Lead`, `Developer`, `Client`. Default is `Developer`.
- **first_name**: `CharField`, max length 30.
- **last_name**: `CharField`, max length 30.

#### **Role Permissions:**

1. **Admin**:
   - Full access to all resources and actions.
   - Can view, create, update, and delete users, projects, tasks, and comments.

2. **Project Manager**:
   - Can create and manage projects.
   - Can view tasks within their projects and assign them to users.
   - Can comment on tasks and manage comments within their projects.
   - Cannot modify other users' roles or access user management features.

3. **Project Lead**:
   - Can view tasks and projects they are assigned to.
   - Can comment on tasks and assign tasks within their projects.
   - Limited ability to manage tasks but cannot create or delete projects.

4. **Developer**:
   - Can view tasks assigned to them.
   - Can comment on tasks they are assigned to.
   - Cannot create, update, or delete projects or tasks.

5. **Client**:
   - Can view only projects and tasks they are assigned to.
   - Can only comment on tasks they are associated with.
   - Cannot create, update, or delete tasks or projects.

---

### **Project Model**

#### **Fields:**
- **name**: `CharField`, max length 255.
- **description**: `TextField`, optional (blank=True).
- **created_at**: `DateTimeField`, auto_now_add.
- **users**: `ManyToManyField` to `User`, related name `projects`, representing users associated with the project.
- **created_by**: `ForeignKey` to `User`, related name `created_projects`, on_delete=models.SET_NULL, null=True, blank=True (user who created the project).

#### **Permissions:**
- Admin: Full control over all projects.
- Project Manager: Can create, update, and delete projects they have created.
- Project Lead: Can view and manage tasks in their assigned projects.
- Developer: Can view tasks but cannot create or modify projects.
- Client: Can only view projects they are assigned to.

---

### **Task Model**

#### **Fields:**
- **title**: `CharField`, max length 255.
- **description**: `TextField`, optional (blank=True).
- **project**: `ForeignKey` to `Project`, related name `tasks`, on_delete=models.CASCADE (the project to which the task belongs).
- **assigned_to**: `ForeignKey` to `User`, related name `tasks`, on_delete=models.SET_NULL, null=True, blank=True (the user assigned to the task).
- **status**: `CharField`, choices: `todo`, `in_progress`, `done`. Default is `todo`.
- **created_by**: `ForeignKey` to `User`, related name `task_creators`, on_delete=models.CASCADE (user who created the task).
- **created_at**: `DateTimeField`, auto_now_add.

#### **Permissions:**
- Admin: Full control over all tasks.
- Project Manager: Can create, update, delete tasks within their projects.
- Project Lead: Can assign tasks and update statuses in their projects.
- Developer: Can view and comment on tasks assigned to them, but cannot modify tasks.
- Client: Can view tasks assigned to them and comment on them.

---

### **Comment Model**

#### **Fields:**
- **content**: `TextField`, the content of the comment.
- **task**: `ForeignKey` to `Task`, related name `comments`, on_delete=models.CASCADE (the task to which the comment belongs).
- **project**: `ForeignKey` to `Project`, related name `comments`, on_delete=models.CASCADE (the project to which the comment belongs).
- **user**: `ForeignKey` to `User`, related name `comment_authors`, on_delete=models.CASCADE (the user who wrote the comment).
- **created_by**: `ForeignKey` to `User`, related name `comment_creators`, on_delete=models.CASCADE (the user who created the comment).
- **created_at**: `DateTimeField`, auto_now_add.

#### **Permissions:**
- Admin: Can comment on any task within any project.
- Project Manager: Can comment on tasks within their projects.
- Project Lead: Can comment on tasks within their assigned projects.
- Developer: Can comment on tasks assigned to them.
- Client: Can comment on tasks they are associated with.

---

### **Authentication Mechanism**

- **Login Mechanism**:
   - The system uses **Token-based Authentication** via the Django REST Framework.
   - Users can log in using their **username** and **password**, and they will receive a **token** for authenticated requests.
   - The token must be passed in the `Authorization` header in the format `Token <token_value>` for subsequent requests.

#### **Endpoints for Login:**
- **POST** `/api/auth/login/`: Accepts username and password, and returns an authentication token.

  **Request Body**:
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
  **Request Body**:
  ```json
  {
    "token": "your_auth_token"
  }
  ```
- **POST** `/api/auth/register/`: Allows users to register by providing their username, password, email, and role.

   **Request Body**:
  ```json
  {
    "username": "newuser",
    "password": "newpass123",
    "email": "new@site.com",
    "role": "Client"
  }
  ```
  **Request Body**:
  ```json
  {
    "username": "newuser",
    "role": "Client"
  }
  ```

---

### **Database Schema**

#### **User Table (User Model):**
- **id**: AutoField, Primary Key
- **username**: CharField, max length 150, unique
- **password**: CharField
- **email**: EmailField, unique
- **role**: CharField, choices: Admin, Project Manager, Project Lead, Developer, Client
- **first_name**: CharField, max length 30
- **last_name**: CharField, max length 30

#### **Project Table (Project Model):**
- **id**: AutoField, Primary Key
- **name**: CharField, max length 255
- **description**: TextField
- **created_at**: DateTimeField, auto_now_add
- **users**: ManyToManyField to User
- **created_by**: ForeignKey to User, related name created_projects

#### **Task Table (Task Model):**
- **id**: AutoField, Primary Key
- **title**: CharField, max length 255
- **description**: TextField
- **project**: ForeignKey to Project
- **assigned_to**: ForeignKey to User
- **status**: CharField, choices: todo, in_progress, done
- **created_by**: ForeignKey to User
- **created_at**: DateTimeField, auto_now_add

#### **Comment Table (Comment Model):**
- **id**: AutoField, Primary Key
- **content**: TextField
- **task**: ForeignKey to Task
- **project**: ForeignKey to Project
- **user**: ForeignKey to User
- **created_by**: ForeignKey to User
- **created_at**: DateTimeField, auto_now_add

---

### **API Endpoints**

#### **User Endpoints:**
- **GET** `/api/users/`: List all users (Admin only).
- **POST** `/api/users/`: Create a new user (Admin only).
- **GET** `/api/users/{id}/`: Get a specific user's details.
- **PUT/PATCH** `/api/users/{id}/`: Update a user's details (Admin only).
- **DELETE** `/api/users/{id}/`: Delete a user (Admin only).

#### **Project Endpoints:**
- **GET** `/api/projects/`: List all projects (Admin, Project Manager).
- **POST** `/api/projects/`: Create a new project (Admin, Project Manager).
- **GET** `/api/projects/{id}/`: Get details of a specific project.
- **PUT/PATCH** `/api/projects/{id}/`: Update a project (Admin, Project Manager).
- **DELETE** `/api/projects/{id}/`: Delete a project (Admin, Project Manager).

#### **Task Endpoints:**
- **GET** `/api/tasks/`: List all tasks (Admin, Project Manager, Project Lead).
- **POST** `/api/tasks/`: Create a new task (Admin, Project Manager, Project Lead).
- **GET** `/api/tasks/{id}/`: Get details of a specific task.
- **PUT/PATCH** `/api/tasks/{id}/`: Update a task (Admin, Project Manager, Project Lead).
- **DELETE** `/api/tasks/{id}/`: Delete a task (Admin, Project Manager).

#### **Comment Endpoints:**
- **GET** `/api/comments/`: List all comments.
- **POST** `/api/comments/`: Create a new comment (Authenticated user).
- **GET** `/api/comments/{id}/`: Get details of a specific comment.
- **PUT/PATCH** `/api/comments/{id}/`: Update a comment (Admin, Project Manager, Project Lead).
- **DELETE** `/api/comments/{id}/`: Delete a comment (Admin, Project Manager).

---

### **Conclusion**

The Task Management System is a comprehensive solution designed to streamline project and task management. The system leverages Django's powerful ORM for managing complex relationships between users, projects, tasks, and comments, while ensuring that role-based permissions are enforced for secure access.

By using a clear and scalable database schema and exposing a set of well-defined API endpoints, the system provides an easy-to-use interface for users with varying levels of access. The role-based access control ensures that only authorized users can perform certain actions, making it a secure and effective tool for teams to manage their workflows.

This documentation serves as a reference for developers and users to understand the structure and functionality of the system, facilitating easy development and future expansion.
