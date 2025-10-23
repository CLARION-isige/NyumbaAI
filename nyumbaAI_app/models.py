from django.db import models

class SearchQuery(models.Model):
    query = models.TextField()
    location = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    results_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.query} - {self.location}"

class HouseListing(models.Model):
    search = models.ForeignKey(SearchQuery, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(
        default='Address not available',  # Add default
        blank=True,  # Allow blank
        null=True  # Allow null in DB
    )
    address = models.TextField()
    link = models.URLField(
        max_length=500, 
        default='#', 
        blank=True,
        null=True  
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.title