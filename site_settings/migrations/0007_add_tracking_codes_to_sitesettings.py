from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("site_settings", "0006_remove_pagemeta_meta_description_en_en_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="head_tracking_code",
            field=models.TextField(
                blank=True,
                null=True,
                help_text=(
                    "Sayfa <head> içerisine eklenecek takip kodları (ör: Google tag gtag.js, "
                    "Meta Pixel script vb.). Tam script/snippet olarak girin."
                ),
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="body_tracking_code",
            field=models.TextField(
                blank=True,
                null=True,
                help_text=(
                    "Sayfa <body> içerisine eklenecek takip kodları (ör: noscript piksel kodu vb.). "
                    "Tam script/snippet olarak girin."
                ),
            ),
        ),
    ]


