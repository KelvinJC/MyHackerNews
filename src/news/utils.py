import requests
import json
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor

from .models import NewsArticle

class APIRequest(ABC):
    @abstractmethod
    def fetch_all_story_ids(self):
        pass

class HackerAPINewsRequest(APIRequest):
    id_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    each_story_url = "https://hacker-news.firebaseio.com/v0/item/{}.json"

    def fetch_all_story_ids(self):
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
        request_ids = self.fetch_all_story_ids()
        print(request_ids)
        old_ids = NewsArticle.objects.values_list('api_id', flat=True)
        print('old_ids', old_ids)
        new_ids = list(set(request_ids) - set(old_ids))
        print('new ids', new_ids)
        if new_ids:
            return new_ids
        return None

    def fetch_story_with_id(self, ids):
        ''' Uses the obtained ids to fetch each story from the Get item endpoint.
            Uses multi-threading to make concurrent HTTP requests to external api'''
        def get_url(url):
            return json.loads(requests.get(url).text)

        if ids:
            list_of_urls = [self.each_story_url.format(i) for i in ids]
            
            with ThreadPoolExecutor(max_workers=50) as pool:
                a = list(pool.map(get_url, list_of_urls))  
            return a
        print('no new stories from fetch fxn')
        return None

class KeyFinder():
    def __init__(self, request: APIRequest): 
        self.request = request
    
    def remove_non_news(self):
        news = self.request.fetch_story_with_id(self.request.find_new_ids())
        if news:
            only_news = [i for i in news if i.get('type') == 'story']
            return only_news
        else:
            return None

    def get_stories_with_select_keys(self, keys):
        new_stories = self.remove_non_news()
        if new_stories:
            b = []
            for i in new_stories:
                choice_dict = {k: v for k, v in i.items() if k in keys }
                b.append(choice_dict)   
            return b
        else:
            print('No new stories')
            return None
    
request = HackerAPINewsRequest()
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

"""
 
<!-- A little Javascript to help in clickingthrough pages in a search --> 

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
    r = HackerAPINewsRequest()
    a = r.get_stories_with_select_keys()  
    print(a) 