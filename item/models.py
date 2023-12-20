from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.
class Item(models.Model):
    type1_cuisins=[('Chinese','Chinese'),
    ('NorthIndian','North Indian'),
    ('SouthIndian','South Indian'),
    ]
    type2_vegNon=[
        ('veg','VEG'),
        ('nonveg','NONVEG'),
    ]
    type3_course=[
        ('BreakFast','BreakFast'),
        ('Starters','Starters'),
        ('MainCourse','Main Course'),
        ('Dessert','Dessert') ,
    ]
    '''type4_rotis=[
        ('Roti','Roti'),
        ('dosa','Dosa'),
        ('curry','Curry'),
        ('Rice','Rice'),
        ('Rolls','Rolls'),
        ('Soup','Soup'),
    ] '''
    item_code=models.CharField(primary_key=True,default='FD00',max_length=10,null=False)
    item_name=models.CharField(max_length=30)
    type1=models.CharField(choices=type1_cuisins,max_length=20,default='na')
    type2=models.CharField(choices=type2_vegNon,max_length=20,default='na')
    type3=models.CharField(choices=type3_course,max_length=20,default='na')
    # type4=models.CharField(choices=type4_rotis,max_length=20,default='na')
    price=models.IntegerField()
    info=models.TextField(max_length=300)
    image_field=models.ImageField(upload_to='images/')

class Beverages(models.Model):
    item_code1=models.CharField(primary_key=True,default='DR00',max_length=10,null=False)
    item_name=models.CharField(max_length=30)
    type1_beverages=[('Alcoholic','Alcoholic'),
    ('NonALcoholic','Non-Alcoholic'),]
    type2_beverages=[('Beer','Beer'),
    ('Wine','Wine'),
    ('Vodka','Vodka'),
    ('Rum','Rum'),
    ('Whisky','Whisky'),
    ('Tequila','Tequila'),
    ('Tea','Tea'),
    ('Coffee','Coffee'),
    ('FruitJuice','FruitJuice'),
    ('SoftDrinks','SoftDrinks'),
    ('MilkShake','MilkShake')]
    type1=models.CharField(choices=type1_beverages,max_length=20,default='na')
    type2=models.CharField(choices=type2_beverages,max_length=20,default='na')
    info=models.TextField(max_length=300)
    price=models.IntegerField()
    image_field=models.ImageField(upload_to='images/')
class order(models.Model):
    order_id=models.CharField(max_length=12,primary_key=True)
    username=models.ForeignKey(User,on_delete=models.CASCADE)
    
    is_ordered=models.BooleanField(default=False)
class order_details(models.Model):
    state_choice=[('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Goa','Goa'),
    ('Maharashtra','Maharashtra')]
    #order_idf=models.ForeignKey(order_food,to_field='order_idf', on_delete=models.PROTECT,null=True)
    #order_idb=models.ForeignKey(order_beverage,to_field='order_idb', on_delete=models.PROTECT,null=True)
    order_id=models.ForeignKey(order,to_field='order_id',max_length=12 ,primary_key=True,on_delete=models.CASCADE)
    username=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    address=models.TextField(max_length=300)
    phone_no=models.CharField(max_length=12)
    state=models.CharField(choices=state_choice,max_length=20)
    city=models.CharField(max_length=20)
    postal_code=models.IntegerField()
    total_price=models.FloatField() 
    order_date=models.DateTimeField()
    delivery_date=models.DateTimeField()
    payment_id=models.CharField(max_length=13,unique=True,null=False)
    is_purchase=models.BooleanField(default=False)
    def clean(self):
        if self.order_date>self.delivery_date:
            print("raise validation error")
            raise ValidationError('deliver_date must be greater than order_date')
        return super().clean()

class food_cart(models.Model):
    order_idf=models.ForeignKey(order,to_field='order_id',max_length=12,on_delete=models.CASCADE,null=False)
    item_code=models.ForeignKey(Item,on_delete=models.CASCADE,null=False)
    #added new
    #username=models.ForeignKey(User,on_delete=models.CASCADE)
    fquantity=models.IntegerField()
   
    class Meta:
        unique_together = (("order_idf", "item_code"))
class beverage_cart(models.Model):
    order_idb=models.ForeignKey(order,to_field='order_id',max_length=12,on_delete=models.CASCADE,null=False)
    item_code=models.ForeignKey(Beverages,on_delete=models.CASCADE,null=False)
    #username=models.ForeignKey(User,on_delete=models.CASCADE)
    bqty=models.IntegerField()
    class Meta:
        unique_together = (("order_idb", "item_code"))
