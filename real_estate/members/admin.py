from django.contrib import admin
from .models import City, Buyer, Seller, Agent, Property, Landlord, Renter, Favorite, Review,PropertyImage

# Register your models here
admin.site.register(City)
admin.site.register(Buyer)
admin.site.register(Seller)
admin.site.register(Agent)
admin.site.register(Property)
admin.site.register(Landlord)
admin.site.register(Renter)
admin.site.register(Favorite)
admin.site.register(Review)
admin.site.register(PropertyImage)