from django.db import migrations

def populate_locations(apps, schema_editor):
    Province = apps.get_model('core', 'Province')
    District = apps.get_model('core', 'District')
    Sector = apps.get_model('core', 'Sector')
    Cell = apps.get_model('core', 'Cell')
    Village = apps.get_model('core', 'Village')

    # Create provinces
    provinces = [
        {'name': 'Kigali City', 'code': '01'},
        {'name': 'Southern Province', 'code': '02'},
        {'name': 'Western Province', 'code': '03'},
        {'name': 'Northern Province', 'code': '04'},
        {'name': 'Eastern Province', 'code': '05'},
    ]

    for province_data in provinces:
        Province.objects.get_or_create(
            name=province_data['name'],
            code=province_data['code']
        )

    # Create districts for Kigali City
    kigali = Province.objects.get(code='01')
    kigali_districts = [
        {'name': 'Gasabo', 'code': '0101'},
        {'name': 'Kicukiro', 'code': '0102'},
        {'name': 'Nyarugenge', 'code': '0103'},
    ]

    for district_data in kigali_districts:
        District.objects.get_or_create(
            name=district_data['name'],
            code=district_data['code'],
            province=kigali
        )

    # Create districts for Southern Province
    southern = Province.objects.get(code='02')
    southern_districts = [
        {'name': 'Gisagara', 'code': '0201'},
        {'name': 'Huye', 'code': '0202'},
        {'name': 'Kamonyi', 'code': '0203'},
        {'name': 'Muhanga', 'code': '0204'},
        {'name': 'Nyamagabe', 'code': '0205'},
        {'name': 'Nyanza', 'code': '0206'},
        {'name': 'Nyaruguru', 'code': '0207'},
        {'name': 'Ruhango', 'code': '0208'},
    ]

    for district_data in southern_districts:
        District.objects.get_or_create(
            name=district_data['name'],
            code=district_data['code'],
            province=southern
        )

    # Create districts for Western Province
    western = Province.objects.get(code='03')
    western_districts = [
        {'name': 'Karongi', 'code': '0301'},
        {'name': 'Ngororero', 'code': '0302'},
        {'name': 'Nyabihu', 'code': '0303'},
        {'name': 'Nyamasheke', 'code': '0304'},
        {'name': 'Rubavu', 'code': '0305'},
        {'name': 'Rusizi', 'code': '0306'},
        {'name': 'Rutsiro', 'code': '0307'},
    ]

    for district_data in western_districts:
        District.objects.get_or_create(
            name=district_data['name'],
            code=district_data['code'],
            province=western
        )

    # Create districts for Northern Province
    northern = Province.objects.get(code='04')
    northern_districts = [
        {'name': 'Burera', 'code': '0401'},
        {'name': 'Gakenke', 'code': '0402'},
        {'name': 'Gicumbi', 'code': '0403'},
        {'name': 'Musanze', 'code': '0404'},
        {'name': 'Rulindo', 'code': '0405'},
    ]

    for district_data in northern_districts:
        District.objects.get_or_create(
            name=district_data['name'],
            code=district_data['code'],
            province=northern
        )

    # Create districts for Eastern Province
    eastern = Province.objects.get(code='05')
    eastern_districts = [
        {'name': 'Bugesera', 'code': '0501'},
        {'name': 'Gatsibo', 'code': '0502'},
        {'name': 'Kayonza', 'code': '0503'},
        {'name': 'Kirehe', 'code': '0504'},
        {'name': 'Ngoma', 'code': '0505'},
        {'name': 'Nyagatare', 'code': '0506'},
        {'name': 'Rwamagana', 'code': '0507'},
    ]

    for district_data in eastern_districts:
        District.objects.get_or_create(
            name=district_data['name'],
            code=district_data['code'],
            province=eastern
        )

def reverse_populate_locations(apps, schema_editor):
    Province = apps.get_model('core', 'Province')
    Province.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_locations, reverse_populate_locations),
    ] 