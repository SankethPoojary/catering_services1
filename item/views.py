from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.db.models import F
from django.http import HttpResponse
from .models import Beverages,Item,beverage_cart,food_cart,order,User,order_details
from django.http import JsonResponse
import json
from django.contrib import messages
from datetime import datetime,timedelta
from django.db import IntegrityError
import stripe
from django.conf import settings
from django.shortcuts import render, redirect
import uuid
# Create your views here.

import random
import string
type1_cussin="SouthIndian"
type2_v_n="veg"
type3_course="BreakFast"
food_item=[]

def generate_id(length=10):
    # Define the characters to use in the ID
    chars = string.ascii_uppercase + string.digits
    
    # Generate a random ID with the given length
    id = ''.join(random.choice(chars) for _ in range(length))
    
    # Add any other formatting or prefix/suffix to the ID as needed
    # Example: prefix = "ID-", suffix = "-01", final_id = prefix + id + suffix
    
    return id
def index(request):
    return render(request,'index.html')
def client(request):
    global type3_course
    global type1_cussin
    global type2_v_n
    global item
    global item1
    global food_item
    cussin=["SouthIndian","NorthIndian","Chinese"]
    if  request.GET.get("SouthIndian"):
        type1_cussin="SouthIndian"
    if  request.GET.get("NorthIndian"):
        type1_cussin="NorthIndian"
    if  request.GET.get("Chinese"):
        type1_cussin="Chinese"
    if  request.GET.get("beverages"):
        type1_cussin="beverages"
    if  request.GET.get("veg"):
        type2_v_n=request.GET.get("veg")
    if  request.GET.get("Alcoholic"):
        type2_v_n=request.GET.get("Alcoholic")
    item=Item.objects.all().filter( type1=type1_cussin,type2=type2_v_n,type3=type3_course)
    bev=Beverages.objects.all().filter( type1=type2_v_n,type2=type3_course)
    if request.GET.get("type3_course"):
        type3_course=request.GET.get('type3_course')
    print(type1_cussin)
    print(type2_v_n)
    print(type3_course)
    
    if request.GET.get("buy"):
       # checking(request)
        print("working")
        i_code=request.GET.get("buy")
        quant=request.GET.get("quantity")
        food_item.append(request.GET.get("buy"))
        food_item1=set(food_item)
        food_item2=list(food_item1)
        print(food_item)
        item1=Item.objects.all().filter(item_code__in=food_item2)
        bev1=Beverages.objects.all().filter( item_code1=request.GET.get("buy"))
        print(item1)
        return  cart(request,i_code,quant)
        #return render(request,'clientdisplay.html',{'item':item,'bev':bev,'type1_cussin':type1_cussin,'cussin':cussin,'type3_course':type3_course,'type2_v_n':type2_v_n,'item1':item1,'bev1':bev1})
    if  type1_cussin in ['SouthIndian','NorthIndian','Chinese']:
            if type2_v_n in ["veg","nonveg"]:
                if type3_course in ['BreakFast','Starters','MainCourse','Dessert']:

                    item=Item.objects.all().filter( type1=type1_cussin,type2=type2_v_n,type3=type3_course)
                    return render(request,'clientdisplay.html',{'item':item,'type1_cussin':type1_cussin,'cussin':cussin,'type3_course':type3_course,'type2_v_n':type2_v_n}) 
                else:
                    item=Item.objects.all().filter( type1=type1_cussin,type2=type2_v_n)
                    return render(request,'clientdisplay.html',{'item':item,'type1_cussin':type1_cussin,'cussin':cussin,'type3_course':type3_course,'type2_v_n':type2_v_n}) 
            else:
                type2_v_n="veg"
                type3_course="BreakFast"
                item=Item.objects.all().filter( type1=type1_cussin,type2=type2_v_n,type3=type3_course)
                return render(request,'clientdisplay.html',{'item':item,'type1_cussin':type1_cussin,'cussin':cussin,'type3_course':type3_course,'type2_v_n':type2_v_n}) 
    elif type1_cussin in ['beverages']:
        if type2_v_n in ["Alcoholic","NonALcoholic"]:
            if type3_course in ['Beer','Wine','Vodka','Rum','Whisky','Tequila','Tea','Coffee','FruitJuice','SoftDrinks','MilkShake']: 
                bev=Beverages.objects.all().filter( type1=type2_v_n,type2=type3_course)
                return render(request,'clientdisplay.html',{'bev':bev,'cussin':cussin,'type1_cussin':type1_cussin,'type3_course':type3_course,'type2_v_n':type2_v_n}) 
            else:
                type3_course='Beer'
                bev=Beverages.objects.all().filter( type1=type2_v_n,type2=type3_course)
                return render(request,'clientdisplay.html',{'bev':bev,'cussin':cussin,'type1_cussin':type1_cussin,'type3_course':type3_course,'type2_v_n':type2_v_n}) 
        else:
            bev=Beverages.objects.all().filter( type1=type2_v_n)
            return render(request,'clientdisplay.html',{'bev':bev,'type1_cussin':type1_cussin,'cussin':cussin,'type3_course':type3_course,'type2_v_n':type2_v_n})
    
    else:
        item=Item.objects.all().filter( type1="SouthIndian",type2="veg",type3="BreakFast")
        return render(request,'clientdisplay.html',{'item':item,'type1_cussin':type1_cussin,'cussin':cussin,'type3_course':type3_course,'type2_v_n':type2_v_n})


def placeorder(request):
    ord=order_details()
    o_idf=order.objects.filter(username=request.user,is_ordered=False).values_list('order_id',flat=True).first()
    i_codef=food_cart.objects.filter(order_idf=o_idf).values_list('item_code',flat=True)
    i_codeb=beverage_cart.objects.filter(order_idb=o_idf).values_list('item_code',flat=True)
    #qf=food_cart.objects.filter(order_idf=o_idf).values('fquantity','price').aggregate(F('fquantity') * F('price'))
    qf=list(food_cart.objects.filter(order_idf=o_idf).values_list('fquantity',flat=True))
    qb=list(beverage_cart.objects.filter(order_idb=o_idf).values_list('bqty',flat=True))
    pf=list(Item.objects.all().filter(item_code__in=i_codef).values_list('price',flat=True))
    pb=list(Beverages.objects.all().filter(item_code1__in=i_codeb).values_list('price',flat=True))
    print('food quantity',qf)
    print('bevr quantity',qb)
    print('food price',pf)
    print('bevr price',pb)
    price=0
    for i in range(0,len(qf)):
        price=price+(qf[i]*pf[i])
    print(price)
    for i in range(0,len(qb)):
        price=price+(qb[i]*pb[i])
    print('price' ,price)
    if price>10000:
        if request.method=='POST':
            if order_details.objects.filter(delivery_date=request.POST.get('date')).count()<5:
                try:
                    ord.order_id_id=order.objects.filter(username=request.user,is_ordered=False).values_list('order_id',flat=True).first()
                    ord.username=request.user
                    ord.name=request.POST.get('uname')
                    ord.address=request.POST.get('address')
                    ord.phone_no=request.POST['phone']
                    ord.state=request.POST.get('state')
                    ord.city=request.POST.get('city')
                    ord.postal_code=request.POST.get('pc')
                    check_date=datetime.now()+timedelta(days=7)
                    print('direct',type(request.POST.get('date')))
                    print('got date',datetime.strptime(request.POST.get('date'),'%Y-%m-%d'))
                    print('check date',check_date)
                    if datetime.strptime(request.POST.get('date'),'%Y-%m-%d') > check_date:
                        print('correct')
                        ord.delivery_date=request.POST.get('date')
                        #return redirect('checkout')

                       

                    else:
                        print('errrr')
                        messages.error(request,'must place the order before 1 week')
                        return redirect('placeorder')
                    ord.payment_id=generate_id()
                    ord.total_price=price
                    ord.order_date=datetime.now()
                    ord.save()
                    order.objects.filter(order_id=o_idf).update(is_ordered=True)
                    print("inserted")
                except IntegrityError:
                    messages.error(request,"your order is already placed")
                    return redirect('placeorder')
            else:
                messages.error(request,"Maximum order limit reached try next delivery date")
                return redirect('placeorder')
        #looop hole
    else:
        messages.error(request,"minimum price for the order should be more than 10,000")
        return redirect('client')
    return render(request,'placeorder.html')
def price(request):
    return render(request,'price.html')
def cussin(request):
    print('hello')
    return render(request,'cussin.html') 

def cart(request,i_code,quant):
    print("called")
    o_idf=order.objects.filter(username=request.user,is_ordered=False).values_list('order_id',flat=True).first()
   # print(request.POST.get("del"))
    if request.user.id in list(order.objects.filter(username=request.user).values_list('username',flat=True)):
        print('username present')
        if True==all(list(order.objects.filter(username=request.user).values_list('is_ordered',flat=True))):
            ord=order()
            ord.order_id=generate_id()
            ord.username=request.user
            #ord.payment_id=generate_id()
            ord.save()
           
    else:
        ord=order()
        ord.order_id=generate_id()
        ord.username=request.user
       # ord.payment_id=generate_id()
        ord.save()
        ('username not present')
    #if request.user in table
    food_cart1=food_cart()
    bev_cart=beverage_cart()
    #quant=request.POST.get("quantity")
    #i_code=request.POST.get("food_id")
    #i_code=request.POST.get("buy")
    print(request.user)
    print(quant,i_code)
    o_idf=order.objects.filter(username=request.user,is_ordered=False).values_list('order_id',flat=True).first()
    if 'FD'==i_code[0:2]:
        print('fd if')
        if i_code not in list(food_cart.objects.filter(order_idf=o_idf).values_list('item_code',flat=True)):
            food_cart1.order_idf_id=order.objects.filter(username=request.user,is_ordered=False).values_list('order_id',flat=True).first()
            food_cart1.item_code=Item.objects.filter(item_code=i_code).first()
            food_cart1.fquantity=quant
            food_cart1.save()
            messages.success(request,"item  added to the cart successfully")
            print("food inserted")
            return redirect('client')
        else:
            messages.error(request,"item already present in your cart")
            print("element alredy present")
            return redirect('client')
                #give new order_id
    elif 'DR'==i_code[0:2]:
        if i_code not in list(beverage_cart.objects.filter(order_idb=o_idf).values_list('item_code',flat=True)):
            bev_cart.order_idb_id=order.objects.filter(username=request.user,is_ordered=False).values_list('order_id',flat=True)
            bev_cart.item_code=Beverages.objects.filter(item_code1=i_code).first()
            bev_cart.bqty=quant
            bev_cart.save()
            print("brev inserted")
            messages.success(request,"item  added to the cart successfully")
            return redirect('client')
        else:
            messages.error(request,"item already present in your cart")
            print("element alredy present")
            return redirect('client')
    food_codeb=beverage_cart.objects.all().filter(order_idb=o_idf).values_list('item_code',flat=True)
    food_codei=food_cart.objects.all().filter(order_idf=o_idf).values_list('item_code',flat=True)
    item=Item.objects.all().filter(item_code__in=food_codei)
    bev=Beverages.objects.all().filter(item_code1__in=food_codeb) 
    food_quanb=beverage_cart.objects.all().filter(order_idb=o_idf)
    food_quanf=food_cart.objects.all().filter(order_idf=o_idf)
    print(' food_quanf', food_quanf)
    print(' food_quanb', food_quanb)
    return render(request,'cart.html',{'items':item,'bev':bev,'quanf': food_quanf,'quanb':food_quanb})
def cart1(request):
    print("carrt")
    #present price
    ord=order_details()
    o_idf=order.objects.filter(username=request.user,is_ordered=False).values_list('order_id',flat=True).first()
    o_idf1=order.objects.filter(username=request.user,is_ordered=True).values_list('order_id',flat=True)[1:2]
    i_codef=food_cart.objects.filter(order_idf=o_idf).values_list('item_code',flat=True)
    i_codeb=beverage_cart.objects.filter(order_idb=o_idf).values_list('item_code',flat=True)
    #qf=food_cart.objects.filter(order_idf=o_idf).values('fquantity','price').aggregate(F('fquantity') * F('price'))
    qf=list(food_cart.objects.filter(order_idf=o_idf).values_list('fquantity',flat=True))
    qb=list(beverage_cart.objects.filter(order_idb=o_idf).values_list('bqty',flat=True))
    pf=list(Item.objects.all().filter(item_code__in=i_codef).values_list('price',flat=True))
    pb=list(Beverages.objects.all().filter(item_code1__in=i_codeb).values_list('price',flat=True))
    print('food quantity',qf)
    print('bevr quantity',qb)
    print('food price',pf)
    print('bevr price',pb)
    pres_price=0
    for i in range(0,len(qf)):
        pres_price=pres_price+(qf[i]*pf[i])
    for i in range(0,len(qb)):
        pres_price=pres_price+(qb[i]*pb[i])
    print(pres_price)
    #previous price
    i_codef=food_cart.objects.filter(order_idf=o_idf1).values_list('item_code',flat=True)
    i_codeb=beverage_cart.objects.filter(order_idb=o_idf1).values_list('item_code',flat=True)
    #qf=food_cart.objects.filter(order_idf=o_idf).values('fquantity','price').aggregate(F('fquantity') * F('price'))
    qf=list(food_cart.objects.filter(order_idf=o_idf1).values_list('fquantity',flat=True))
    qb=list(beverage_cart.objects.filter(order_idb=o_idf1).values_list('bqty',flat=True))
    pf=list(Item.objects.all().filter(item_code__in=i_codef).values_list('price',flat=True))
    pb=list(Beverages.objects.all().filter(item_code1__in=i_codeb).values_list('price',flat=True))
    print('food quantity',qf)
    print('bevr quantity',qb)
    print('food price',pf)
    print('bevr price',pb)
    prev_price=0
    for i in range(0,len(qf)):
        prev_price=prev_price+(qf[i]*pf[i])
    for i in range(0,len(qb)):
        prev_price=prev_price+(qb[i]*pb[i])
    print(prev_price)
    o_idf=order.objects.filter(username=request.user,is_ordered=False).values_list('order_id',flat=True).first()
   
    #previous
    food_codeb=beverage_cart.objects.all().filter(order_idb=o_idf).values_list('item_code',flat=True)
    food_codei=food_cart.objects.all().filter(order_idf=o_idf).values_list('item_code',flat=True)
    item=Item.objects.all().filter(item_code__in=food_codei)
    bev=Beverages.objects.all().filter(item_code1__in=food_codeb)
    food_quanb=beverage_cart.objects.all().filter(order_idb=o_idf)
    food_quanf=food_cart.objects.all().filter(order_idf=o_idf)
    print(' food_quanf', food_quanf)
    print(' food_quanb', food_quanb)

    #previous order
    
    print(o_idf1)
    food_codeb1=beverage_cart.objects.all().filter(order_idb__in=o_idf1).values_list('item_code',flat=True)
    food_codei1=food_cart.objects.all().filter(order_idf__in=o_idf1).values_list('item_code',flat=True)
    item1=Item.objects.all().filter(item_code__in=food_codei1)
    bev1=Beverages.objects.all().filter(item_code1__in=food_codeb1)
    food_quanb1=beverage_cart.objects.all().filter(order_idb=o_idf1)
    food_quanf1=food_cart.objects.all().filter(order_idf=o_idf1)

    if request.GET.get('delete'):
        print("work")
        if 'FD'==request.GET.get('delete')[0:2]:
            print("called")
            food_cart.objects.all().filter(order_idf=o_idf,item_code=request.GET.get("delete")).delete()
        else:
            print("beer called")
            beverage_cart.objects.all().filter(order_idb=o_idf,item_code=request.GET.get("delete")).delete()
    if request.POST.get('edit'):
            up_quan=request.POST.get('quantity')
            if 'FD'==request.POST.get('edit')[0:2]:
                print("updated")
                
                food_cart.objects.all().filter(order_idf=o_idf,item_code=request.POST.get('edit')).update(fquantity=up_quan)
            else:
                print("no update")
                beverage_cart.objects.all().filter(order_idb=o_idf,item_code=request.POST.get("edit")).update(bqty=up_quan)
    if request.POST.get('delf'):
            food_cart.objects.all().filter(order_idf=o_idf).delete()
    if request.POST.get('delb'):
            beverage_cart.objects.all().filter(order_idb=o_idf).delete()
    if request.POST.get('delall'):
            food_cart.objects.all().filter(order_idf=o_idf).delete()
            beverage_cart.objects.all().filter(order_idb=o_idf).delete()
    if request.GET.get('searchbtn'):
            print('search')
            search=request.GET.get('search')
            item1=Item.objects.filter(item_name__icontains=search)
            bev1=Beverages.objects.filter(item_name__icontains=search)
    if request.GET.get('searchbtn1'):
        print('search1')
        search=request.GET.get('search1')
        print(search)
        item=Item.objects.filter(item_name__icontains=search)
        bev=Beverages.objects.filter(item_name__icontains=search)
    #present order
    
    return render(request,'cart.html',{'items':item,'bev':bev,'quanf': food_quanf,'quanb':food_quanb,'item1':item1,'bev1':bev1,'quanb1':food_quanb1,'quanf1':food_quanf1,'pres_price':pres_price, 'prev_price':prev_price})


def check(request):
    o_idf=order.objects.filter(username=request.user,is_ordered=False).values_list('order_id',flat=True).first()
    print(request)
    print(request.GET.get('del'))
    food_cart.objects.all().filter(order_idf=o_idf,item_code=request.GET.get("del")).values_list('item_code',flat=True)
    return redirect('cart1')



stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    ord=order_details()
    o_idf=order.objects.filter(username=request.user,is_ordered=True).values_list('order_id',flat=True).first()
    print(o_idf)
    amt=order_details.objects.filter(order_id=o_idf).values_list('total_price',flat=True).first()
    print(amt)
    if request.method == 'POST':
        """ try:
            # Create a new charge object
            charge = stripe.Charge.create(
                amount=10000,
                currency='usd',
                description='Payment gateway',
                source=request.POST.get('stripeToken')
            )
        except stripe.error.CardError as e:
            # Display error message to the user
            return render(request, 'checkout.html', {'error': e.error.message}) """

        # Payment successful, redirect to success page
        messages.success(request,'your order has been successfully placed ')
        return redirect('home')
    
    # Render the checkout form
    return render(request, 'checkout.html', {'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,'amount':amt})
