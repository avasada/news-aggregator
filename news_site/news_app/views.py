from django.shortcuts import render, redirect
from news_app.models import Person
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup as BSoup
from news_app.models import Headline
from newsapi import NewsApiClient
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import ensure_csrf_cookie, requires_csrf_token, csrf_exempt

# Create your views here.

#def home(request):
    #return render(request, "home.html")


def addData(request):
    first_name = request.GET.get("first_name")
    last_name = request.GET.get("last_name")
    person = Person(first_name=first_name, last_name=last_name)
    person.save()
    return HttpResponse("Data added successfully")

def receiveData(request):
    pk = request.GET.get("pk")
    try:
        person = Person.objects.get(pk=pk)
        return HttpResponse(f"Received person: {person.first_name} {person.last_name}")
    except Person.DoesNotExist:
        return HttpResponse("Person not found", status=404)


def scrape(request):
    # Clear existing articles from the database
    Headline.objects.all().delete()

    newsapi = NewsApiClient(api_key='04b5ec18c6cd40b0ac9bfaf87ffc39f9')

    categories = ['science', 'technology', 'health']

    all_articles = [] #list to hold all the articles

    for category in categories:
        top_headlines = newsapi.get_top_headlines(language='en', country='us', category=category)

        # Process fetched headlines
        for article in top_headlines['articles']:
            title = article['title']
            link = article['url']
            image_src = article.get('urlToImage', '')  # Use get to avoid KeyError if 'urlToImage' is missing
            category_name = category  # Set the category for each article

            # Check if the article with the same title already exists in the database
            existing_article = Headline.objects.filter(title=title).first()
            if existing_article is None:
                # If the article doesn't exist, save it to the database
                new_headline = Headline(title=title, url=link, image=image_src, category=category_name)
                new_headline.save()

    return redirect("/")


@cache_control(max_age=3600)  # Set cache-control header to cache response for 1 hour
def news_list(request):
    headlines = Headline.objects.all()
    context = {
        'object_list': headlines,
    }
    return render(request, "home.html", context)

'''
def category_page(request):
    headlines = Headline.objects.all()
    context = {
        'object_list': headlines,
    }
    return render(request, "category.html", context)
'''

def category_page(request, category):
    headlines = Headline.objects.filter(category=category)  # Adjust the filter to match your model fields
    context = {
        'object_list': headlines,
        'category': category,  # Add this line to pass 'category' to the template
    }
    return render(request, 'category.html', context)

@csrf_exempt
def search(request, category=None):
    print("hello world")  # Debug message (can be removed in production)
    
    # Get the search query from the POST request
    query = request.POST.get('query', '')  # Use a default of empty string if 'query' is not provided
    
    print(query)
    
    # Initialize the queryset for headlines
    if category:
        # Filter headlines by category and possibly by the search query if provided
        if query:
            headlines = Headline.objects.filter(title__icontains=query, category=category)
        else:
            # If no query is provided, return all headlines in the specified category
            headlines = Headline.objects.filter(category=category)
    else:
        # If no category is specified, filter only by the query or return all
        if query:
            headlines = Headline.objects.filter(title__icontains=query)
        else:
            headlines = Headline.objects.all()

    # Render the search results to a template
    return render(request, 'category.html', {'object_list': headlines, 'category': category})
