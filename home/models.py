from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    is_manager = models.BooleanField(default=False)
    name = models.CharField(null=True,max_length=255)
    phone = models.CharField(null=True,blank=True,max_length=20)
    
    # Add any other fields as necessary
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email', 'phone']
    
    def __str__(self):
        return self.username
    
class Food(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


class Accommodation(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

class Package(models.Model):
   

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    source = models.CharField(max_length=100)
    start_date = models.DateField()
    duration = models.PositiveIntegerField()
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    foods = models.ManyToManyField(Food)
    accommodations = models.ManyToManyField(Accommodation)

    def __str__(self):
        return self.name
    
    def get_total_food_cost(self, duration):
        meals_per_day = 3
        total_meals = meals_per_day * duration
        total_food_cost = sum([food.price for food in self.foods.all()]) * total_meals
        return total_food_cost

    def get_total_accommodation_cost(self, duration):
        total_accommodation_cost = sum([accommodation.price for accommodation in self.accommodations.all()]) * duration
        return total_accommodation_cost

    def get_total_cost(self, duration):
        total_food_cost = self.get_total_food_cost(duration)
        total_accommodation_cost = self.get_total_accommodation_cost(duration)
        total_cost = self.price + total_food_cost + total_accommodation_cost
        return total_cost

    
class Order(models.Model):
    order_id = models.CharField("order_id", max_length=10, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    food_price = models.DecimalField(default=0,max_digits=10, decimal_places=2)
    accommodation_price = models.DecimalField(default=0,max_digits=10, decimal_places=2)
    total_price = models.DecimalField(default=0,max_digits=10, decimal_places=2)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    created_at = models.DateField()

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, blank=True, null=True)
    food_id = models.IntegerField(null=True, blank=True,)
    accommodation_id = models.IntegerField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Cart"
    
    def clear_cart(self):
        self.items.clear()

class Places(models.Model):
    package = models.ManyToManyField(Package)
    place = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "Places"
    def __str__(self):
        return f"{self.place}"