from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from django.shortcuts import redirect
from django.shortcuts import reverse

def add_page(request,category_name_slug):
    try:
        category=Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category=None
        
    #if it doesnt exist, go back to the homepage
    if category is None:
        return redirect('/rango/')
        
    form = PageForm()
    
    #checks if user submitted data via the form
    if request.method=='POST':
        form = PageForm(request.POST)
        
        if form.is_valid():
            if category:
                page=form.save(commit=False)
                page.category=category
                page.views=0
                page.save()
                
                #send user to the show_category view, reverse() looks up URLs in views.py (rango:show_category
                #second parameter makes sure complete URL can be formulaed to send to redirect() method
                return redirect(reverse('rango:show_category',kwargs={'category_name_slug':category_name_slug}))
        else:
            #error print
            print(form.errors)
    
    context_dict={'form': form, 'category':category}            
    #handles errors
    return render(request, 'rango/add_page.html', context=context_dict)

def add_category(request):
    form = CategoryForm()
    
    #checks if user submitted data via the form
    if request.method=='POST':
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            #save new category to db
            form.save(commit=True)
            #redirect to index view for now
            return redirect('/rango/')
        else:
            #error print
            print(form.errors)
    #handles errors
    return render(request, 'rango/add_category.html', {'form': form})
def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine 
    context_dict = {}
    
    try:
        # If we can find a category name slug with the given name, the .get() method returns one model instance, else it raises a DoesNotExist exception.
        category = Category.objects.get(slug=category_name_slug)
        
        # Retrieve all of the associated pages.
        # The filter() will return a list of objects or an empty list.
        pages = Page.objects.filter(category=category)
        
        # Adds our results list to the template context under name pages
        context_dict['pages'] = pages
        #Add the category object from the database to the context dictionary.
        #Use this in the template to verify that the category exists.
        context_dict['category'] =category
        
    except Category.DoesNotExist:
        # Don't do anything, the template will sort it
        context_dict['category'] = None
        context_dict['pages'] = None
    # Render the response and return it to the client
    return render(request, 'rango/category.html', context=context_dict)


def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by the number of likes in descending order.
    # Retrieve the top 5 only -- or all if less than 5.
    # Place the list in our context_dict dictionary (with our boldmesage!) that will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    
    page_list = Page.objects.order_by('-views')[:5]


    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    
    context_dict['pages'] = page_list
    
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context = context_dict)
    
def about(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    # context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
    # , context = context_dict
    
    # Return a rendered response to send to the client.
    #We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'rango/about.html')