from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
import django.db

import time
from .models import JobArticle
from .utils import keyfinder, get_page_indices
from .forms import JobsCreateForm


# Create your views here.
def jobs_list_view(request):
    ''' Display the news articles by page beginning from the latest.'''

    job_query = JobArticle.objects.all().order_by('-api_time') # The '-' in front of time makes it descending order
    paginator = Paginator(job_query, 5) # Show 5 news articles per page.

    page_number = request.GET.get('page')
    jobs_page = paginator.get_page(page_number)
    
    # to handle clicking on subsequent page numbers
    l, r = get_page_indices(page_number, paginator)
    custom_range = range(l, r)
    
    context = {
        'paginator': paginator ,
        'jobs_page': jobs_page, 
        'custom_range': custom_range
        }

    return render(request, 'jobs/job_listing.html', context)


def jobs_api_request_view(request):
    ''' Cover the use case of populating the db with news articles '''
    
    choice_keys = ["by", "id", "type", "title", "url", "time"]
    start = time.time()
    job_stories = keyfinder.get_job_posts_with_select_keys(choice_keys)
    end_keyfinder = time.time()
    print('keyfinder function took: ', end_keyfinder - start, ' seconds')

    if job_stories:
        for i in job_stories:
            try:
                JobArticle.objects.create(
                api_id     = i.get('id'),
                api_time   = i.get('time'),
                author     = i.get('by'),
                type       = i.get('type'),
                title      = i.get('title'),
                url        = i.get('url')
            )
            except django.db.utils.IntegrityError:
                print( 'news story ', job_stories.index(i), ' is already in the database')
    else:
        messages.error(request, ("There are no new articles right now. Check again later"))
     
    end_db = time.time()
    print('db run took: ', end_db - end_keyfinder, ' seconds')

    #return(request, "job/jobs_create.html", {})
    return redirect('list-jobs')


def add_job_view(request):
    ''' Cover the use case of a need to upload a specific job article '''
    
    if request.method == "POST":
        form = JobsCreateForm(request.POST or None) 
        if form.is_valid():
            form.save()
            form = JobsCreateForm()

            messages.success(request, ("Job post was added sucessfully."))
            return render(request, "jobs/add_job.html", {'form': form})
    else:
        form = JobsCreateForm
        return render(request, "jobs/add_job.html", {'form': form})

def search_jobs_view(request):
    q = request.GET.get('q')
    if q:
        news_query = JobArticle.objects.distinct().filter(
            Q(title__icontains=q) | 
            Q(author__icontains=q) | 
            Q(url__icontains=q)
            ).order_by('time_added')

        paginator = Paginator(news_query, 5)
        page_number = request.GET.get('page', 1)
        jobs_page = paginator.get_page(page_number)
        
        l, r = get_page_indices(page_number, paginator)
        custom_range = range(l, r)   

        context = {
        'q' : q,
        'count': paginator.count,
        'jobs_page': jobs_page, 
        'custom_range': custom_range
        }

        return render(request, 'jobs/search_jobs.html', context)
    else:
        return render(request, 'jobs/search_jobs.html', {})
