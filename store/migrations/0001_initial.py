from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
            options={'ordering': ['name'], 'verbose_name_plural': 'Categories'},
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=160)),
                ('phone', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=255)),
                ('notes', models.TextField(blank=True)),
                ('payment_method', models.CharField(choices=[('cash', 'Naqd'), ('card', 'Karta'), ('click', 'Click'), ('payme', 'Payme')], default='cash', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('total_price', models.PositiveIntegerField(default=0)),
                ('is_paid', models.BooleanField(default=False)),
                ('payment_status', models.CharField(default='pending', max_length=50)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=30)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=180)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('short_description', models.CharField(max_length=220)),
                ('description', models.TextField(blank=True)),
                ('price', models.PositiveIntegerField()),
                ('old_price', models.PositiveIntegerField(default=0)),
                ('stock', models.PositiveIntegerField(default=0)),
                ('image_emoji', models.CharField(default='🛒', max_length=10)),
                ('image_url', models.URLField(blank=True)),
                ('product_type', models.CharField(choices=[('fruit', 'Meva'), ('vegetable', 'Sabzavot'), ('dairy', 'Sut'), ('drink', 'Ichimlik'), ('bakery', 'Non'), ('other', 'Boshqa')], default='other', max_length=20)),
                ('is_featured', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.category')),
            ],
            options={'ordering': ['-is_featured', 'name']},
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=180)),
                ('price', models.PositiveIntegerField()),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.order')),
            ],
        ),
    ]
