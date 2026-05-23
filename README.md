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
├── accounts/         # User auth, registration, and profile templates
├── gallery/          # Album and Photo models, CBVs, and main UI templates
├── static/           # Custom CSS, JavaScript, and images
└── sportsnap/        # Core project settings and configurations
```

## 🚀 Local Development Setup

1. **Clone the repository and enter the directory.**
2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   source venv/bin/activate 
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables:**
   Create a `.env` file in the root directory and fill in the required variables (see the Deployment section below for the full list).
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
3. Set the **Start Command** to: `gunicorn sportsnap.wsgi:application`
4. Add the following **Environment Variables** in the Render dashboard:
   - `PYTHON_VERSION`: `3.14.3`
   - `SECRET_KEY`: `django-insecure-sportsnap-prod-2026-!@#$%^`
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `.onrender.com`
   - `DATABASE_URL`: `postgresql://sportsnap_db_user:J2LzhWR9slM5lIelTTbo1oUTjj1ONdEV@dpg-d88qb56q1p3s73f7cjag-a/sportsnap_db`
   - `CLOUDINARY_CLOUD_NAME`: `dfpajntid`
   - `CLOUDINARY_API_KEY`: `125814895956173`
   - `CLOUDINARY_API_SECRET`: `[ILAGAY DITO YUNG ROOT API SECRET MULA SA CLOUDINARY]`

## 👨‍💻 Developer Notes

- The project uses `dj-database-url` to seamlessly switch between SQLite (local) and PostgreSQL (production).
- Image uploads go directly to Cloudinary via `django-cloudinary-storage`, keeping the server stateless.
- WhiteNoise handles static files efficiently without a separate CDN.
