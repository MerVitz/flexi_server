from django.core.management.base import BaseCommand
from backend_app.models import CustomUser

class Command(BaseCommand):
    help = "Updateing the users type all istaff to should be admin user type"

    def handle(self, *args, **kwargs):
        admin_users = CustomUser.objects.filter(is_staff=True)
        updated_count = admin_users.update(user_type='admin')
        self.stdout.write(f'Succefully updated {updated_count} user(s).')