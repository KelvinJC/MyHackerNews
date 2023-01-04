from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib import messages
import django.db
import time


from .models import NewsArticle
from .forms import NewsCreateForm
from .utils import get_page_indices
from api.news import keyfinder

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "home.html", {})

def news_list_view(request):
    ''' Display the news articles by page beginning from the latest.'''

    news_query = NewsArticle.objects.all().order_by('-api_time') # The '-' in front of time makes it descending order
    paginator = Paginator(news_query, 12) # Show 5 news articles per page.

    page_number = request.GET.get('page')
    news_page = paginator.get_page(page_number)
    
    l, r = get_page_indices(page_number, paginator)
    custom_range = range(l, r)
    
    context = {
        'paginator': paginator ,
        'news_page': news_page, 
        'custom_range': custom_range
        }

    return render(request, 'news/news_listing.html', context)


def news_api_request_view(request):
    ''' Cover the use case of populating the db with news articles '''

    choice_keys = ["by", "id", "type", "title", "url", "time"]
    start = time.time()
    stories = keyfinder.get_stories_with_select_keys(choice_keys)
    end_keyfinder = time.time()
    print('keyfinder function took: ', end_keyfinder - start, ' seconds')

    if stories:
        for i in stories:
            try:
                NewsArticle.objects.create(
                api_id     = i.get('id'),
                api_time   = i.get('time'),
                post_by    = i.get('by'),
                type       = i.get('type'),
                title      = i.get('title'),
                url        = i.get('url'),
                author     = None,
            )
            except django.db.utils.IntegrityError:
                print( 'news story ', stories.index(i), ' is already in the database')
    else:
        messages.error(request, ("There are no new articles right now. Check again later"))
        
    end_db = time.time()
    print('db run took: ', end_db - end_keyfinder, ' seconds')

    #return render(request, "news/news_create.html", {}) # need a better return statement. Tests use http status code
    return redirect('list-news')

def search_news_view(request):
    q = request.GET.get('q')
    if q:
        news_query = NewsArticle.objects.distinct().filter(
            Q(title__icontains=q) | 
            Q(post_by__icontains=q) | 
            Q(url__icontains=q) |
            Q(author__username__icontains=q)
            ).order_by('-time_added')

        paginator = Paginator(news_query, 8)
        page_number = request.GET.get('page', 1)
        news_page = paginator.get_page(page_number)
        
        l, r = get_page_indices(page_number, paginator)
        custom_range = range(l, r)   

        context = {
        'q' : q,
        'count': paginator.count,
        'news_page': news_page, 
        'custom_range': custom_range
        }

        return render(request, 'news/search_news.html', context)
    else:
        return render(request, 'news/search_news.html', {})



def add_news_view(request):
    ''' Cover the use case of a need to upload a specific news article '''
    
    if request.method == "POST":
        form = NewsCreateForm(request.POST or None) 
        if form.is_valid():
            news = form.save(commit=False)

            # integer hack to stand in for api id
            # convert username to a string of integers, concatenate with current unix time
            # alternative: separate newsarticle table/model for news articles added by users and not the api
            integer = int(time.time()) # int(''.join(map(str, map(ord, request.user.username))))  + str(int(time.time())))
            
            news.api_id = integer
            print(news.api_id)
            news.author = request.user
            news.api_time = int(time.time()) # adding Unix time of when post is added
            news.save()
            form = NewsCreateForm()
            messages.success(request, ("Job post was added sucessfully."))
            return render(request, "news/add_news.html", {'form': form})
        else:
            return render(request, "news/add_news.html", {'form': form})
    else:
        form = NewsCreateForm
        return render(request, "news/add_news.html", {'form': form})

# former version of get_unique_news_article
# def get_news_article_view(request):
#     api_request = HackerAPIRequest()
#     ids = api_request.fetch_all_story_ids() # should be fetch the last 100 eg or last 50. Not efficient to be comparing against all ids in db each time
#     queryset = NewsArticle.objects.all()
#     unique_ids = set(ids) ^ set(queryset) # find the elements not common to ids and queryset
    
#     if unique_ids:
#         unique_stories = api_request.fetch_each_story(unique_ids)
#     return render(request, "")

