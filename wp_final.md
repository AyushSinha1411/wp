Initial Commands
mkdir exam
cd exam
python3 -m venv venv
source venv/bin/activate
pip install django
django-admin startproject myproject .
python manage.py startapp myapp
code .


#django_lab_project/myproject/settings.py 

INSTALLED_APPS = [
    'myapp',
]

django_lab_project/myapp/models.py


from django.db import models


class Item(models.Model):
   name = models.CharField(max_length=100)
   quantity = models.IntegerField()
   description = models.TextField(blank=True)


   def __str__(self):
       return f"{self.name} ({self.quantity})"




Commands

python manage.py makemigrations myapp
python manage.py migrate
Make myapp/forms.py

from django import forms
from .models import Item


class ItemForm(forms.ModelForm):
   class Meta:
       model = Item
       fields = ['name', 'quantity', 'description']
       widgets = {
           'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter item name'}),
           'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}),
           'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter item description', 'rows': 3}),
       }




In myapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Item


def home(request):
   if request.method == 'POST':
       item_id = request.POST.get('item_id')
       if item_id:
           item = get_object_or_404(Item, pk=item_id)
           item.name = request.POST['name']
           item.quantity = request.POST['quantity']
           item.description = request.POST['description']
           item.save()
       return redirect('home')
   return render(request, 'myapp/home.html', {'items': Item.objects.all().order_by('name')})


def insert_item(request):
   if request.method == 'POST':
       Item.objects.create(
           name=request.POST['name'],
           quantity=request.POST['quantity'],
           description=request.POST['description']
       )
       return redirect('home')
   return render(request, 'myapp/insert_item.html')


def delete_item(request, item_id):
   if request.method == 'POST':
       get_object_or_404(Item, pk=item_id).delete()
   return redirect('home')



Make myapp/urls.py
from django.urls import path
from . import views


urlpatterns = [
   path('', views.home, name='home'),
   path('insert/', views.insert_item, name='insert_item'),
   path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
]





In myproject/urls.py add



from django.contrib import admin
from django.urls import path,include # add include


urlpatterns = [
   path('admin/', admin.site.urls),
   path('', include('myapp.urls')), # add this line
]


myapp/admin.py
from django.contrib import admin
from .models import Item


class ItemAdmin(admin.ModelAdmin):
   list_display = ('name', 'quantity', 'description')
   search_fields = ('name', 'description')
   ordering = ('name',)


admin.site.register(Item, ItemAdmin)



Run command

python manage.py createsuperuser

myapp/templates/myapp/base.html
<!DOCTYPE html>
<html lang="en">
<head>
   <meta charset="UTF-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title>{% block title %}My Lab Project{% endblock %}</title>
   <!-- Add link to Bootstrap CSS for basic styling (optional) -->
   <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
   <style>
       body { padding: 20px; }
       .action-forms form { display: inline-block; margin-left: 5px; }
   </style>
</head>
<body>
   <div class="container">
       {% block content %}
       {% endblock %}
   </div>
   <!-- Add link to Bootstrap JS bundle (optional) -->
   <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>



myapp/templates/myapp/home.html

{% extends 'myapp/base.html' %}
{% block title %}Items{% endblock %}
{% block content %}
   <div class="d-flex mb-3">
       <h1>Items</h1>
       <a href="{% url 'insert_item' %}" class="btn btn-primary ms-auto">Add</a>
   </div>


   <table class="table">
       <tr>
           <th>Name</th>
           <th>Qty</th>
           <th>Desc</th>
           <th>Actions</th>
       </tr>
       {% for i in items %}
           <tr>
               <td>{{i.name}}</td>
               <td>{{i.quantity}}</td>
               <td>{{i.description|default:"-"}}</td>
               <td>
                   <button onclick="e('{{i.id}}','{{i.name|escapejs}}','{{i.quantity}}','{{i.description|default:''|escapejs}}')"
                           class="btn-sm btn-warning">Edit</button>
                   <form class="d-inline ms-1" onsubmit="return confirm('Delete?');"
                         action="{% url 'delete_item' i.id %}" method="post">
                       {% csrf_token %}
                       <button class="btn-sm btn-danger">Del</button>
                   </form>
               </td>
           </tr>
       {% empty %}
           <tr><td colspan="4" class="text-center">No items</td></tr>
       {% endfor %}
   </table>


   <div class="modal fade" id="m">
       <div class="modal-dialog">
           <div class="modal-content">
               <div class="modal-header">
                   <h5>Edit</h5>
                   <button class="btn-close" data-bs-dismiss="modal"></button>
               </div>
               <form method="post">
                   <div class="modal-body">
                       {% csrf_token %}
                       <input type="hidden" name="item_id">
                       <input class="form-control mb-2" name="name" required>
                       <input type="number" class="form-control mb-2" name="quantity" required>
                       <textarea class="form-control" name="description" rows="2"></textarea>
                   </div>
                   <div class="modal-footer">
                       <button type="button" class="btn-sm btn-secondary" data-bs-dismiss="modal">Cancel</button>
                       <button class="btn-sm btn-primary">Save</button>
                   </div>
               </form>
           </div>
       </div>
   </div>


   <script>
       function e(i,n,q,d) {
           document.querySelector('[name="item_id"]').value = i;
           document.querySelector('[name="name"]').value = n;
           document.querySelector('[name="quantity"]').value = q;
           document.querySelector('[name="description"]').value = d;
           new bootstrap.Modal(document.getElementById('m')).show();
       }
   </script>
{% endblock %}




Insert_item.html

{% extends 'myapp/base.html' %}
{% block title %}Insert Item{% endblock %}
{% block content %}
<div class="container mt-4">
   <h1>Insert New Item</h1>
   <form method="post">
       {% csrf_token %}
       <div class="mb-3">
           <label class="form-label">Name</label>
           <input type="text" name="name" class="form-control" required>
       </div>
       <div class="mb-3">
           <label class="form-label">Quantity</label>
           <input type="number" name="quantity" class="form-control" required>
       </div>
       <div class="mb-3">
           <label class="form-label">Description</label>
           <textarea name="description" class="form-control" rows="3"></textarea>
       </div>
       <button type="submit" class="btn btn-primary">Save</button>
       <a href="{% url 'home' %}" class="btn btn-secondary">Cancel</a>
   </form>
</div>
{% endblock %}



To run

python manage.py runserver

