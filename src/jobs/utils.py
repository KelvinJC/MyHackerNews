import requests
import json
from concurrent.futures import ThreadPoolExecutor
from abc import ABC, abstractmethod
from .models import JobArticle


class APIRequest(ABC):
    @abstractmethod
    def fetch_all_job_post_ids():
        pass
    @abstractmethod
    def fetch_job_posts_with_id():
        pass

class HackerAPIJobsRequest(APIRequest):
    __id_url = "https://hacker-news.firebaseio.com/v0/jobstories.json"
    __each_job_story_url = "https://hacker-news.firebaseio.com/v0/item/{}.json"
    def __request(self, url):
        try:
            r = requests.request("GET", url, timeout=120) 
            r_text = json.loads(r.text)
        except ConnectionError as e:  
            print(e)
        return r_text
 
    def fetch_all_job_post_ids(self):
        ids = self.__request(self.__id_url)
        if ids:
            ids_int = [int(i) for i in ids]
            return ids_int
        return None
     
    def find_new_ids(self):
        '''
        Query db to get all past ids
        Compare list of past ids with current request
        Return all new ids or None
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
    def __concurrent_request(self, urls: list):
        '''
        Use multi-threading to make concurrent HTTP requests to a list of urls
        '''     
        with ThreadPoolExecutor(max_workers=50) as pool:
            a = list(pool.map(self.__request, urls))  
        return a
    # Use the obtained ids to fetch each job from the Get item endpoint 
    def fetch_job_posts_with_id(self):
        ''' 
        Use the obtained ids to fetch each story from the Get item endpoint.
        '''
        ids = self.find_new_ids()
        if ids:
            list_of_urls = [self.__each_job_story_url.format(i) for i in ids]
            response = self.__concurrent_request(list_of_urls)
            return response
        print('no new job stories from fetch fxn')
        return None


class Checker(ABC):
    def __init__(self, request: APIRequest): 
        self.request = request
    
    @abstractmethod
    def get_only_job_stories():
        pass
    @abstractmethod
    def get_job_posts_with_links():
        pass

class JobPostChecker(Checker):
    def get_only_job_stories(self):
        ne = self.request.fetch_job_posts_with_id()
        if ne:
            only_news = [i for i in ne if i.get('type') == 'job']
            return only_news
        else:
            return None
    def get_job_posts_with_links(self):
        nw = self.get_only_job_stories()
        if nw:
            only_posts_with_links = [i for i in nw if i.get('url') != '' and i.get('url') != None]
            return only_posts_with_links
        return None

class KeyFinder:
    def __init__(self, checker: Checker): 
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
post_checker = JobPostChecker(request)
keyfinder    = KeyFinder(post_checker)

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