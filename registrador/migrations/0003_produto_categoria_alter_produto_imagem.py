# Generated by Django 5.2.3 on 2025-06-23 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrador', '0002_alter_produto_imagem'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='categoria',
            field=models.CharField(choices=[('combo', 'Combo'), ('pizza', 'Pizza'), ('lanche', 'Lanche'), ('bebida', 'Bebida')], default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='produto',
            name='imagem',
            field=models.ImageField(blank=True, null=True, upload_to='produtos/'),
        ),
    ]
