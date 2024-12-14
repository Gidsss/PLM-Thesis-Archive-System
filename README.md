# PLM Thesis Archive System

## Overview
The **PLM Thesis Archive System** is a digital repository for managing, storing, and retrieving academic theses and research papers. This project is built with the Django framework and uses a MySQL/MariaDB database.

## Prerequisites
- Python 3.12 or later
- Django 4.2
- MySQL or MariaDB (10.4+ recommended)
- pip (Python package manager)
- A database management tool (e.g., phpMyAdmin)

## Setup Instructions

### 1. Clone the Repository
If applicable, clone the project repository:
```bash
git clone <repository_url>
cd plm_archive_system
```

### 2. Set Up a Virtual Environment
Create and activate a Python virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
Install the required Python libraries:
```bash
pip install -r requirements.txt
```

Install the required npm libraries too:
```
npm install
```

If `requirements.txt` does not exist, manually install the following packages:
```bash
pip install django mysqlclient
```

### 4. Configure the Database
#### Set up MySQL/MariaDB:
- **Create a database**:
    ```sql
    CREATE DATABASE plm_archive CHARACTER SET utf8mb4 COLLATE utf8_general_ci;
    ```
- **Create a user and grant privileges**:
    ```sql
    CREATE USER 'your_mysql_user'@'localhost' IDENTIFIED BY 'your_password';
    GRANT ALL PRIVILEGES ON plm_archive.* TO 'your_mysql_user'@'localhost';
    FLUSH PRIVILEGES;
    ```

#### Update `settings.py`:
Configure the database connection in your Django project:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'plm_archive',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 5. Apply Migrations and Seeder
Prepare the database schema and run seeder:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py seed
```

### 6. Create a Superuser
Set up an admin account for managing the system:
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
Start the Django server locally:
```bash
python manage.py runserver
```

Run the following command to compile TailwindCSS into an output file (always run):
```bash
npx tailwindcss -i ./static/src/input.css -o ./static/src/output.css --watch
```

Access the application at `http://127.0.0.1:8000`.

## Troubleshooting

### `mysqlclient` Errors
If `mysqlclient` causes issues, use `PyMySQL`:
1. Install `PyMySQL`:
    ```bash
    pip install pymysql
    ```
2. Configure Django to use `PyMySQL`: Add this to `plm_archive_system/__init__.py`:
    ```python
    import pymysql
    pymysql.install_as_MySQLdb()
    ```

## Features
- **Role-Based Access:** Guest, Student, and Admin roles with distinct permissions.
- **Document Management:** Upload, view, and manage theses and research papers.
- **Advanced Search:** Filter documents by title, keywords, or metadata.
- **Audit Logs:** Track user actions like uploads and deletions.
- **Access Control:** Enforce permissions based on user roles.

## Project Structure
```
plm_archive_system/
├── archive_app/         # Core app for managing the archive system
├── manage.py            # Django management script
├── plm_archive_system/  # Project settings and configurations
├── static/              # Static assets (images,videos,gifs,etc.)
├── templates/           # Frontend templates for the web interface
├── venv/                # Virtual environment
└── requirements.txt     # Project dependencies
```

## Dependencies
- **Django 4.x**: Core framework.
- **mysqlclient/PyMySQL**: Database adapter for MySQL/MariaDB.
- **MySQL/MariaDB**: Relational database for storing metadata.

## License
This project is licensed under the MIT License.
