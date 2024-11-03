from django.db import models
from django.contrib.auth.models import User

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
    rating = models.PositiveSmallIntegerField()  # 1 to 5 scale
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.buyer} for {self.property}"

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='property_images/%Y/%m/%d/')  # Default path
    description = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.property:
            self.image.name = f'property_{self.property.id}/{self.image.name}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.property} - {self.description or 'No Description'}"