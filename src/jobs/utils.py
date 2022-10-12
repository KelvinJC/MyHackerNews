import requests
import ast
from concurrent.futures import ThreadPoolExecutor
from abc import ABC, abstractmethod

from .models import JobArticle

class APIRequest(ABC):
    @abstractmethod
    def fetch_all_job_post_ids():
        pass

class HackerAPIJobsRequest(APIRequest):
    id_url = "https://hacker-news.firebaseio.com/v0/jobstories.json"
    each_job_story_url = "https://hacker-news.firebaseio.com/v0/item/{}.json"

    def fetch_all_job_post_ids(self):
        payload = "{}"
        response = requests.request("GET", self.id_url, data=payload) # should be wrapped in try catch block against network errors

        res_text = response.text
        # reponse.text appears to be a list of integers cast in a string
        all_ids = (res_text).strip('[').strip(']').split(',')
        all_ids_int = [int(i) for i in all_ids]
        return all_ids_int

    def find_new_ids(self):
        '''
        Queries db to get all past ids
        Compares list of past ids with current request
        Returns all new ids or None
        '''
        request_ids = self.fetch_all_job_post_ids()
        print(request_ids)
        old_ids = JobArticle.objects.values_list('api_id', flat=True)
        print('old_ids', old_ids)
        new_ids = list(set(request_ids) - set(old_ids))
        print('set request ids', set(request_ids))
        print('set old ids', set(old_ids))
        print('req - old', set(request_ids) - set(old_ids))
        print('new ids', new_ids)
        if new_ids:
            return new_ids
        return None

    # Use the obtained ids to fetch each job from the Get item endpoint 
    def fetch_job_posts_with_id(self, ids):
        ''' uses multi-threading to make concurrent HTTP requests to external api'''
        def get_url(url):
            return requests.get(url).text

        if ids:
            list_of_urls = [self.each_job_story_url.format(i) for i in ids]
            
            with ThreadPoolExecutor(max_workers=50) as pool:
                a = list(pool.map(get_url, list_of_urls))  

            return a
       
        print('no new job stories from fetch fxn')
        return None

class KeyFinder():
    def __init__(self, request: APIRequest): 
        self.request = request

    def get_job_posts_with_select_keys(self, keys):
        new_job_stories = self.request.fetch_job_posts_with_id(self.request.find_new_ids()) 
        if new_job_stories:
            b = []
            for i in new_job_stories:
                i = ast.literal_eval(i)
                choice_dict = {k: v for k, v in i.items() if k in keys }
                b.append(choice_dict)   
            return b
        else:
            print('No new job stories')
            return None

request = HackerAPIJobsRequest()
keyfinder = KeyFinder(request)





def get_page_indices(page, paginator):
    try:
        leftIndex = (int(page) - 3)
    except TypeError:
        leftIndex = 1

    if leftIndex < 1:
        leftIndex = 1
    
    try:
        rightIndex = (int(page) + 3)
    except TypeError:
        rightIndex = 9
    
    if leftIndex == 1:
        rightIndex = 6   

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    return leftIndex, rightIndex



