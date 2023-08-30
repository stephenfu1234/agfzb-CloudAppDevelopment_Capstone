from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=100, null=False, default="Enter car make name")
    description = models.CharField(max_length=500, null=False, default="Enter car make description")

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):    
    SALOON = 'saloon'
    SPORTS = 'sports'
    HATCHBACK = 'hatchback'
    SUV = 'SUV'
    MODEL_TYPES = [
        (SALOON, 'Saloon'),
        (SPORTS, 'Sports'),
        (HATCHBACK, 'Hatchback'),
        (SUV, 'SUV')
    ]    
    name = models.CharField(max_length=100, null=False, default="Enter car model name")
    dealer_id = models.IntegerField(default=0)
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=MODEL_TYPES, default=HATCHBACK)
    year = models.DateField(null=True)

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Dealer ID: " + str(self.dealer_id) + "," + \
               "Make: " + str(self.make) + "," + \
               "Type: " + self.type + "," + \
               "Year: " + str(self.year)

    

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
