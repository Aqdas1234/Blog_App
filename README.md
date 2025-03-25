# Blog App Backend

This is a **Django REST Framework** (DRF)–based backend for a blog application that allows users to create, update, and manage blog posts with images and videos. It includes authentication using **JWT tokens** and supports formatted content with **CKEditor5**.

## Features

- **User Authentication**: JWT-based authentication (Signup, Login, Logout)
- **Blog Post Management**: CRUD operations for blog posts
- **Rich Text Editing**: CKEditor5 for enhanced text formatting
- **Media Support**: Upload images and videos using `FileField`
- **Pagination**: Blog listing with pagination
- **Permissions**: Only authors can edit or delete their posts

## Technologies Used

- **Django** (Backend framework)
- **Django REST Framework (DRF)** (API development)
- **Simple JWT** (Authentication)
- **CKEditor5** (Rich text content)



## Installation

### 1. Clone the repository

```bash
  git clone https://github.com/your-username/blog-app-backend.git
  cd blog-app-backend
```

### 2. Create a virtual environment and activate it

```bash
  python -m venv venv
  source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies

```bash
  pip install -r requirements.txt
```

### 4. Apply migrations

```bash
  python manage.py migrate
```

### 5. Create a superuser (optional)

```bash
  python manage.py createsuperuser
```

### 6. Run the server

```bash
  python manage.py runserver
```

## API Endpoints

### Authentication

- `POST /api/signup/` → User signup
- `POST /api/login/` → Obtain JWT access and refresh tokens
- `POST /api/logout/` → Logout user

### Blog Posts

- `GET /api/blogs/` → List all blog posts
- `POST /api/blogs/create/` → Create a new blog post (Authenticated users only)
- `GET /api/blogs/{id}/` → Retrieve a single blog post
- `PUT /api/blogs/{id}/` → Update a blog post (Only author)
- `DELETE /api/blogs/{id}/` → Delete a blog post (Only author)

##

---

Feel free to contribute or report issues in the repository!


