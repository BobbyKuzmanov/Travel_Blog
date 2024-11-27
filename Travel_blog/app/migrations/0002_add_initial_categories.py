from django.db import migrations


def add_initial_categories(apps, schema_editor):
    Category = apps.get_model('app', 'Category')
    initial_categories = [
        {
            'name': 'Beach Vacation',
            'description': 'Relaxing beach destinations and coastal getaways'
        },
        {
            'name': 'Mountain Adventure',
            'description': 'Hiking, climbing, and mountain exploration experiences'
        },
        {
            'name': 'City Break',
            'description': 'Urban adventures and city exploration'
        },
        {
            'name': 'Cultural Experience',
            'description': 'Historical sites, museums, and cultural immersion'
        },
        {
            'name': 'Food & Wine',
            'description': 'Culinary adventures and wine tasting experiences'
        },
        {
            'name': 'Wildlife & Nature',
            'description': 'Safari, national parks, and nature exploration'
        },
        {
            'name': 'Island Paradise',
            'description': 'Tropical island destinations and archipelago adventures'
        },
        {
            'name': 'Road Trip',
            'description': 'Cross-country driving adventures and scenic routes'
        }
    ]
    
    for category_data in initial_categories:
        Category.objects.create(**category_data)

def remove_initial_categories(apps, schema_editor):
    Category = apps.get_model('app', 'Category')
    Category.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_initial_categories, remove_initial_categories),
    ]
