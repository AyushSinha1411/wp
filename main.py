#!/usr/bin/env python3

import os
import subprocess
import sys
import platform
import getpass
import time

# --- Configuration ---
PROJECT_PARENT_DIR = "."  # Directory where 'exam' will be created
PROJECT_DIR_NAME = "exam"
PROJECT_NAME = "myproject"
APP_NAME = "myapp"
VENV_NAME = "venv"
OPEN_VSCODE = True # Set to False if you don't want to open VS Code automatically
ADD_GITIGNORE = True # Set to True to add a basic Python .gitignore

# --- Platform Specific Paths ---
if platform.system() == "Windows":
    VENV_BIN_DIR = os.path.join(VENV_NAME, "Scripts")
    PYTHON_EXEC = os.path.join(VENV_BIN_DIR, "python.exe")
    PIP_EXEC = os.path.join(VENV_BIN_DIR, "pip.exe")
    DJANGO_ADMIN_EXEC = os.path.join(VENV_BIN_DIR, "django-admin.exe")
    ACTIVATE_CMD = os.path.join(VENV_BIN_DIR, "activate") # Note: activation is implicit via exec path
else: # Linux/macOS
    VENV_BIN_DIR = os.path.join(VENV_NAME, "bin")
    PYTHON_EXEC = os.path.join(VENV_BIN_DIR, "python")
    PIP_EXEC = os.path.join(VENV_BIN_DIR, "pip")
    DJANGO_ADMIN_EXEC = os.path.join(VENV_BIN_DIR, "django-admin")
    ACTIVATE_CMD = f"source {os.path.join(VENV_BIN_DIR, 'activate')}" # Note: activation is implicit via exec path

# --- Helper Functions ---
def run_command(command, cwd=None, env=None, shell=False):
    """Executes a shell command and checks for errors."""
    print(f"\n---> Running Command: {' '.join(command) if isinstance(command, list) else command}")
    try:
        process = subprocess.run(
            command,
            check=True,
            cwd=cwd,
            text=True,
            capture_output=True,
            env=env,
            shell=shell # Needed for commands like 'source' if used, but prefer direct exec path
        )
        print(process.stdout)
        if process.stderr:
            print("STDERR:", process.stderr, file=sys.stderr)
        print(f"<--- Command Successful: {' '.join(command) if isinstance(command, list) else command}")
        time.sleep(0.5) # Small delay for filesystem changes
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(command) if isinstance(command, list) else command}", file=sys.stderr)
        print(f"Return Code: {e.returncode}", file=sys.stderr)
        print(f"Output:\n{e.stdout}", file=sys.stderr)
        print(f"Error Output:\n{e.stderr}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print(f"Error: Command not found - {command[0] if isinstance(command, list) else command.split()[0]}", file=sys.stderr)
        print("Please ensure Python 3, pip, and potentially git are installed and in your PATH.", file=sys.stderr)
        return False

def create_or_update_file(filepath, content, mode='w', insert_after=None, insert_before=None, replace_line=None):
    """Creates a new file, overwrites an existing one, appends, or inserts content."""
    print(f"---> Writing/Updating File: {filepath}")
    try:
        # Ensure parent directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        if mode == 'w' or not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        elif mode == 'a':
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(content)
        elif insert_after or insert_before or replace_line:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            processed = False
            with open(filepath, 'w', encoding='utf-8') as f:
                for i, line in enumerate(lines):
                    if replace_line and replace_line in line:
                         print(f"     Replacing line containing '{replace_line}'")
                         f.write(content + "\n") # Assume content is the replacement line
                         processed = True
                    elif insert_after and insert_after in line and not processed:
                        print(f"     Inserting content after line containing '{insert_after}'")
                        f.write(line)
                        f.write(content + "\n")
                        processed = True
                    elif insert_before and insert_before in line and not processed:
                        print(f"     Inserting content before line containing '{insert_before}'")
                        f.write(content + "\n")
                        f.write(line)
                        processed = True
                    else:
                        f.write(line)
                # If marker not found for insertion, append (optional, maybe error prone)
                # if not processed and (insert_after or insert_before):
                #     print(f"     Warning: Marker line not found. Appending content to {filepath}")
                #     f.write("\n" + content + "\n")

        print(f"<--- File Updated: {filepath}")
        time.sleep(0.2) # Small delay
    except IOError as e:
        print(f"Error writing to file {filepath}: {e}", file=sys.stderr)
        raise # Re-raise the exception to stop the script

def get_input_with_prompt(prompt, default=None):
    """Gets user input, providing a default value."""
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "

    value = input(prompt).strip()
    return value if value else default

# --- File Contents ---

SETTINGS_PY_APP_INSERT = f"    '{APP_NAME}',"
SETTINGS_PY_INSERT_MARKER = "INSTALLED_APPS = ["

MODELS_PY_CONTENT = """
from django.db import models

class Item(models.Model):
   name = models.CharField(max_length=100)
   quantity = models.CharField(max_length=100) # Consider IntegerField or DecimalField if appropriate

   def __str__(self):
       return f"{self.name} ({self.quantity})"
"""

FORMS_PY_CONTENT = """
from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
   class Meta:
       model = Item
       fields = ['name', 'quantity']
       widgets = {
           'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter item name'}),
           'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}), # Consider forms.NumberInput
       }
"""

VIEWS_PY_CONTENT = """
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from .models import Item
# from .forms import ItemForm # Consider using Django Forms for validation/rendering

def home(request):
   if request.method == 'POST':
       item_id = request.POST.get('item_id')
       if item_id:
           try:
               item = get_object_or_404(Item, pk=int(item_id))
               # Basic validation (could be improved with Django Forms)
               name = request.POST.get('name', '').strip()
               quantity = request.POST.get('quantity', '').strip()
               if not name or not quantity:
                   # Handle error - perhaps flash message or return error response
                   # For simplicity, redirecting here. A better UX would show errors.
                   print("Warning: Empty name or quantity submitted during edit.")
                   return redirect('home')
               item.name = name
               item.quantity = quantity # Consider validation/conversion if not CharField
               item.save()
           except (ValueError, Item.DoesNotExist):
                return HttpResponseBadRequest("Invalid Item ID") # Or handle more gracefully
       else:
           # This case might indicate an issue with the form if item_id is expected
           print("Warning: POST request received on home view without item_id.")
           pass # Or handle potential incorrect submissions
       return redirect('home')

   items = Item.objects.all().order_by('name') # Order items for consistency
   context = {'items': items}
   return render(request, 'myapp/home.html', context)


def insert_item(request):
   if request.method == 'POST':
       # Basic validation (could be improved with Django Forms)
       name = request.POST.get('name', '').strip()
       quantity = request.POST.get('quantity', '').strip()
       if name and quantity:
            Item.objects.create(
                name=name,
                quantity=quantity, # Consider validation/conversion
            )
            return redirect('home')
       else:
            # Handle error - perhaps show form with errors
            # For simplicity, rendering the form again here.
            print("Warning: Empty name or quantity submitted during insert.")
            return render(request, 'myapp/insert_item.html', {'error': 'Both fields are required.'})

   # If GET request or failed POST:
   return render(request, 'myapp/insert_item.html')


def delete_item(request, item_id):
   if request.method == 'POST':
       try:
           item = get_object_or_404(Item, pk=int(item_id))
           item.delete()
       except (ValueError, Item.DoesNotExist):
            return HttpResponseBadRequest("Invalid Item ID") # Or handle more gracefully
   # Always redirect to home, even for GET requests to this URL (though ideally only POST is used)
   return redirect('home')
"""

APP_URLS_PY_CONTENT = """
from django.urls import path
from . import views

# app_name = 'myapp' # Optional: Add this for namespacing URLs

urlpatterns = [
   path('', views.home, name='home'),
   path('insert/', views.insert_item, name='insert_item'),
   path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
]
"""

PROJECT_URLS_PY_IMPORT_REPLACE = "from django.urls import path, include # add include"
PROJECT_URLS_PY_IMPORT_FIND = "from django.urls import path"
PROJECT_URLS_PY_PATH_INSERT = f"    path('', include('{APP_NAME}.urls')), # add this line"
PROJECT_URLS_PY_PATH_MARKER = "urlpatterns = ["


ADMIN_PY_CONTENT = """
from django.contrib import admin
from .models import Item

@admin.register(Item) # Use decorator for cleaner registration
class ItemAdmin(admin.ModelAdmin):
   list_display = ('name', 'quantity')
   search_fields = ('name',) # Comma is important for single-item tuples
   ordering = ('name',) # Comma is important
"""

BASE_HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}My Lab Project{% endblock %}</title>
  {# Add link to CSS framework or custom CSS here if desired #}
  <style>
    body { font-family: sans-serif; margin: 20px; }
    table { border-collapse: collapse; margin-top: 1em; width: 100%; max-width: 600px; }
    th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
    th { background-color: #f2f2f2; }
    td form { display: inline; margin-left: 5px; }
    button { padding: 5px 10px; cursor: pointer; }
    .action-buttons button, .action-buttons form button { margin-right: 5px; }
    a { text-decoration: none; color: blue; }
    a:hover { text-decoration: underline; }
    .add-link { display: inline-block; margin-bottom: 1em; padding: 8px 15px; background-color: #4CAF50; color: white; border-radius: 4px; }
    .modal { display: none; position: fixed; left: 50%; top: 50%; transform: translate(-50%, -50%); border: 1px solid #ccc; padding: 20px; background: white; box-shadow: 0 4px 8px rgba(0,0,0,0.1); z-index: 1000; min-width: 300px; }
    .modal h5 { margin-top: 0; border-bottom: 1px solid #eee; padding-bottom: 10px; }
    .modal label { display: block; margin-top: 10px; }
    .modal input[type=text], .modal input[type=number] { width: 95%; padding: 8px; margin-top: 5px; border: 1px solid #ccc; }
    .modal .buttons { margin-top: 15px; text-align: right; }
    .modal .buttons button { margin-left: 10px; }
    .error { color: red; margin-top: 10px; }
  </style>
</head>
<body>
  <main>
    {% block content %}
    {% endblock %}
  </main>
  {# Add link to JS framework or custom JS here if desired #}
  {% block extra_js %}{% endblock %}
</body>
</html>
"""

HOME_HTML_CONTENT = """{% extends 'myapp/base.html' %}
{% load static %} {# Example if you use static files later #}

{% block title %}Items{% endblock %}

{% block content %}
 <h1>Items</h1>
 <a href="{% url 'insert_item' %}" class="add-link">Add New Item</a>

 {% if items %}
 <table border="1">
     <thead>
         <tr>
             <th>Name</th>
             <th>Quantity</th>
             <th>Actions</th>
         </tr>
     </thead>
     <tbody>
         {% for item in items %}
             <tr>
                 <td>{{ item.name }}</td>
                 <td>{{ item.quantity }}</td>
                 <td class="action-buttons">
                     {# Use data-* attributes for better JS interaction #}
                     <button onclick="openEditModal('{{ item.id }}', '{{ item.name|escapejs }}', '{{ item.quantity|escapejs }}')">Edit</button>
                     <form onsubmit="return confirm('Are you sure you want to delete {{ item.name|escapejs }}?');" action="{% url 'delete_item' item.id %}" method="post" style="display: inline;">
                         {% csrf_token %}
                         <button type="submit">Delete</button>
                     </form>
                 </td>
             </tr>
         {% endfor %}
     </tbody>
 </table>
 {% else %}
     <p>No items found. <a href="{% url 'insert_item' %}">Add the first item!</a></p>
 {% endif %}

 {# Edit Modal Dialog #}
 <div id="edit-modal" class="modal">
     <h5>Edit Item</h5>
     <form id="edit-form" method="post" action="{% url 'home' %}"> {# Posts back to the home view #}
         {% csrf_token %}
         <input type="hidden" name="item_id" id="edit-item-id">

         <label for="edit-name">Name:</label>
         <input type="text" id="edit-name" name="name" required>

         <label for="edit-quantity">Quantity:</label>
         {# Use type="text" if model field is CharField, use type="number" if Integer/Decimal #}
         <input type="text" id="edit-quantity" name="quantity" required>

         <div class="buttons">
             <button type="button" onclick="closeEditModal()">Cancel</button>
             <button type="submit">Save Changes</button>
         </div>
     </form>
     <button onclick="closeEditModal()" style="position: absolute; top: 10px; right: 10px; background: none; border: none; font-size: 1.2em; cursor: pointer;">×</button>
 </div>
{% endblock %}

{% block extra_js %}
 <script>
     const modal = document.getElementById('edit-modal');
     const form = document.getElementById('edit-form');
     const itemIdInput = document.getElementById('edit-item-id');
     const nameInput = document.getElementById('edit-name');
     const quantityInput = document.getElementById('edit-quantity');

     function openEditModal(id, name, quantity) {
         itemIdInput.value = id;
         nameInput.value = name;
         quantityInput.value = quantity; // Quantity might need parsing if it's numeric in JS
         modal.style.display = 'block';
     }

     function closeEditModal() {
         modal.style.display = 'none';
         // Optional: Clear form fields on close
         // form.reset();
     }

     // Optional: Close modal if clicking outside of it
     // window.onclick = function(event) {
     //     if (event.target == modal) {
     //         closeEditModal();
     //     }
     // }
 </script>
{% endblock %}
"""

INSERT_ITEM_HTML_CONTENT = """{% extends 'myapp/base.html' %}

{% block title %}Insert Item{% endblock %}

{% block content %}
  <h1>Insert New Item</h1>

  {# Display error message if present #}
  {% if error %}
    <p class="error">{{ error }}</p>
  {% endif %}

  <form method="post" action="{% url 'insert_item' %}">
      {% csrf_token %}
      <div>
          <label for="name">Name:</label><br>
          {# Use value="{{ request.POST.name }}" to retain value on error #}
          <input type="text" id="name" name="name" required value="{{ request.POST.name | default:'' }}">
      </div>
      <br>
      <div>
          <label for="quantity">Quantity:</label><br>
          {# Use type="text" if model field is CharField, use type="number" if Integer/Decimal #}
          {# Use value="{{ request.POST.quantity }}" to retain value on error #}
          <input type="text" id="quantity" name="quantity" required value="{{ request.POST.quantity | default:'' }}">
      </div>
      <br>
      <button type="submit">Save</button>
      <a href="{% url 'home' %}" style="margin-left: 10px;">Cancel</a>
  </form>
{% endblock %}
"""

GITIGNORE_CONTENT = """
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a CI, but they might be saved in your repository source tree.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal # add this line
media/ # If you store user uploads here

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having different versions across platforms makes it problematic - ignore it.
# Pipfile.lock

# PEP 582; used by PDM, Flit and tdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/ # Updated VENV_NAME here
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rove Concepts testing tools
.datadir/

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# VSCode
.vscode/

# OSX / Misc
.DS_Store
"""


# --- Main Script Logic ---
def main():
    start_time = time.time()
    print("--- Starting Django Project Setup ---")

    # Get absolute path for the project directory
    project_path = os.path.abspath(os.path.join(PROJECT_PARENT_DIR, PROJECT_DIR_NAME))
    print(f"Project will be created in: {project_path}")

    # 1. Create Project Directory
    if not os.path.exists(project_path):
        print(f"---> Creating Directory: {project_path}")
        os.makedirs(project_path)
    else:
        print(f"--- Directory already exists: {project_path}")

    # --- Change to Project Directory ---
    try:
        os.chdir(project_path)
        print(f"--- Changed directory to: {os.getcwd()}")
    except OSError as e:
        print(f"Error: Could not change directory to {project_path}: {e}", file=sys.stderr)
        sys.exit(1)

    # --- Inside 'exam' directory from here ---

    # 2. Create Virtual Environment
    if not os.path.exists(VENV_NAME):
         # Use the python executable that runs this script
        if not run_command([sys.executable, "-m", "venv", VENV_NAME], cwd=project_path):
            print("Error: Failed to create virtual environment.", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"--- Virtual environment '{VENV_NAME}' already exists. Skipping creation.")
        # Check if essential executables exist
        if not os.path.exists(PYTHON_EXEC) or not os.path.exists(PIP_EXEC):
             print(f"Error: Virtual environment '{VENV_NAME}' seems incomplete. Missing executables.", file=sys.stderr)
             print(f"Please delete the '{VENV_NAME}' folder and run the script again.", file=sys.stderr)
             sys.exit(1)


    # 3. Install Django (using the venv pip)
    if not run_command([PIP_EXEC, "install", "django"], cwd=project_path):
        print("Error: Failed to install Django.", file=sys.stderr)
        sys.exit(1)

    # 4. Start Django Project (if manage.py doesn't exist)
    manage_py_path = os.path.join(project_path, "manage.py")
    if not os.path.exists(manage_py_path):
        if not run_command([DJANGO_ADMIN_EXEC, "startproject", PROJECT_NAME, "."], cwd=project_path):
             print("Error: Failed to create Django project.", file=sys.stderr)
             sys.exit(1)
    else:
        print(f"--- Django project ('{manage_py_path}') already exists. Skipping 'startproject'.")


    # 5. Start Django App (if app directory doesn't exist)
    app_path = os.path.join(project_path, APP_NAME)
    if not os.path.exists(app_path):
        if not run_command([PYTHON_EXEC, manage_py_path, "startapp", APP_NAME], cwd=project_path):
            print("Error: Failed to create Django app.", file=sys.stderr)
            sys.exit(1)
    else:
         print(f"--- Django app ('{APP_NAME}') already exists. Skipping 'startapp'.")

    # 6. Add Gitignore (Optional)
    if ADD_GITIGNORE:
        gitignore_path = os.path.join(project_path, ".gitignore")
        gitignore_content_updated = GITIGNORE_CONTENT.replace("venv/", f"{VENV_NAME}/") # Adjust for custom venv name
        create_or_update_file(gitignore_path, gitignore_content_updated)

    # --- Modify/Create Files ---
    try:
        # settings.py
        settings_file = os.path.join(project_path, PROJECT_NAME, "settings.py")
        create_or_update_file(settings_file, SETTINGS_PY_APP_INSERT, mode='insert', insert_after=SETTINGS_PY_INSERT_MARKER)

        # myapp/models.py
        models_file = os.path.join(app_path, "models.py")
        create_or_update_file(models_file, MODELS_PY_CONTENT)

        # Run initial migrations BEFORE creating files that depend on models (like forms/admin)
        # 7. Make Migrations for the app
        if not run_command([PYTHON_EXEC, manage_py_path, "makemigrations", APP_NAME], cwd=project_path):
            print(f"Error: Failed to run makemigrations for {APP_NAME}.", file=sys.stderr)
            # Allow continuing, maybe models haven't changed, but warn user.
            # sys.exit(1) # Uncomment to make this fatal

        # 8. Apply Migrations
        if not run_command([PYTHON_EXEC, manage_py_path, "migrate"], cwd=project_path):
            print("Error: Failed to run migrate.", file=sys.stderr)
            sys.exit(1)

        # myapp/forms.py
        forms_file = os.path.join(app_path, "forms.py")
        create_or_update_file(forms_file, FORMS_PY_CONTENT)

        # myapp/views.py
        views_file = os.path.join(app_path, "views.py")
        create_or_update_file(views_file, VIEWS_PY_CONTENT)

        # myapp/urls.py
        app_urls_file = os.path.join(app_path, "urls.py")
        create_or_update_file(app_urls_file, APP_URLS_PY_CONTENT)

        # myproject/urls.py
        project_urls_file = os.path.join(project_path, PROJECT_NAME, "urls.py")
        # First, ensure 'include' is imported
        create_or_update_file(project_urls_file, PROJECT_URLS_PY_IMPORT_REPLACE, mode='replace', replace_line=PROJECT_URLS_PY_IMPORT_FIND)
        # Then, add the app's url pattern
        create_or_update_file(project_urls_file, PROJECT_URLS_PY_PATH_INSERT, mode='insert', insert_after=PROJECT_URLS_PY_PATH_MARKER)


        # myapp/admin.py
        admin_file = os.path.join(app_path, "admin.py")
        create_or_update_file(admin_file, ADMIN_PY_CONTENT)

        # Create template directories
        templates_dir = os.path.join(app_path, "templates", APP_NAME)
        os.makedirs(templates_dir, exist_ok=True)
        print(f"---> Created directory: {templates_dir}")

        # myapp/templates/myapp/base.html
        base_html_file = os.path.join(templates_dir, "base.html")
        create_or_update_file(base_html_file, BASE_HTML_CONTENT)

        # myapp/templates/myapp/home.html
        home_html_file = os.path.join(templates_dir, "home.html")
        create_or_update_file(home_html_file, HOME_HTML_CONTENT)

        # myapp/templates/myapp/insert_item.html (Corrected filename)
        insert_item_html_file = os.path.join(templates_dir, "insert_item.html")
        create_or_update_file(insert_item_html_file, INSERT_ITEM_HTML_CONTENT)

    except IOError as e:
        print(f"Fatal Error during file operation: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during file setup: {e}", file=sys.stderr)
        sys.exit(1)


    # 9. Create Superuser (non-interactively)
    print("\n--- Create Superuser ---")
    print("You need to create an administrator account for Django.")

    # Get username, email, and password securely
    superuser_username = get_input_with_prompt("Enter superuser username", default=os.environ.get('USER', 'admin'))
    superuser_email = get_input_with_prompt("Enter superuser email", default=f"{superuser_username}@example.com")
    while True:
        superuser_password1 = getpass.getpass("Enter superuser password: ")
        superuser_password2 = getpass.getpass("Confirm superuser password: ")
        if superuser_password1 == superuser_password2:
            if superuser_password1: # Ensure password is not empty
                 break
            else:
                 print("Password cannot be empty. Please try again.")
        else:
            print("Passwords do not match. Please try again.")

    # Set environment variables for non-interactive creation
    superuser_env = os.environ.copy()
    superuser_env["DJANGO_SUPERUSER_USERNAME"] = superuser_username
    superuser_env["DJANGO_SUPERUSER_EMAIL"] = superuser_email
    superuser_env["DJANGO_SUPERUSER_PASSWORD"] = superuser_password1

    # Check if user already exists before attempting creation
    # This requires running a manage.py command, which might be complex to parse reliably here.
    # A simpler approach is to just try creating it and let Django handle the "already exists" error gracefully.
    # The --noinput flag will prevent prompts if the user exists.
    print("Attempting to create superuser...")
    if not run_command([PYTHON_EXEC, manage_py_path, "createsuperuser", "--noinput"], cwd=project_path, env=superuser_env):
        print("Warning: 'createsuperuser --noinput' failed. The user might already exist, or there could be another issue.", file=sys.stderr)
        print("You may need to create the superuser manually using:", file=sys.stderr)
        print(f"  cd {PROJECT_DIR_NAME}", file=sys.stderr)
        print(f"  {ACTIVATE_CMD}", file=sys.stderr) # Show activate command
        print(f"  python manage.py createsuperuser", file=sys.stderr)
        # Don't exit, setup might still be mostly complete.

    # 10. Open VS Code (Optional)
    if OPEN_VSCODE:
        print("\n---> Opening project in VS Code...")
        try:
            # Use subprocess.Popen to detach the process
             subprocess.Popen(["code", "."], cwd=project_path)
             print("<--- VS Code launch command issued.")
        except FileNotFoundError:
            print("Warning: 'code' command not found. VS Code might not be installed or not in your PATH.", file=sys.stderr)
        except Exception as e:
            print(f"Warning: Could not open VS Code: {e}", file=sys.stderr)

    # --- Final Instructions ---
    end_time = time.time()
    print("\n--- Django Project Setup Complete ---")
    print(f"Total time: {end_time - start_time:.2f} seconds")
    print("\nTo run your Django development server:")
    print(f"1. Navigate to the project directory: cd {PROJECT_DIR_NAME}")
    print(f"2. Activate the virtual environment:")
    if platform.system() == "Windows":
        print(f"   {VENV_NAME}\\Scripts\\activate")
    else:
        print(f"   source {VENV_NAME}/bin/activate")
    print(f"3. Run the server:")
    print(f"   python manage.py runserver")
    print("\nThen open your web browser to http://127.0.0.1:8000/")
    print("Access the admin interface at http://127.0.0.1:8000/admin/ using the superuser credentials you created.")


if __name__ == "__main__":
    main()
