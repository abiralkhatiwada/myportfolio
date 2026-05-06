from django.db import migrations

def update_site_name(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    # Update the default site (ID=1)
    Site.objects.update_or_create(
        id=1,
        defaults={
            'domain': 'abiralkhatiwada.com.np',
            'name': 'Abiral Khatiwada'
        }
    )

class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_alter_skill_options_skill_category'),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(update_site_name),
    ]
