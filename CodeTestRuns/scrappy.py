import logging
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup


# logging.basicConfig(
#     format='%(asctime)s %(levelname)s:%(message)s',
#     level=logging.INFO)

class Crawler:

    def __init__(self, urls): #Urls is an array with starting point of url
        self.visited_urls = []
        self.urls_to_visit = urls
        self.ignoredLinks = ['https://www.bundesarchiv.de/DE/Navigation/'] #Limiting the sub url crawl with 1 more more root url
        self.blackListedUrls=  ['https://www.bundesarchiv.de/','http://www.bundesarchiv.de/']#Urls or sub urls of domain we dont want to crawl
        self.allowedDomains = ['www.bundesarchiv.de'] #Keeps us away from social media links
        self.url_Invalid = []
  
    def JoinUrl(self,subUrl, currUrl):
        # print("BaseURL",baseUrl)
        # print("SubUrl",subUrl)
        return urljoin(currUrl,subUrl)

    def isListPartOfIgnoreLinks(self,urlToCheck):
            resp = False
            if urlToCheck != None:
                for item in self.ignoredLinks:
                    if item in urlToCheck :
                        resp =True
            print('isListPartOfIgnoreLinks()-' + str(urlToCheck)+ ". Allowed ?: "+ str(resp))#print only if ignored
            return resp
    def IsBlackListedUrl(self,urlTovalidate):
        for urls in self.blackListedUrls:
            if urlTovalidate.removesuffix("/") == urls.removesuffix("/"):
                print("Url is blacklisted: "+ urlTovalidate)    
                return True
        return False
    
    #validates if the the url to crawl is what we want,we do not wanted to wander
    def WithinCurrentDomain(self,urlDomain):
        urlDomain= urlparse(urlDomain).netloc
        for domain in self.allowedDomains:
            if urlDomain == domain:
                return True
        print("Domain is not part of allowed list: "+ str(urlDomain)    )
        return False


    def download_url(self, url):
        return requests.get(url).text

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path != None and  path.startswith('#') == False: #path.startswith('/') and
                logging.info(f'get_linked_urls() - valid path: {path}')
                path = urljoin(url, path)
                yield path
            else:
                logging.info(f'get_linked_urls() - invalid path: {path}')

    
    def add_url_to_visit(self, url):
        if url != None and url not in self.visited_urls and url not in self.urls_to_visit and url not in self.url_Invalid and self.WithinCurrentDomain(url) and self.isListPartOfIgnoreLinks(url) == False and self.IsBlackListedUrl(url) == False:
            self.urls_to_visit.append(url)
        elif url != None and self.WithinCurrentDomain(url) == False or  self.isListPartOfIgnoreLinks(url) == False or  self.IsBlackListedUrl(url) == False and url not in self.url_Invalid: #not already in invalid url
            self.url_Invalid.append(url)

    def crawl(self, currUrl):
        html = self.download_url(currUrl)
        for subUrl in self.get_linked_urls(currUrl, html):
            logging.info(f'crawl() - Sub Url: {subUrl}')
            self.add_url_to_visit(subUrl)

    async def run(self):
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            logging.info(f'Run() - Url to Crawl: {url}')
            try:
                self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)

if __name__ == '__main__':
    logging.info('Initiating Main function')
    Crawler(urls=['https://www.bundesarchiv.de/cocoon/barch/0000/index.html']).run()
