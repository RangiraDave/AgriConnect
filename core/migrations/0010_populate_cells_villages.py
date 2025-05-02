from django.db import migrations

def populate_cells_villages(apps, schema_editor):
    Province = apps.get_model('core', 'Province')
    District = apps.get_model('core', 'District')
    Sector = apps.get_model('core', 'Sector')
    Cell = apps.get_model('core', 'Cell')
    Village = apps.get_model('core', 'Village')

    # Get Gasabo district and its sectors
    gasabo = District.objects.get(name='Gasabo')
    bumbogo = Sector.objects.get(name='Bumbogo', district=gasabo)
    gikomero = Sector.objects.get(name='Gikomero', district=gasabo)
    jabana = Sector.objects.get(name='Jabana', district=gasabo)

    # Create cells for Bumbogo sector
    bumbogo_cells = [
        ('Bumbogo', 'KG01S1C1', bumbogo),
        ('Gahanga', 'KG01S1C2', bumbogo),
        ('Kinyana', 'KG01S1C3', bumbogo),
    ]
    
    for name, code, sector in bumbogo_cells:
        cell = Cell.objects.create(name=name, code=code, sector=sector)
        # Create villages for each cell
        for i in range(1, 4):  # Create 3 villages per cell
            Village.objects.create(
                name=f'{name} Village {i}',
                code=f'{code}V{i}',
                cell=cell
            )

    # Create cells for Gikomero sector
    gikomero_cells = [
        ('Gikomero', 'KG01S2C1', gikomero),
        ('Kabeza', 'KG01S2C2', gikomero),
        ('Kinyinya', 'KG01S2C3', gikomero),
    ]
    
    for name, code, sector in gikomero_cells:
        cell = Cell.objects.create(name=name, code=code, sector=sector)
        # Create villages for each cell
        for i in range(1, 4):  # Create 3 villages per cell
            Village.objects.create(
                name=f'{name} Village {i}',
                code=f'{code}V{i}',
                cell=cell
            )

    # Create cells for Jabana sector
    jabana_cells = [
        ('Jabana', 'KG01S3C1', jabana),
        ('Kacyiru', 'KG01S3C2', jabana),
        ('Kimironko', 'KG01S3C3', jabana),
    ]
    
    for name, code, sector in jabana_cells:
        cell = Cell.objects.create(name=name, code=code, sector=sector)
        # Create villages for each cell
        for i in range(1, 4):  # Create 3 villages per cell
            Village.objects.create(
                name=f'{name} Village {i}',
                code=f'{code}V{i}',
                cell=cell
            )

def reverse_populate(apps, schema_editor):
    Cell = apps.get_model('core', 'Cell')
    Village = apps.get_model('core', 'Village')
    Village.objects.all().delete()
    Cell.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0009_add_location_models'),
    ]

    operations = [
        migrations.RunPython(populate_cells_villages, reverse_populate),
    ] 