from django.db import models
class Expense(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_by = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"

    
class Member(models.Model):
     name = models.CharField(max_length=100, unique=True)
     contact = models.CharField(max_length=200, blank=True)
def __str__(self):
 return self.name
