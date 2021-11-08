from chats.models import Chat
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0001_initial'),
    ]

    def create_common_chat(apps, schema_editor):

        common_chat = Chat.objects.create(
            name="Common",
            short_link = "commonchat"
        )
        common_chat.save()

    operations = [
        migrations.RunPython(create_common_chat),
    ]