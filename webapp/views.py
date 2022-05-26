import re
from urllib.robotparser import RequestRate
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect, render
import mysql.connector as mc 
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import json
from .models import *
import os
# Create your views here.

def admin(request):
    return render(request,'Admin.html')


def login(request):
    if request.method=='POST':
        try:
            data=json.loads(request.body)
            Email=data['email']    
            Password=data['password']
        except:
            emailid=request.POST['Email']
            if Role.objects.get(Email=User.objects.get(Email=emailid)).Role=='Admin':
                    return redirect('home')
            else:
                request.session['User']=emailid
                return redirect('Home')
        if User.objects.filter(Email=Email).exists():
            UserObject= User.objects.get(Email=Email)
            if(UserObject.Password != Password and len(Password)>0):
                return JsonResponse({'error2':'The password does not match the username'})
            else:
                return JsonResponse({'valid':True})
        else:
            return JsonResponse({'error1':'Email does not exist'})
    return render(request,"Login1.html")

def register(request):
    if request.method=='POST':
        try:
            data=json.loads(request.body)
        except:
            print('register page')
            data=User(FirstName=request.POST['FirstName'],LastName=request.POST['LastName'],Email=request.POST['Email'],Password=request.POST['Password'])
            data.save()
            r=Role(Email=data,Role="User")
            r.save()
            # emailid=request.POST['Email']
            # request.session['User']=emailid
            return redirect('Login')
        email=data['emailid']    
        if User.objects.filter(Email=email).exists():
            return JsonResponse({'error1':'Email Already in use'})
        else:
            return JsonResponse({'username_valid':True})
    return render(request,"Register1.html")  

def home(request):   
    return render(request,'index.html')

def add_product(request):
    if request.method == 'POST':
        mydb=mc.connect(host="localhost",user="bot1",passwd="12345")
        mycursor=mydb.cursor()
        mycursor.execute("use smart_trolley_django")
        mycursor.execute("create table if not exists product_details(prod_name varchar(50),prod_id varchar(10),location varchar(8),category varchar(20))")
        mydb.commit()
        '''
        add_items method takes 4 parameters(product_name,product_id,product_location,product_category)
        '''
        mycursor.execute("insert into product_details values('%s','%s','%s','%s');"%(request.POST['product_name'],request.POST['product_id'],request.POST['product_location'],request.POST['product_category']))
        mydb.commit()
        print("Item added")
        name="Added successfully"
        return render(request,'add_product.html')
    return render(request,'add_product.html')


def set_location_product(request):
    if request.method=='POST':
            mydb=mc.connect(host="localhost",user="bot1",passwd="12345")
            mycursor=mydb.cursor()
            mycursor.execute("use smart_trolley_django")
            mycursor.execute("create table if not exists coordinates_table(location varchar(10))")
            mydb.commit()

            print("req obj",request.POST['column'])
            location_list=[request.POST['column'],request.POST['row'],request.POST['rack']]
            location="-".join(i for i in location_list)
            print("location",location)
            # mycursor.execute("update coordinates_table set location='%s' where location='%s';))
            def onclick(event): 
                
                #print("location=%s, xdata=%f, ydata=%f" % (location_list[counter], event.xdata, event.ydata))
                print(" [%f, %f] " % ( event.xdata, event.ydata))
                
                mycursor.execute('''update coordinates_table set x_cord='%s',y_cord='%s' where location='%s';'''%(event.xdata,event.ydata,location))
                
                
                mydb.commit()
                

            def onrelease(event):
                pass
            img = mpimg.imread('../smart_trolley_django/static/imgs/floor_1.png')
            plt.figure(figsize = (12,12))
            ax = plt.imshow(img)
            fig = ax.get_figure()
            cid = fig.canvas.mpl_connect('button_press_event', onclick) 
            cid = fig.canvas.mpl_connect('button_press_event', onrelease)
            plt.show()
            
    return render(request,'product_location_setter.html')


def tables(request):
    mydb=mc.connect(host="localhost",user="bot1",passwd="12345")
    mycursor=mydb.cursor()
    mycursor.execute("use smart_trolley_django")
    mycursor.execute("select * from product_details")

    myresult=mycursor.fetchall()
    # prod_name,prod_id,location,category=myresult[0]
    # print(prod_name,prod_id,location,category)


    return render(request,'tables.html',{'result':myresult})

# def upload_image(request):
    
#         # mydb=mc.connect(host="localhost",user="bot1",passwd="12345")
#         # mycursor=mydb.cursor()
#         # mycursor.execute("use smart_trolley_django")
#         # mycursor.execute("create table if not exists product_image(prod_id varchar(10),image varchar(100))")
#         # mydb.commit()
#         # mycursor.execute("insert into product_image values('%s','%s');"%(request.POST['product_id'],request.POST['image']))
#         # mydb.commit()
#         # print("Image uploaded")
#         # name="Uploaded successfully"
#         # return render(request,'404.html')
#         if request.method=='POST':
#             print(request.POST['shop_name'])        
#         return render(request,'upload_image.html')


# def login(request):
#     return render(request,'login.html')

# def register(request):
#     return render(request,'register.html')

def upload_image(request):
    

    UPLOAD_FOLDER = './uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    

    if request.method == 'POST':
        # def upload_file():
        #     if request.method == 'POST':
        #         # check if the post request has the file part
        #         if 'file' not in request.files:
        #             flash('No file part')
        #             return redirect(request.url)
        #         file = request.files['file']
        #         # if user does not select file, browser also
        #         # submit an empty part without filename
        #         if file.filename == '':
        #             flash('No selected file')
        #             return redirect(request.url)
        #         #if file and allowed_file(file.filename):
        #         if file:
        #             filename = secure_filename(file.filename)
        #             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #             return redirect(url_for('uploaded_file',
        #                                     filename=filename))
        file=request.FILES['file']
        img_save_location= "E:/projects/smart trolley django/smart_trolley_django/static/imgs/layouts.png"
        with open(img_save_location,'wb') as fi:
            for chunk in file.chunks():
                fi.write(chunk)
       
    #     file.save(os.path.join('../smart trolley django/smart_trolley_django/static/imgs',file.filename))
        return render(request,'404.html')
    return render(request,'upload_image.html')
    
    
def view_layout(request):
    return render(request,'view_layout.html')

def settings(request):
    return render(request,'settings.html')

def error_404(request):
    return render(request,'404.html')


