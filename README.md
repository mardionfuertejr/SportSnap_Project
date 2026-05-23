# SportSnap 📸🏀⚽

> **"Capture Every Winning Moment."**

SportSnap is a complete, production-ready Django web application built as a sports-themed Photo Album Management System. It allows authenticated users to create albums, upload sports photos, organize their collections, and manage access roles securely.

🌐 **Live App:** https://sportsnap-project.onrender.com

---

## 🌟 Features

- **Authentication System:** Registration, login, and role management via Django's native auth system.
- **Album Management:** Create, edit, and delete photo albums.
- **Photo Gallery:** Upload photos directly to Cloudinary with a modern masonry layout.
- **Role-Based Access Control:** Only album/photo owners and admins can edit or delete content.
- **Modern UI:** Glassmorphism design, Bootstrap 5, Google Fonts, and responsive layout.

---

## ✅ Architectural Compliance

### Class-Based Views (CBVs)
All CRUD operations use Django's built-in CBVs:

| View | Type | Purpose |
|---|---|---|
| `AlbumListView` | ListView | Browse all albums |
| `AlbumDetailView` | DetailView | View album and its photos |
| `AlbumCreateView` | CreateView | Create a new album |
| `AlbumUpdateView` | UpdateView | Edit an existing album |
| `AlbumDeleteView` | DeleteView | Delete an album |
| `PhotoCreateView` | CreateView | Upload a new photo |
| `PhotoUpdateView` | UpdateView | Edit photo details |
| `PhotoDeleteView` | DeleteView | Delete a photo |

### Role-Based Access Control (RBAC)
- `LoginRequiredMixin` — All create/edit/delete operations require login.
- `IsOwnerOrAdminMixin` (via `UserPassesTestMixin`) — Only the **owner** or a **superuser/admin** can edit or delete content.

### Cloud Storage
- All images are stored via `CloudinaryField` in `models.py`.
- Production storage backend is set to `cloudinary_storage.storage.MediaCloudinaryStorage`.
- No media files are stored locally on the server.

### Security
- All secrets (`SECRET_KEY`, `DATABASE_URL`, `CLOUDINARY_*`) are stored as **environment variables** — never hardcoded.
- `.env` is excluded from the repository via `.gitignore`.

---

## 🛠️ Technologies Used

- **Backend:** Django 6.0.5, Python 3.14
- **Database:** PostgreSQL (Production via Render) / SQLite (Local)
- **Media Storage:** Cloudinary (`django-cloudinary-storage`)
- **Static Files:** WhiteNoise
- **Frontend:** HTML5, CSS3 (Glassmorphism), Bootstrap 5, Google Fonts
- **Server:** Gunicorn on Render

---

## 📂 Project Structure

```
sportsnap/
├── accounts/         # User auth, registration, and profile templates
├── gallery/          # Album and Photo models, CBVs, and main UI templates
├── static/           # Custom CSS, JavaScript, and images
└── sportsnap/        # Core project settings and configurations
```

---

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

---

## ☁️ Deployment (Render)

This project is configured for deployment on Render.

1. Create a new **Web Service** on Render and connect your GitHub repository.
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
   - `CLOUDINARY_API_SECRET`: `[Your Cloudinary Root API Secret]`

---

## 👨‍💻 Developer Notes

- The project uses `dj-database-url` to seamlessly switch between SQLite (local) and PostgreSQL (production).
- Image uploads go directly to Cloudinary via `django-cloudinary-storage`, keeping the server stateless.
- WhiteNoise handles static files efficiently without a separate CDN.
- `build.sh` automatically runs `collectstatic` and `migrate` on every Render deploy.
