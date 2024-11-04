from django.db import models
from django.contrib.auth.models import User
import os
from django.conf import settings


# 1. City Model
class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}, {self.state}, {self.country}"

# 2. Buyer Model
class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username

# 3. Seller Model
class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username

# 4. Agent Model
class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username

# 5. Property Model
class Property(models.Model):
    property_id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    address = models.TextField()
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    property_type = models.CharField(max_length=50, choices=[
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('land', 'Land')
    ])
    is_rented = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.property_type} at {self.address}"
    
    def get_agent(self):
        try:
            return Agent.objects.get(user=self.seller.user)
        except Agent.DoesNotExist:
            return None



# 6. Landlord Model
class Landlord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username

# 7. Renter Model
class Renter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username

# 8. Favorite Model
class Favorite(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('buyer', 'property')

    def __str__(self):
        return f"{self.buyer} favorited {self.property}"

# 9. Review Model
class Review(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.buyer} for {self.property}"


def property_image_upload_to(instance, filename):
    return os.path.join('property_image', str(instance.property.property_id), filename)


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=property_image_upload_to)
    description = models.TextField(blank=True, null=True)