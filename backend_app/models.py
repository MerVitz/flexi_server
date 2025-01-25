from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.db import models

##These are my models, they are 8 in number; Customuser, Equipment,
##Booking, Payment, Notification, Maintenance, Comment, Review,
## Any more that will bde added, ; MUST NOTE THE REASONS IN THE DOCUMENATION.

from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.db import models



# 1. CustomUser and CustomUserManager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        # If a superuser (admin) is creating this user, set them as Admin
        if created_by and created_by.is_superuser and created_by.is_staff and created_by.is_active:
            user.user_type = CustomUser.ADMIN  # Set user_type to 'admin'
            user.is_staff = True  # Admins have is_staff=True
            admin_group, created = Group.objects.get_or_create(name='Admin')
            user.save(using=self._db)
            user.groups.add(admin_group)  # Add to the Admin group
        else:
            # Default user type and group for regular users
            user.user_type = CustomUser.CUSTOMER  # Default user_type is 'customer'
            user.is_staff = False  # Customers don't have staff permissions
            customer_group, created = Group.objects.get_or_create(name='Customer')
            user.save(using=self._db)
            user.groups.add(customer_group)  # Add to the Customer group
        
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and returns a superuser, adding them to the Admin group and setting their user_type to 'admin'.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        user = self.create_user(email, password, **extra_fields)

        # Ensure the superuser is in the Admin group and has the correct user_type
        user.user_type = CustomUser.ADMIN
        admin_group, created = Group.objects.get_or_create(name='Admin')
        user.groups.add(admin_group)
        user.save(using=self._db)

        return user

class CustomUser(AbstractUser):
    CUSTOMER = 'customer'
    ADMIN = 'admin'
    USER_TYPE_CHOICES = [
        (CUSTOMER, 'customer'),
        (ADMIN, 'admin')
    ]
    
    username = None
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default=CUSTOMER)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

# 2. Equipment model
class Equipment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    description = models.TextField()
    availability = models.BooleanField(default=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    added_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='equipment_images/')

    def __str__(self):
        return self.name

# 3. Booking model
class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.equipment.name}"

# 4. Payment model
class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100)
    payment_date = models.DateTimeField()

    def __str__(self):
        return f'Payment of {self.amount} for booking {self.booking.id}'

# 5. Notification model
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    requires_confirmation = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.email}"

# 6. Maintenance model
class Maintenance(models.Model):
    id = models.AutoField(primary_key=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    issue_description = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Maintenance for {self.equipment.name}'

# 7. Comment model
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.email} on {self.equipment.name}'

# 8. Review model
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.email} on {self.equipment.name} with rating {self.rating}'
