# Generated by Django 4.2.7 on 2023-11-29 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ProductCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=120, verbose_name="name")),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=120, verbose_name="name")),
                (
                    "description",
                    models.CharField(max_length=250, verbose_name="description"),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, max_digits=7, verbose_name="price"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True, upload_to="products/%Y/%m/%d/", verbose_name="image"
                    ),
                ),
                (
                    "thumbnail",
                    models.ImageField(
                        blank=True,
                        upload_to="products/thumb/%Y/%m/%d/",
                        verbose_name="thumbnail",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="products",
                        to="products.productcategory",
                    ),
                ),
            ],
        ),
    ]
