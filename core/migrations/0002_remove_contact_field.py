from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        # First make the field nullable
        migrations.AlterField(
            model_name='product',
            name='contact',
            field=models.CharField(max_length=15, null=True, blank=True),
        ),
        # Then remove the field
        migrations.RemoveField(
            model_name='product',
            name='contact',
        ),
    ] 