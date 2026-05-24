from django.db import migrations
from django.contrib.auth import get_user_model

def create_admin_superuser(apps, schema_editor):
    User = get_user_model()
    username = 'admin'
    email = 'admin@example.com'
    password = 'Admin123!'
    
    # Check if the user already exists
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
    else:
        User.objects.create_superuser(username=username, email=email, password=password)

class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(create_admin_superuser),
    ]
