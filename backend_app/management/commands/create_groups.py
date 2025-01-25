from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Create user groups and assign permissions'

    def handle(self, *args, **kwargs):
        # Create Customer group
        customer_group, customer_created = Group.objects.get_or_create(name='customer')
        if customer_created:
            self.stdout.write(self.style.SUCCESS('Customer group created'))
        else:
            self.stdout.write(self.style.WARNING('Customer group already exists'))

        # Create Admin group
        admin_group, admin_created = Group.objects.get_or_create(name='admin')
        if admin_created:
            self.stdout.write(self.style.SUCCESS('Admin group created'))
        else:
            self.stdout.write(self.style.WARNING('Admin group already exists'))

        # Assign permissions to Customer group (if any specific)
        # e.g., customer_group.permissions.add(Permission.objects.get(codename='add_vehicle'))

        # Assign all permissions to Admin group
        permissions = Permission.objects.all()
        admin_group.permissions.set(permissions)

        self.stdout.write(self.style.SUCCESS('Groups and permissions have been set up'))
