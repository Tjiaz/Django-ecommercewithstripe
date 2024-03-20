from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from myapp.models import Contact,Product,Orders,OrderUpdate
from math import ceil
import stripe
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt


from django.contrib import messages
# Create your views here.


def index(request):
    allProducts =[]
    catProducts = Product.objects.values('category','id')
   
    cats = {item['category'] for item in catProducts}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n=len(prod)
        nSlides = n // 4 + ceil((n/4) - - (n//4))
        allProducts.append([prod,range(1,nSlides),nSlides])
    params = {'allProducts':allProducts}

    return render(request, 'index.html',params)

def contact(request):
    if request.method == 'POST':
        name=request.POST.get("fullname")
        email=request.POST.get("email")
        desc=request.POST.get("desc")
        pnumber=request.POST.get("phone_number")
        myquery=Contact(name=name,email=email,desc=desc,phonenumber=pnumber)
        myquery.save()
        messages.info(request,"We will get back to you soon...")
        return redirect('contact')
    else:  # This will handle GET requests
        return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2: 
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email already exists')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username already used')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save();
                return redirect('login')
        else:
            messages.info(request,"password not the same")
            return redirect('register')
    else:
        return render(request,'register.html')
   
def login(request):
    if request == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Credential Invalid')
            return redirect('/login')
    else:
         return render(request,'login.html')
   

# def checkout(request):
    
#     if not request.user.is_authenticated:
#         messages.warning(request,"Login & Try Again")
#         return redirect('/auth/login')

#     if request.method=="POST":
#         items_json = request.POST.get('itemsJson', '')
#         name = request.POST.get('name', '')
#         amount = request.POST.get('amt')
#         email = request.POST.get('email', '')
#         address1 = request.POST.get('address1', '')
#         address2 = request.POST.get('address2','')
#         city = request.POST.get('city', '')
#         state = request.POST.get('state', '')
#         zip_code = request.POST.get('zip_code', '')
#         phone = request.POST.get('phone', '')
#         Order = Orders(items_json=items_json,name=name,amount=amount, email=email, address1=address1,address2=address2,city=city,state=state,zip_code=zip_code,phone=phone)
#         print(amount)
#         Order.save()
#         update = OrderUpdate(order_id=Order.order_id,update_desc="the order has been placed")
#         update.save()
#         thank = True

# # # PAYMENT INTEGRATION

#         id = Order.order_id
#         oid=str(id)+"ShopyCart"
#         param_dict = {

#             'MID':keys.MID,
#             'ORDER_ID': oid,
#             'TXN_AMOUNT': str(amount),
#             'CUST_ID': email,
#             'INDUSTRY_TYPE_ID': 'Retail',
#             'WEBSITE': 'WEBSTAGING',
#             'CHANNEL_ID': 'WEB',
#             'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',

#         }
#         # param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
#         return render(request, 'paytm.html', {'param_dict': param_dict})

#     return render(request, 'checkout.html')


@csrf_exempt
# def handlerequest(request):
#     # paytm will send you post request here
#     form = request.POST
#     response_dict = {}
#     for i in form.keys():
#         response_dict[i] = form[i]
#         if i == 'CHECKSUMHASH':
#             checksum = form[i]

#     # verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
#     if verify:
#         if response_dict['RESPCODE'] == '01':
#             print('order successful')
#             a=response_dict['ORDERID']
#             b=response_dict['TXNAMOUNT']
#             rid=a.replace("ShopyCart","")
           
#             print(rid)
#             filter2= Orders.objects.filter(order_id=rid)
#             print(filter2)
#             print(a,b)
#             for post1 in filter2:

#                 post1.oid=a
#                 post1.amountpaid=b
#                 post1.paymentstatus="PAID"
#                 post1.save()
#             print("run agede function")
#         else:
#             print('order was not successful because' + response_dict['RESPMSG'])
#     return render(request, 'paymentstatus.html', {'response': response_dict})


def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/auth/login')
    currentuser=request.user.username
    items=Orders.objects.filter(email=currentuser)
    rid=""
    for i in items:
        print(i.oid)
        # print(i.order_id)
        myid=i.oid
        rid=myid.replace("ShopyCart","")
        print(rid)
    status=OrderUpdate.objects.filter(order_id=int(rid))
    for j in status:
        print(j.update_desc)

   
    context ={"items":items,"status":status}
    # print(currentuser)
    return render(request,"profile.html",context)



stripe.api_key = settings.STRIPE_SECRET_KEY

# def stripeCheckout(request):
#      checkout_session = stripe.checkout.Session.create(
#             line_items=[
#                 {
#                     # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
#                     'price': 'price_1Ov9LjKx7UNSCrUkbzz302ul',
#                     'quantity': 1,
#                 },
#             ],
#             mode='subscription',
#             success_url='http://127.0.0.1:8000',
#             cancel_url='http://127.0.0.1:8000',
#         )
    
#      return redirect(checkout_session.url,code=303)


# def stripeCheckout(request):
#     # Create a Stripe checkout session
#     checkout_session = stripe.checkout.Session.create(
#         payment_method_types=['card'],
#         line_items=[
#             {
#                 'price': 'price_1Ov9LjKx7UNSCrUkbzz302ul',  
#                 'quantity': 1,
#             },
#         ],
#         mode='payment',
#         success_url='http://127.0.0.1:8000/success/',
#         cancel_url='http://127.0.0.1:8000/cancel/',
#     )
#     return redirect(checkout_session.url)

# def success(request):
#     return HttpResponse("Payment successful")

# def cancel(request):
#     return HttpResponse("Payment cancelled")


def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')

    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        Order = Orders(items_json=items_json, name=name, amount=amount, email=email, address1=address1, address2=address2, city=city, state=state, zip_code=zip_code, phone=phone)
        Order.save()
        update = OrderUpdate(order_id=Order.order_id, update_desc="the order has been placed")
        update.save()
        thank = True

        # Redirect to Stripe checkout
        return stripeCheckout(request)

    return render(request, 'checkout.html')

def stripeCheckout(request):
    # Create a Stripe checkout session
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price': 'price_1Ov9LjKx7UNSCrUkbzz302ul',  
                'quantity': 1,
            },
        ],
        mode='subscription',
        success_url='http://127.0.0.1:8000/success/',
        cancel_url='http://127.0.0.1:8000/cancel/',
    )
    return redirect(checkout_session.url)

def success(request):
    return HttpResponse("Payment successful")

def cancel(request):
    return HttpResponse("Payment cancelled")