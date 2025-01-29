# Todo-List Backend (Django REST Framework)

## Overview
This project is a backend for a Todo-List API built using Django REST Framework. It provides a robust API for managing tasks, user authentication and authorization. The project focuses on applying best practices in backend development, including secure user authentication using JWT, efficient CRUD operations for managing tasks, and important concepts like pagination and database optimization using Django ORM methods.

The backend also integrates the Groq AI model to generate relevant hashtags for task titles, enhancing the user experience by organizing tasks more effectively.

---

## Main Project Aims
The primary goals of this project are:
1. **User Authentication and Authorization**: Implement secure user authentication and authorization using JSON Web Tokens (JWT) via the `SimpleJWT` package.
2. **CRUD Operations**: Provide Create, Read, Update, and Delete (CRUD) functionality for managing todo lists and tasks.
3. **Concepts**: Apply pagination for efficient data retrieval and utilize Django ORM methods for optimized database interactions.
4. **AI Integration**: Use the Groq AI model to generate hashtags related to task titles, improving task organization and searchability.

---

## Technologies and Packages
- **Backend Framework**: Django REST Framework
- **Authentication**: SimpleJWT (for JWT-based user authentication)
- **AI Integration**: Groq AI model (for generating hashtags related to task titles)
- **Database**: SQLite (default) 
- **Other Features**: Pagination, Django ORM methods, and RESTful API design

---

## Key Features
- **User Authentication**: Secure user registration, login, and token-based authentication.
- **Task Management**: Full CRUD functionality for tasks and todo lists.
- **Pagination**: Efficiently handle large datasets by paginating task lists.
- **Hashtag Generation**: Automatically generate hashtags for tasks using the Groq AI model.
- **Best Practices**: Follow Django and REST framework best practices for clean and maintainable code.

---

## Endpoints

### User Authentication Endpoints
1. **Register a New User**  
   - **URL**: `/api/v1/user/register/`  
   - **Method**: `POST`

2. **Login (Obtain JWT Tokens)**  
   - **URL**: `/api/v1/user/login/`  
   - **Method**: `POST`

3. **Refresh Access Token**  
   - **URL**: `/api/v1/user/api/token/refresh/`  
   - **Method**: `POST`

4. **Logout (Blacklist Refresh Token)**  
   - **URL**: `/api/v1/user/logout/`  
   - **Method**: `POST`

---

### Todo List Endpoints
1. **Create a New Todo**  
   - **URL**: `/api/v1/lists/todos/`  
   - **Method**: `POST`

2. **Get All Todos**  
   - **URL**: `/api/v1/lists/todos/`  
   - **Method**: `GET`

3. **Get a Single Todo**  
   - **URL**: `/api/v1/lists/todos/<int:pk>/`  
   - **Method**: `GET`

4. **Update a Todo**  
   - **URL**: `/api/v1/lists/todos/<int:pk>/`  
   - **Method**: `PUT`

5. **Delete a Todo**  
   - **URL**: `/api/v1/lists/todos/<int:pk>/`  
   - **Method**: `DELETE`

6. **Update Todo Status**  
   - **URL**: `/api/v1/lists/update-list-status/<int:pk>/`  
   - **Method**: `PATCH`

7. **Get Paginated Todos (Limit-Offset)**  
   - **URL**: `/api/v1/lists/todos-paginated-l/`  
   - **Method**: `GET`

8. **Get Paginated Todos (Page Number)**  
   - **URL**: `/api/v1/lists/todos-paginated-p/`  
   - **Method**: `GET`

9. **Get Paginated Todos (Custom Pagination)**  
   - **URL**: `/api/v1/lists/todos-paginated/`  
   - **Method**: `GET`

---

## How to Use
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run migrations: `python manage.py migrate`.
4. Start the development server: `python manage.py runserver`.
5. Access the API endpoints via `http://localhost:8000/`.

---
