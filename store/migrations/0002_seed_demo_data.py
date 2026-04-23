from django.db import migrations
from django.utils.text import slugify


def seed_data(apps, schema_editor):
    Category = apps.get_model('store', 'Category')
    Product = apps.get_model('store', 'Product')

    categories = {}
    category_names = [
        'Mevalar',
        'Sabzavotlar',
        'Sut mahsulotlari',
        'Ichimliklar',
        'Non va pishiriqlar',
    ]

    for name in category_names:
        obj, _ = Category.objects.get_or_create(
            name=name,
            defaults={'slug': slugify(name)}
        )
        categories[name] = obj

    products = [
        ('Qizil olma', 'Shirador va tabiiy olma', 18000, 22000, 40, '🍎', 'fruit', True, 'Mevalar', 'https://images.unsplash.com/photo-1567306226416-28f0efdc88ce?auto=format&fit=crop&w=900&q=80'),
        ('Banan', 'Sifatli import banan', 24000, 28000, 30, '🍌', 'fruit', False, 'Mevalar', 'https://images.unsplash.com/photo-1574226516831-e1dff420e37f?auto=format&fit=crop&w=900&q=80'),
        ('Uzum', 'Shirin va toza uzum', 26000, 30000, 25, '🍇', 'fruit', False, 'Mevalar', 'https://images.unsplash.com/photo-1537640538966-79f369143f8f?auto=format&fit=crop&w=900&q=80'),
        ('Pomidor', 'Yangi va pishgan pomidor', 16000, 19000, 55, '🍅', 'vegetable', True, 'Sabzavotlar', 'https://images.unsplash.com/photo-1546094096-0df4bcaaa337?auto=format&fit=crop&w=900&q=80'),
        ('Bodring', 'Toza va saralangan bodring', 13000, 15000, 50, '🥒', 'vegetable', False, 'Sabzavotlar', 'https://images.unsplash.com/photo-1604977042946-1eecc30f269e?auto=format&fit=crop&w=900&q=80'),
        ('Kartoshka', 'Toza va yangi kartoshka', 9000, 11000, 80, '🥔', 'vegetable', False, 'Sabzavotlar', 'https://images.unsplash.com/photo-1518977676601-b53f82aba655?auto=format&fit=crop&w=900&q=80'),
        ('Sut 1L', 'Kunlik yangi sut mahsuloti', 14000, 17000, 35, '🥛', 'dairy', True, 'Sut mahsulotlari', 'https://images.unsplash.com/photo-1563636619-e9143da7973b?auto=format&fit=crop&w=900&q=80'),
        ('Qatiq', 'Tabiiy va foydali qatiq', 12000, 14000, 28, '🥣', 'dairy', False, 'Sut mahsulotlari', 'https://images.unsplash.com/photo-1488477181946-6428a0291777?auto=format&fit=crop&w=900&q=80'),
        ('Mineral suv', 'Sovutilgan tetiklantiruvchi suv', 6000, 8000, 90, '💧', 'drink', False, 'Ichimliklar', 'https://images.unsplash.com/photo-1564419320408-38e24e038739?auto=format&fit=crop&w=900&q=80'),
        ('Apelsin sharbati', 'Vitaminlarga boy sharbat', 19000, 23000, 26, '🧃', 'drink', True, 'Ichimliklar', 'https://images.unsplash.com/photo-1600271886742-f049cd451bba?auto=format&fit=crop&w=900&q=80'),
        ('Issiq non', 'Yangi yopilgan issiq non', 5000, 7000, 70, '🍞', 'bakery', False, 'Non va pishiriqlar', 'https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=900&q=80'),
        ('Kruassan', 'Mazali nonushta pishirig‘i', 11000, 13000, 22, '🥐', 'bakery', False, 'Non va pishiriqlar', 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=900&q=80'),
    ]

    for name, short_desc, price, old_price, stock, emoji, ptype, featured, cat_name, image_url in products:
        Product.objects.get_or_create(
            name=name,
            defaults={
                'category': categories[cat_name],
                'slug': slugify(name),
                'short_description': short_desc,
                'description': short_desc,
                'price': price,
                'old_price': old_price,
                'stock': stock,
                'image_emoji': emoji,
                'image_url': image_url,
                'product_type': ptype,
                'is_featured': featured,
                'is_active': True,
            }
        )


def unseed_data(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    Category = apps.get_model('store', 'Category')
    Product.objects.all().delete()
    Category.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [('store', '0001_initial')]

    operations = [
        migrations.RunPython(seed_data, unseed_data),
    ]