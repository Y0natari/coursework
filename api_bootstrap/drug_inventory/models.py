from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

class Drug(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='drugs', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

class Transaction(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    transaction_type = models.CharField(max_length=10, choices=[('buy', 'Buy'), ('sell', 'Sell')])
    transaction_date = models.DateTimeField(auto_now_add=True)
