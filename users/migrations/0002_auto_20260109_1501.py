from django.db import migrations

def add_roles(apps, schema_editor):
    Role = apps.get_model('users', 'Role')
    Role.objects.get_or_create(name='owner')
    Role.objects.get_or_create(name='seeker')

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_roles),
    ]