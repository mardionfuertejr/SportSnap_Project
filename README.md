# SportSnap 📸🏀⚽

> **"Capture Every Winning Moment."**

SportSnap is a complete production-ready Django web application built as a sports-themed Photo Album Management System. It allows users to create albums, upload sports photos, organize collections, and manage access roles.

## 🌟 Features

- **Authentication System:** Registration, login, profiles, and role management.
- **Album Management:** Create, edit, and delete photo albums with public/private visibility.
- **Photo Gallery:** Upload multiple photos directly to Cloudinary with masonry layout and lightbox view.
- **Admin Dashboard:** Track user activity and view platform statistics.
- **Modern UI:** Built with Bootstrap 5, featuring a dark mode sports theme, glassmorphism UI elements, and responsive design.

## 🛠️ Technologies Used

- **Backend:** Django 5.1, Python 3.10+
- **Database:** PostgreSQL (Production) / SQLite (Local)
- **Storage:** Cloudinary (Media files) & WhiteNoise (Static files)
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5, Masonry Layout

## 📂 Project Structure

```
sportsnap/
├── accounts/         # User auth, profiles, and admin user management
├── albums/           # Album CRUD, lists, and filtering
├── photos/           # Multi-image upload and photo management
├── dashboard/        # Activity logs and site statistics
├── templates/        # HTML templates using Bootstrap 5
├── static/           # Custom CSS and JavaScript
└── sportsnap/        # Core project settings
```

## 🚀 Local Development Setup

1. **Clone the repository and enter the directory.**
2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables:**
   Copy `.env.example` to `.env` and fill in your Cloudinary credentials.
5. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```
7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

## ☁️ Deployment (Render)

This project is configured for deployment on Render.

1. Create a new **Web Service** on Render and connect your repository.
2. Set the **Build Command** to: `./build.sh`
3. Set the **Start Command** to: `gunicorn sportsnap.wsgi --log-file -`
4. Add the following **Environment Variables** in the Render dashboard:
   - `PYTHON_VERSION`: `3.10.13`
   - `SECRET_KEY`: Your secure secret key
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `.onrender.com`
   - `DATABASE_URL`: Add a Render PostgreSQL database and paste the internal URL here.
   - `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`: Your Cloudinary credentials.

## 👨‍💻 Developer Notes

- The project uses `dj-database-url` to seamlessly switch between SQLite (local) and PostgreSQL (production).
- Image uploads go directly to Cloudinary via `django-cloudinary-storage`, keeping the server stateless.
- WhiteNoise handles static files efficiently without a separate CDN.
