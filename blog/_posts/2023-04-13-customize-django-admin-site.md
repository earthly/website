---
title: "Customizing the Django Admin"
categories:
  - Tutorials
toc: true
author: Chepkirui Dorothy
editor: Mustapha Ahmad Ayodeji

internal-links:
 - Django
 - Python
 - Model
excerpt: |
    Learn how to customize the Django Admin site to enhance the user experience and increase efficiency in managing data within a Django project. This tutorial covers various customization options such as controlling field display, adding filters and thumbnails, linking related objects, and overriding templates and forms.
---
<!--sgpt-->**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization.  Earthly is a powerful tool for CI/CD that can be used to automate the build and deployment process of Django projects, including customizing the Django Admin site. [Check us out](/).**

The Django framework comes with an [admin site](https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#module-django.contrib.admin) which is a quick, model-centric interface that Django creates by reading metadata from your models. The interface allows trusted users to manage model content on your site.
You can easily create, read, update, and delete model content on the admin site. This saves you a lot of time during development.

This tutorial will focus on customizing the Django Admin site. You will create a simple SocialApp to work with. The SocialApp app will have two models, the Author model, and the Post model. The Author model will have a first and last name field, as well as an image field. The Post model will include the author, the content posted, and the date it was created.

We will assume a working understanding of how Django works.

> Note that this article uses version 4.1.2 of Django.

In this tutorial, you will learn to customize the admin site with the following features: controlling field display, disabling models, making lists searchable, adding filters, thumbnails, links, custom validations, and overriding templates and forms.

All the code examples in this tutorial can be found in this [Github](/blog/ci-comparison) [repository](https://github.com/chepkiruidorothy/SocialApp/tree/main/SocialApp_project)

## Project Setup

Set up a Django project and create a Django app to follow up with the rest of this tutorial. I will set up my project and app and call them `SocialApp_project` and `SocialApp` respectively.

Register the `SocialApp` app you created in the list of `INSTALLED_APPS` in the *settings.py* file. Run migrations for the apps that are installed in Django by default.

### Creating the Model

Add the following in the *models.py*:

~~~{.python caption="models.py"}
from django.db import models

class Author(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images", blank=True, null=True)

    def __str__ (self):
        return self.first_name

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    details=models.TextField()
    date=models.DateTimeField(auto_now_add = True)

    def __str__ (self):
        return self.title

~~~

These models represent an author and a post. The Author model has a `first_name`, `last_name`, and an `image` field. The image will be uploaded to the `images` folder you specified in the image field.
The `ImageField` requires that you install the [Pillow](https://pypi.org/project/Pillow/) package.

You can install Pillow with the pip package manager as shown below:

~~~{.bash caption=">_"}
pip install pillow
~~~

The `Post` model has a  `title` field for the post title, a `details` field for the post details, and a `date` field for the date the post was created.

### Configuring the Media File

To configure the [media files](https://docs.djangoproject.com/en/4.1/topics/files/), you will need to specify the location where all the uploaded media files will be stored. You can do this by defining the `MEDIA_ROOT` and `MEDIA_URL` in the *settings.py* file:

Add the following code snippet to *settings.py*:

~~~{.python caption="settings.py"}
import os

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
~~~

The [MEDIA_ROOT](https://docs.djangoproject.com/en/4.1/topics/files/)  setting specifies the path to where the media files are stored. The path is relative to the root directory (`BASEDIR`), while the [MEDIA_URL](https://docs.djangoproject.com/en/4.1/topics/files/) setting defines the base URL for accessing these media files.
This configuration will let Django create an `images` directory under the *media*  folder when the author uploads an image.

### Registering the Models

For a model to be visible on the Django admin site, you need to register it in the *admin.py* file. You can register the model alone or register the model with a subclass of the [`ModelAdmin`](https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#modeladmin-objects) if you want to customize the default interface that Django creates for the model.

The [ModelAdmin](https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#modeladmin-objects) is a class that contains all the information required to define the interface used to handle a specific model.
When you define a `ModelAdmin` class for a model, you can customize the appearance and behavior of the admin interface for that model, such as making the list of model objects searchable.

When you register a model alone, Django will use the default `ModelAdmin` class, which provides a basic interface for working with the records for the model. In this case, you don't have to define a custom `ModelAdmin` class, and you don't have any control over the appearance or behavior of the admin interface for the model.

The following code registers the models with the default `ModelAdmin` class:

~~~{.python caption="admin.py"}
from django.contrib import admin
from .models import  Author, Post

admin.site.register(Author)
admin.site.register(Post)

~~~

If you want to customize the appearance or behavior of the admin interface for a model, you can create a subclass of the `ModelAdmin` class and register the model with that class.

You can register the model with a subclass of the `ModelAdmin` class as shown below:

~~~{.python caption="admin.py"}
from django.contrib import admin
from .models import  Author, Post

class   AuthorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Author, AuthorAdmin)

class PostAdmin(admin.ModelAdmin):
    pass
admin.site.register(Post, PostAdmin)
~~~

Alternatively, you can register the models by decorating the subclass of the `ModelAdmin` class with the `admin.register()` decorator:

~~~{.python caption="admin.py"}

from django.contrib import admin
from .models import  Author, Post

@admin.register(Author)
class   AuthorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Author, AuthorAdmin)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass
admin.site.register(Post, PostAdmin)

~~~

## Accessing the Admin Site

Only a superuser or an admin user can access the admin site. Therefore, you need to create one.

In the terminal, create a superuser that can access the admin site:

~~~{.bash caption=">_"}
./manage.py createsuperuser
~~~

Follow the prompts, and you should create the superuser successfully.

<div class="wide">
![superuser]({{site.images}}{{page.slug}}/yIOfVBG.png)\
</div>

To access the admin site, run the server.

~~~{.bash caption=">_"}
./manage.py runserver
~~~

<div class="wide">
![runserver]({{site.images}}{{page.slug}}/btZCfnq.png)\
</div>

Navigate to *<http://127.0.0.1:8000/admin>* in your browser to access the admin site:

<div class="wide">
![Django admin_site]({{site.images}}{{page.slug}}/Yt5BOLC.png)
</div>

You can add the author and post model objects here.

Click the *Add* button to add details of a new author. Input their first name, last name, and image, then click on the *SAVE* button:

<div class="wide">
![Adding new Author]({{site.images}}{{page.slug}}/5Ag4k0f.png)
</div>

You can add the posts data the same way:

<div class="wide">
![Adding new Post]({{site.images}}{{page.slug}}/Gs3qg78.png)
</div>

## Customizing the Admin Site with the `ModelAdmin` Class

The `ModelAdmin` class has a lot of options for you to modify the interface of the admin site. These options are usually specified as a class attribute or as a method in the `ModelAdmin`class.

### Controlling the Fields to Display Using the `list_display` Attribute

The admin site only shows the string representation of a model when listing the model objects, for the Author model. It shows the first name which is the string representation of the Author model that you defined via the `__str __` method.

~~~{.python caption="models.py"}
    def __str__ (self):
        return self.first_name
~~~

<div class="wide">
![all]({{site.images}}{{page.slug}}/dGrvCiH.png)\
</div>

Suppose you want to list the author's first name, last name, and image in the interface, you can use the `list_display` option of the `ModelAdmin` class as shown below:

~~~{.python caption="admin.py"}
@admin.register(Post)
class   PostAdmin(admin.ModelAdmin):

    list_display = ( "title","author","details","date")
~~~

<div class="wide">
![Displaying author_list]({{site.images}}{{page.slug}}/sjZI5XA.png)
</div>

Clicking on the author's first name will take you to the *change author* page, where you can alter the author's details:

<div class="wide">
![Django change_author page]({{site.images}}{{page.slug}}/wFZbcIk.png)
</div>

### Removing Models from the Admin Site

You can remove a model from the admin site by *unregistering* the model in the *admin.py* file. For example, you can remove the `Group` model of the `auth` app that Django includes by default. The `auth` app includes the `User` model and the `Group` model which are automatically included in the admin site.

To remove the default `Group` model or any model from the admin site, you need to unregister it in the *admin.py* file of your SocialApp project:

~~~{.python caption="models.py"}
from django.contrib.auth.models import Group

admin.site.unregister(Group)
~~~

<div class="wide">
![remove_group]({{site.images}}{{page.slug}}/8oP5JQg.png)\
</div>

### Making the Model Object List Searchable

Django lets you create a search box in the admin interface by adding the [`search_fields`](https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields) attribute in the `ModelAdmin` class. This should be set to a list of field names that will be searched whenever somebody submits a search query in that text box.

You can add the `seach_fields` as shown below:

~~~{.python caption="models.py"}
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):

    list_display = ("first_name", "last_name","image")
    search_fields = ("first_name",)

~~~

Searching for a word will return all model objects where the fields you specified in `search_fields` contain the searched query.

The search bar comes in handy when dealing with a lot of data.

You can search the author's list as shown in the image below:

<div class="wide">
![Searching first_name]({{site.images}}{{page.slug}}/3ixDVm1.png)
</div>

This searches through the list using the `first_name` field only. If you search using the last name, the results would be 0 authors.

<div class="wide">
![Searching author]({{site.images}}{{page.slug}}/r42xowB.png)
</div>

To search using the `first_name` and the `last_name`  fields, add them to the search fields list:

~~~{.python caption="models.py"}
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    
    list_display = ("first_name", "last_name","image")
    search_fields = ("first_name","last_name")

~~~

<div class="wide">
![Search using First & Last name]({{site.images}}{{page.slug}}/mtDbdn9.png)
</div>

### Adding Filters to the List of Model Object

 You can specify a [`list_filter`](https://docs.djangoproject.com/en/4.1/ref/contrib/admin/filters/) attribute in the `ModelAdmin` subclass to narrow down the search space based on the filter that you selected:

~~~{.python caption="models.py"}
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    
    list_display = ("first_name", "last_name","image")
    search_fields = ("first_name",)
    list_filter = ("first_name", )

~~~

The List filters appear in the admin's right sidebar of the change list page:

<div class="wide">
![Navigating search filter]({{site.images}}{{page.slug}}/zcwmARt.png)
</div>

The filter list is automatically populated with the first name values of the authors.

<div class="wide">
![Search filter_last_name]({{site.images}}{{page.slug}}/bup4JhZ.png)
</div>

By clicking on a name, you will change the filter list to display only users with the selected first name.

### Adding Image Thumbnails

So far, images have been listed with their respective URLs, you can choose to display the image thumbnails instead.

To display the thumbnail for a model object, you will need to define an `image_tag` method in the model class of the object. The method returns an HTML `img` tag. You will need the Django's [`mark_safe`](https://docs.djangoproject.com/en/4.1/ref/utils/#module-django.utils.safestring) function to mark the HTML tag safe for output. The `src` attribute of the `img` tag will specify the path to the image.

Add the following in the Author model in *models.py*:

~~~{.python caption="models.py"}
from django.utils.html import mark_safe

class Author(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images", blank=True, null=True)

    def __str__ (self):
        return self.first_name

    def image_tag(self):
        return mark_safe('<img src="%s" width="100px" height="100px" />'%(self.image.url))
    image_tag.short_description = 'Image'

~~~

The `mark_safe`  function marks a string explicitly as safe for (HTML) output. The returned object can be used in any situation where a string or unicode object would be appropriate.

Add the `image_tag` to the `list_display` attribute in *admin.py*:

~~~{.python caption="admin.py"}
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):

    list_display = ("first_name", "last_name","image_tag")

~~~

You will [have to configure *media urls* in the *urls.py*](https://docs.djangoproject.com/en/4.1/howto/static-files/#serving-files-uploaded-by-a-user-during-development) before the images can appear.

Add the following in the *urls.py*:

~~~{.python caption="urls.py"}
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

~~~

This sets up a URL mapping to serve the images in the `MEDIA_ROOT` specified in the project's settings, allowing you to serve user-uploaded files.

> This only works in debug mode

The thumbnail of the images is displayed on the admin site as shown below:

<div class="wide">
![Author's image_tag]({{site.images}}{{page.slug}}/phEY3da.png)
</div>

### Linking Other Object Pages

Objects can refer to other objects using foreign keys. The post model has a many-to-one relationship with the author via ForeignKey which is displayed as an unclickable text on the admin site. The title fields of the Post model are clickable, making it easy to change their details. If you want to change the author's details, you must go to the Author admin page to [make](/blog/using-cmake) the relevant changes. This can become tedious if a lot of changes are to be made.

<div class="wide">
![unclickable]({{site.images}}{{page.slug}}/iKdP0kL.png)\
</div>

However, you can use Django's [URL-reversing](https://docs.djangoproject.com/en/4.1/ref/urlresolvers/) system to access the related object's admin page and [make](/blog/using-cmake) the changes more efficiently. URL reversing refers to the process of converting a named URL pattern to a URL string that can be used in an HTTP request. This makes it easier to link between pages, as you can refer to named URL patterns instead of hardcoded URLs.

~~~{.python caption="models.py"}
from django.utils.html import mark_safe
from django.urls import reverse

@admin.register(Post)
class   PostAdmin(admin.ModelAdmin):

    list_display = ( "title","author_link","details","date")
   
    def author_link(self, obj):
        url = reverse("admin:SocialApp_author_change", args=[obj.author.id])
        link = '<a href="%s">%s</a>' % (url, obj.author.first_name)
        return mark_safe(link)
    author_link.short_description = 'Author'


~~~

This code defines a custom method `author_link` which takes a Post object (`obj`) and returns a link to the change page of its related author.

The URL for the author change page is generated using Django's URL reversing system and the `reverse` function with the named URL pattern `"admin:SocialApp_author_change"` that Django creates for the author change page.

The first part of the name, `admin`, is a namespace that refers to the Django administration interface. `SocialApp_author_change` is a string that represents the URL pattern name for the change page of the author of a SocialApp model.

The naming follows a specific format: `admin:<app_label>_<model_name>_<action>`, where `app_label` refers to the name of the Django app where you defined the model. The `model_name` is the name of the model, in lowercase and `action` is one of several possible actions, such as change, delete, or add.

 The author's ID is passed to the URL pattern with `obj.author.id`, which returns the ID of the related `Author` instance. This ID is used to generate a URL to the change page of the `Author` model, which is then used in the `link` variable to create a link to the change page of the `Author` in the Django admin view.
The `mark_safe` function is used to indicate that the returned string is safe to be displayed. The `short_description` attribute is set to `"Author"` for the header in the Django admin site.

This will hyperlink the author field to its change view, where you can change their first name, last name, and image by just clicking on the hyperlinked first name from the post view:

<div class="wide">
![Navigating to change Author details]({{site.images}}{{page.slug}}/lcPetmg.png)
</div>

The change view:

<div class="wide">
![Changing Author details]({{site.images}}{{page.slug}}/QHM3NPz.png)
</div>

### Adding Custom Validation to the Admin

In a standard web application, users enter data through forms that are then stored in a database. It's crucial to verify that the stored data is valid and meets specific criteria. For instance, email addresses must adhere to a particular format, passwords should be of a minimum length, and dates must be set to occur in the future. We can validate this data with a validator.

A [validator](https://docs.djangoproject.com/en/4.1/ref/validators/) is a callable that accepts a value and raises a `ValidationError` if the value doesn't satisfy specific requirements.
When you try to save objects with invalid values, the Django admin site will indicate a `ValidationError`.
Depending on your project's needs, you will frequently need to create custom validators and raise custom exceptions. You will need to override the `clean` method of the `models.Model` class to perform additional validation on a model before saving it to the database.

Suppose you want the title to have a minimum character limit of 10 letters,
add a `clean` method in the `Post` model as shown below:

~~~{.python caption="models.py"}
from django.core.exceptions import ValidationError

class Post(models.Model):
   ...
   def clean(self):
       if  len(self.title) > 10:
           raise ValidationError(
               {'title': "Title should have at least 10 letters"})



~~~

The `clean` method is used in Django forms to perform custom validation logic on the form data.
This helps ensure that the data entered by the author is consistent and valid before it is saved to the database, avoiding data integrity and consistency issues. If the validation is successful, no errors are raised and the method simply returns None.
If you enter a title that has a length that is less than 10, the validation fails and a `ValidationError` exception is raised:

<div class="wide">
![Title limit of new post]({{site.images}}{{page.slug}}/MFnnaYW.png)
</div>

### Overriding the Admin Templates

You can override many of the templates the admin module uses to generate the various pages of an admin site. This allows you to customize the appearance of the admin site to match your site's design, or to provide a better user experience.

The admin templates folder is stored in your virtual environment.

~~~{ caption=""}
...SocialApp/venv/lib/python3.10/site-packages/django/contrib/admin/templates
.
├── admin
│ ├── 404.html
│ ├── 500.html
│ ├── actions.html
│ ├── app_index.html
│ ├── app_list.html
│ ├── auth
│ │ └── user
│ │ ├── add_form.html
│ │ └── change_password.html
│ ├── base.html
│ ├── base_site.html
│ ├── change_form.html
│ ├── change_form_object_tools.html
│ ├── change_list.html
│ ├── change_list_object_tools.html
│ ├── change_list_results.html
│ ├── date_hierarchy.html
│ ├── delete_confirmation.html
│ ├── delete_selected_confirmation.html
│ ├── edit_inline
│ │ ├── stacked.html
│ │ └── tabular.html
│ ├── filter.html
│ ├── includes
│ │ ├── fieldset.html
│ │ └── object_delete_summary.html
│ ├── index.html
│ ├── invalid_setup.html
│ ├── login.html
│ ├── nav_sidebar.html
│ ├── object_history.html
│ ├── pagination.html
│ ├── popup_response.html
│ ├── prepopulated_fields_js.html
│ ├── search_form.html
│ ├── submit_line.html
│ └── widgets
│ ├── clearable_file_input.html
│ ├── foreign_key_raw_id.html
│ ├── many_to_many_raw_id.html
│ ├── radio.html
│ ├── related_widget_wrapper.html
│ ├── split_datetime.html
│ └── url.html
└── registration
├── logged_out.html
├── password_change_done.html
├── password_change_form.html
├── password_reset_complete.html
├── password_reset_confirm.html
├── password_reset_done.html
├── password_reset_email.html
└── password_reset_form.html


~~~

The admin templates are saved in two directories:
Registration - Templates for the various Django admin page, password change actions, and the Django admin logout page layout.
Admin - for the model object pages

You can create a new template directory and copy the templates you want to override and paste them into your new templates directory. Django will load these templates instead.

Create a new folder called *templates* in the root directory and configure the *settings.py* to include the new template path.

~~~{.python caption="settings.py"}
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

~~~

This defines a list of dictionaries, where each dictionary represents a template backend configuration. In this case, the only template backend defined is [`django.template.backends.django.DjangoTemplates`](https://docs.djangoproject.com/en/4.1/topics/templates/#django.template.backends.django.DjangoTemplates).
The `DIRS` option specifies the directories where Django should look for templates. In this case, the directory is set to `BASE_DIR/templates`, which means that templates should be stored in a directory called *templates* located within the `BASE_DIR` (The root directory). The `APP_DIRS` option is set to `True` which means that Django will also look for templates in the templates directory of the installed apps.

The `OPTIONS` dictionary contains additional settings for the template engine like the `context_processors` setting. The [`context_processors`](https://docs.djangoproject.com/en/4.1/ref/templates/api/#using-requestcontext) option allows you to specify a list of functions to be run before a template is rendered. These functions are called context processors and their purpose is to add additional data to the context that is passed to the template.
Copy the templates you want to change into the new templates directory. The *index.html* file under the admin folder controls how the homepage of the admin behaves. To alter it, create a new folder under the templates folder called the admin folder, and add the *index.html*  file to the folder.

The file tree is as shown below:

~~~{ caption=""}
Templates
└── admin
└── index.html

~~~

You can change the colors of the *Recent actions* and *My actions* titles as shown below:

~~~{.html caption="index.html"}
{% raw %}
{% block sidebar %}
<div id="content-related">
<div class="module" id="recent-actions-module">
<h2 style="color:purple">{% translate 'Recent actions' %} </h2>
<h3 style="color:red">{% translate 'My actions' %}</h3>

...

</div>
</div>
{% endblock %}
{% endraw %}
~~~

<div class="wide">
![Customized colors to template]({{site.images}}{{page.slug}}/siAR9bH.png)
</div>

Overriding the templates will give you a personalized look at each admin page.

### Overriding Django Admin Forms

Django provides the [`ModelForm`](https://docs.djangoproject.com/en/4.1/topics/forms/modelforms/) class, which provides a convenient way to create and update records in the database. By using a model form, you can automatically generate a form based on the fields defined in a Django model. This saves you from having to write HTML for each form field and also ensures that the form fields match the database fields exactly.

However, you can alter the look of the forms to suit your needs. For example, if the post details contained more words and needed more space to edit them, you would need to increase the editing area.

<div class="wide">
![Post's textarea]({{site.images}}{{page.slug}}/qFzqCh6.png)
</div>

~~~{.python caption="admin.py"}

from django.forms import ModelForm, Textarea


class PostForm(ModelForm):
    class Meta:
        model = Post

        fields = '__all__'

        widgets = {
            'details': Textarea(attrs={'cols': 130, 'rows': 20}),
        }

@admin.register(Post)class   PostAdmin(admin.ModelAdmin):

    form = PostForm

~~~

This is a Django form defined using the `ModelForm` class. It represents a form for creating or updating instances of the `Post` model.

The form will contain all fields of the `Post` model, as specified by the `fields` attribute in the Meta class. Additionally, the `widgets` attribute in the Meta class is used to specify the widget to be used for the `details` field, which is a textarea with 130 columns and 20 rows.

This will increase the editing area as shown below:

<div class="wide">
![add_post_details]({{site.images}}{{page.slug}}/GkRzGK8.png)
</div>

## Conclusion

In conclusion, customizing the Django admin site can greatly enhance the user experience and increase efficiency for managing data within a Django project. With a few simple modifications, the Django admin site can be transformed into a powerful tool that fits the unique needs of a project. The possibilities for customization are endless. By taking advantage of the Django admin site's customization capabilities, developers can create a user-friendly experience for managing data in their applications.

In this tutorial, you learn to customize the admin site by controlling field display, disabling models, making model lists searchable, adding filters, thumbnails, links, custom validations, and overriding templates and forms in the admin site.

There is so much to customize in the Django admin. To fully delve into customizing the admin interface, visit the [Django documentation](https://docs.djangoproject.com/en/4.1/ref/contrib/admin/).

{% include_html cta/bottom-cta.html %}