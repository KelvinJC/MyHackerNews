import requests
import json
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
        res_text = json.loads(response.text)
        all_ids_int = [int(i) for i in res_text]
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
    def fetch_job_posts_with_id(self):
        ''' uses multi-threading to make concurrent HTTP requests to external api'''
        def get_url(url):
            return json.loads(requests.get(url).text)
        
        ids = self.find_new_ids()
        if ids:
            list_of_urls = [self.each_job_story_url.format(i) for i in ids]
            
            with ThreadPoolExecutor(max_workers=50) as pool:
                a = list(pool.map(get_url, list_of_urls))  

            return a
       
        print('no new job stories from fetch fxn')
        return None


class TypeIsJobChecker:
    def __init__(self, request: APIRequest): 
        self.request = request
    
    def get_only_job_stories(self):
        ne = self.request.fetch_job_posts_with_id()
        if ne:
            only_news = [i for i in ne if i.get('type') == 'job']
            return only_news
        else:
            return None


class PostHasLinkChecker:
    def __init__(self, checker: TypeIsJobChecker): 
        self.checker = checker

    def get_job_posts_with_links(self):
        nw = self.checker.get_only_job_stories()
        if nw:
            only_posts_with_links = [i for i in nw if i.get('url') != '' and i.get('url') != None]
            return only_posts_with_links
        return None


class KeyFinder:
    def __init__(self, checker: PostHasLinkChecker): 
        self.checker = checker

    def get_job_posts_with_select_keys(self, keys):
        ns = self.checker.get_job_posts_with_links()
        if ns:
            b = []
            for i in ns:
                choice_dict = {k: v for k, v in i.items() if k in keys }
                b.append(choice_dict)   
            return b
        else:
            print('No new job posts')
            return None

   
request      = HackerAPIJobsRequest()
type_checker = TypeIsJobChecker(request)
link_checker = PostHasLinkChecker(type_checker)
keyfinder    = KeyFinder(link_checker)






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



if  __name__ == '__main__':

    choice = ["by", "id", "type", "title", "url", "time"]
    keys = keyfinder.get_job_posts_with_select_keys(choice)
    
    print(keys) 