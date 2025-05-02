from django.db import migrations

def populate_locations(apps, schema_editor):
    Province = apps.get_model('core', 'Province')
    District = apps.get_model('core', 'District')
    Sector = apps.get_model('core', 'Sector')
    Cell = apps.get_model('core', 'Cell')
    Village = apps.get_model('core', 'Village')

    # Create provinces
    kigali = Province.objects.create(name='Kigali City', code='KG')
    southern = Province.objects.create(name='Southern Province', code='SP')
    western = Province.objects.create(name='Western Province', code='WP')
    northern = Province.objects.create(name='Northern Province', code='NP')
    eastern = Province.objects.create(name='Eastern Province', code='EP')

    # Sample districts for Kigali (for demonstration)
    gasabo = District.objects.create(name='Gasabo', code='KG01', province=kigali)
    kicukiro = District.objects.create(name='Kicukiro', code='KG02', province=kigali)
    nyarugenge = District.objects.create(name='Nyarugenge', code='KG03', province=kigali)

    # Sample sectors for Gasabo (for demonstration)
    sectors = [
        ('Bumbogo', 'KG01S1', gasabo),
        ('Gikomero', 'KG01S2', gasabo),
        ('Jabana', 'KG01S3', gasabo),
    ]
    
    for name, code, district in sectors:
        Sector.objects.create(name=name, code=code, district=district)

def reverse_populate(apps, schema_editor):
    Province = apps.get_model('core', 'Province')
    Province.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0007_create_location_models'),
    ]

    operations = [
        migrations.RunPython(populate_locations, reverse_populate),
    ] 