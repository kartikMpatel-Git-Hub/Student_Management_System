from django.shortcuts import render
from django.http import HttpResponse
from .models import User
from mysql.connector import Connect,Error
# Create your views here.



def register_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        s = User()
        s.email = email
        s.password = password
        s.save()
        return HttpResponse('User Create Succesfully !!')
    else:
        return render(request,'Pages/register.html')

def login_user(request):
    my_context = {}
    try:
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')
            User.objects.get(email = email,password = password)
            return render(request,'Pages/index.html')
        else:
            return render(request,'Pages/login.html')
    except Error:
        my_context['error'] = "Invalid credentials"
        return render(request,'Pages/login.html',my_context)

def connection():
    try:
        con = Connect(host="localhost",user="root",password="K@rtik.018",database = "dbstudent")
        return con
    except Error as e:
        return None

def insert_data(request):
    con = connection()
    cursor = con.cursor()
    try:
        if request.method == 'POST':
            rno = int(request.POST.get("rollno"))
            sname = request.POST.get('name')
            c = int(request.POST.get('cmark'))
            cpp = int(request.POST.get('cppmark'))
            py = int(request.POST.get('pythonmark'))
            cursor.callproc('insertData',(rno,sname,c,cpp,py))
            con.commit()
            return render(request,'Pages/respons.html',{'error' : 'Data Inserted'})
        else:
            return render(request,'Pages/insert.html')
    except Error as e:
        return HttpResponse('Something Went Wrong..',e)
    
def delete_data(request):
    con = connection()
    cursor = con.cursor()
    try:
        if request.method == 'POST':
            rno = int(request.POST.get("rollno"))
            cursor.callproc('deleteRow',(rno,))
            con.commit()
            return render(request,'Pages/respons.html',{'error' : 'Data Deleted'})
        else:
            return render(request,'Pages/delete.html')
    except Error as e:
        return HttpResponse('Something Went Wrong...',e)    
def update_data(request):
    con = connection()
    cursor = con.cursor()
    try:
        if request.method == 'POST':
            try:
                rno = int(request.POST.get("rollno"))
                sname = request.POST.get('name')
                c = int(request.POST.get('cmark'))
                cpp = int(request.POST.get('cppmark'))
                py = int(request.POST.get('pythonmark'))
                cursor.callproc('updateData',(rno,sname,c,cpp,py))
                con.commit()
            except Error as e:
                return HttpResponse(e)
            return render(request,'Pages/respons.html',{'error' : 'Data Updated'})
        else:
            return render(request,'Pages/update.html')
    except Error as e:
        return HttpResponse('Something Went Wrong...')
    
def show_data(request):
    con = connection()
    cursor = con.cursor()
    try:
        sql = "select * from tblstudent order by (cmarks + cppmarks + pythonmarks) desc limit 3"
        cursor.execute(sql)
        rows = cursor.fetchall()
        list_recoard = []
        for row in rows:
            rollno,name,c,cpp,py = row
            total = c + cpp + py
            list_recoard.append((rollno,name,c,cpp,py,total))
        return render(request,'Pages/show.html',{'records' : list_recoard})
    except Error as e:
        return HttpResponse(e)

def redirect_home(request):
    return render(request,"Pages/index.html")