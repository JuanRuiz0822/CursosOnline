# Generated migration for Payment model restructure

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payments', '0001_initial'),
    ]

    operations = [
        # Agregar nuevos campos
        migrations.AddField(
            model_name='payment',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='payment',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='courses.course'),
        ),
        migrations.AddField(
            model_name='payment',
            name='currency',
            field=models.CharField(default='COP', max_length=3),
        ),
        migrations.AddField(
            model_name='payment',
            name='provider',
            field=models.CharField(choices=[('wompi', 'Wompi'), ('stripe', 'Stripe')], default='wompi', max_length=20),
        ),
        migrations.AddField(
            model_name='payment',
            name='method',
            field=models.CharField(choices=[('card', 'Tarjeta Crédito/Débito'), ('nequi', 'Nequi')], default='card', max_length=20),
        ),
        migrations.AddField(
            model_name='payment',
            name='reference',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=255),
        ),
        # Alterar campo status
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('pending', 'Pendiente'), ('approved', 'Aprobado'), ('rejected', 'Rechazado'), ('refunded', 'Reembolsado')], default='pending', max_length=20),
        ),
        # Hacer enrollment nullable
        migrations.AlterField(
            model_name='payment',
            name='enrollment',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='enrollments.enrollment'),
        ),
        # Agregar unique_together
        migrations.AlterUniqueTogether(
            name='payment',
            unique_together={('student', 'course')},
        ),
        # Cambiar ordenamiento
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ['-created_at']},
        ),
    ]
