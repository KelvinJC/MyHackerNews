import requests
import json
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import ConnectionError

from .models import NewsArticle

class APIRequest(ABC):
    @abstractmethod
    def fetch_all_story_ids(self):
        pass

class HackerAPINewsRequest(APIRequest):
    __id_url         = "https://hacker-news.firebaseio.com/v0/topstories.json"
    __each_story_url = "https://hacker-news.firebaseio.com/v0/item/{}.json"

    
    def __request(self, url):
        try:
            r = requests.request("GET", url, timeout=120) 
            r_text = json.loads(r.text)
        except ConnectionError as e:  
            print(e)
        return r_text
        
    def fetch_all_story_ids(self):
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
        request_ids = self.fetch_all_story_ids()
        print(request_ids)
        old_ids = NewsArticle.objects.values_list('api_id', flat=True)
        print('old_ids', old_ids)
        new_ids = list(set(request_ids) - set(old_ids))
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

    def fetch_story_with_id(self):
        ''' 
        Use the obtained ids to fetch each story from the Get item endpoint.
        '''
        ids = self.find_new_ids()
        if ids:
            list_of_urls = [self.__each_story_url.format(i) for i in ids]
            response = self.__concurrent_request(list_of_urls)
            return response
        print('no new stories from fetch fxn')
        return None


class TypeIsStoryChecker:
    def __init__(self, request: APIRequest): 
        self.request = request
    
    def get_only_news_stories(self):
        ne = self.request.fetch_story_with_id()
        if ne:
            only_news = [i for i in ne if i.get('type') == 'story']
            return only_news
        else:
            return None


class StoryHasLinkChecker:
    def __init__(self, checker: TypeIsStoryChecker): 
        self.checker = checker

    def get_news_with_links(self):
        nw = self.checker.get_only_news_stories()
        if nw:
            only_news_with_links = [i for i in nw if i.get('url') != '' and i.get('url') != None]
            # news_without_links = [x for x in nw if x not in only_news_with_links] # what to do with news posts without links? Make a just-headlines feature?
            # print('those without', news_without_links)
            return only_news_with_links
        return None


class KeyFinder:
    def __init__(self, checker: StoryHasLinkChecker): 
        self.checker = checker

    def get_stories_with_select_keys(self, keys):
        ns = self.checker.get_news_with_links()
        if ns:
            b = []
            for i in ns:
                choice_dict = {k: v for k, v in i.items() if k in keys }
                b.append(choice_dict)   
            return b
        else:
            print('No new stories')
            return None
    
request      = HackerAPINewsRequest()
type_checker = TypeIsStoryChecker(request)
link_checker = StoryHasLinkChecker(type_checker)
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

"""
 
<!-- A little Javascript to help in clicking through pages in a search --> 

<script type="text/javascript">
    // Get search form and page links
    let searchForm = document.getElementById('searchForm')
    let pageLinks = document.getElementsByClassName('page-link')

    // Ensure search form exists
    if (searchForm) {
        for(let i=0; pageLinks.length > i; i++) {
            pageLinks[i].addEventListener('click', function (e) {
                e.preventDefault()

                // get the data attribute
                let page = this.dataset.page
                // Add hidden input to form
                searchForm.innerHTML += `<input value=${page} name="page" hidden/>`

                // Submit form
                searchForm.submit()
            })
        }
    }
</script>
 """       
            
        
# Note:
# Each response is a dictionary sample below

"""
["by", "id", "title", "url", "time"]
            '{
                "by":"aloukissas",
                "descendants":14,
                "id":32907234,
                "kids":[
                    32908166,
                    32908375,
                    32908246,
                    32908162,
                    32907804,
                    32907949,
                    32907547
                    ],
                "score":110,
                "time":1663643639,
                "title":"Cache Your CORS",
                "type":"story",
                "url":"https://httptoolkit.tech/blog/cache-your-cors/"
            }'

"""

if  __name__ == '__main__':

    choice = ["by", "id", "type", "title", "url", "time"]
    keys = keyfinder.get_stories_with_select_keys(choice)
    
    print(keys) 


