from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),  # Replace with your last migration
    ]

    operations = [
        migrations.AddField(
            model_name='steganofile',
            name='extracted_message',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='steganofile',
            name='extraction_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='steganofile',
            name='extraction_status',
            field=models.CharField(
                choices=[('pending', 'Pending'), ('processing', 'Processing'), 
                        ('completed', 'Completed'), ('failed', 'Failed')],
                default='pending',
                max_length=10
            ),
        ),
    ]
