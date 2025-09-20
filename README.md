# 📲 Social Media Feed Backend

The **Social Media Feed Backend** is a Django-based backend system designed to power a social media feed.  
It focuses on **GraphQL APIs**, **real-time interactions**, and **scalable database design** to handle posts, comments, likes, and shares.

This project was developed as part of the **ProDev Backend Engineering program**, showcasing backend best practices and advanced API design.

---

## 📑 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

### 1. **Post Management**

- Create, update, and delete posts.
- Query posts with flexible filtering (by user, date, or popularity).

### 2. **User Interactions**

- Like, comment, and share posts.
- Track interactions for analytics (e.g., most liked posts).

### 3. **GraphQL API**

- GraphQL schema for querying posts and interactions.
- GraphQL Playground for testing queries and mutations.

### 4. **Scalability**

- Optimized PostgreSQL schema for large datasets.
- Efficient resolvers for handling feed queries.

### 5. **Permissions & Authentication**

- Role-based access (admin, standard user).
- Secure endpoints with JWT or Django authentication.

---

## Prerequisites

- **Python 3.8+**
- **PostgreSQL 13+**
- **Docker & Docker Compose** (recommended for setup)
- **Git**

---

## Installation

You can run this project either **via Docker** or in a **local Python environment**.

---

### **Method 1 — Docker Compose (Recommended)**

1. **Clone the repository**

```bash
git clone https://github.com/AustinMusuya/connectu-platform-backend.git
cd connectu-platform-backend
```

2. **Create `.env` file**

```bash
cp .env_example .env
```

Example `.env`:

```env
POSTGRESQL_DB=social_feed_db
POSTGRESQL_USER=my_user
POSTGRESQL_PASSWORD=my_pass
DB_HOST=db
DB_PORT=5432
```

3. **Start containers**

```bash
docker compose up -d
```

4. **Apply migrations**

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

5. **Create a superuser**

```bash
docker compose exec web python manage.py createsuperuser
```

6. **Access the application**

- Django server: `http://127.0.0.1:8000/`
- GraphQL Playground: `http://127.0.0.1:8000/graphql/`
- Admin panel: `http://127.0.0.1:8000/admin/`

---

### **Method 2 — Local Virtual Environment**

1. **Clone the repository**

```bash
git clone https://github.com/AustinMusuya/connectu-platform-backend.git
cd connectu-platform-backend
```

2. **Create virtual environment**

```bash
python3 -m venv env
source env/bin/activate   # Mac/Linux
env\Scripts\activate      # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure database in `settings.py`**  
   Example (PostgreSQL):

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'social_feed_db',
        'USER': 'your-username',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

5. **Apply migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create a superuser**

```bash
python manage.py createsuperuser
```

7. **Run server**

```bash
python manage.py runserver
```

---

## Usage

### Admin Features

- Manage users, roles, and permissions via `/admin/`.
- Monitor posts, comments, and interactions.

### User Features

Query and mutate posts using the **GraphQL Playground**.

#### Authentication Guide
- [Authentication Guide](./Authentication.md)

#### User Interactions Guide
- [User Interactions](./User-Interactions.md)

#### Posts, Likes, Comments & Nested Comments Guide
- [Post Comments Likes](./Posts-Comments-Likes.md)

---

## Screenshots

GraphQL Playground:  
![GraphQL Playground](assets/graphql_playground.png)

Admin Panel:  
![Admin Panel](assets/admin_panel.png)

---

## Testing

Run tests using:

```bash
python manage.py test
```

Or via Docker:

```bash
docker compose exec web python manage.py test
```

---

## 🤝 Contributing

1. Fork this repo
2. Create a new branch (`feature/awesome-feature`)
3. Commit changes (`git commit -m "feat: add new feature"`)
4. Push branch (`git push origin feature/awesome-feature`)
5. Open a Pull Request 🎉

---

## 📜 License

MIT License
