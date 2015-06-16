from ecrawler.crawler import Crawler
import json
import sys

class Main(object):
    
    def __init__(self):
        self.jsonDict = {}
        self.pending_sites = []
        self.look_up = "a"
        output = self.inputfromuser()
        site_to_crawl = output[0]
        no_of_link = output[1]
        if site_to_crawl:
            if no_of_link:
                try:
                    no_of_link = int(no_of_link)
                    self.preCrawl(site_to_crawl, no_of_link)
                except:
                    print "No of links to be crawled require either blank entry or integer value"
                    sys.exit()
            else:
                self.preCrawl(site_to_crawl)
    
    def inputfromuser(self):
        try:
            site_to_crawl = raw_input("Web to crawl?\n")
            no_of_link = raw_input("No of links to be crawled? leave it blanck for full crawling\n")
        except SyntaxError:
            site_to_crawl = None
            no_of_link = None
        return [site_to_crawl, no_of_link]

    def preCrawl(self, site_to_crawl, no_of_link=None):
        self.pending_sites.append(site_to_crawl)
        count = 0
        print "Crawing Started..."
        if no_of_link != None:
            while count <= no_of_link:
                self.startCrawl()
                count += 1
            print "Crawling completed"
        else:
            while True:
                self.startCrawl()
        

    def startCrawl(self):
        if len(self.pending_sites) != 0:
            site_to_crawl = self.pending_sites.pop(0)
            if site_to_crawl[-1] != '/':
                site_to_crawl = site_to_crawl+"/"
            crawler = Crawler(site_to_crawl, self.look_up)
            crawled_items = crawler.crawl()
            if 'result' in crawled_items:
                self.jsonDict[site_to_crawl] = []
                for anchor in crawled_items['result']:
                    if not ("https://" in anchor or "http://" in anchor):
                        anchor = site_to_crawl + anchor.replace("../", "")
                    self.pending_sites.append(anchor)
                    self.jsonDict[site_to_crawl].append(anchor)
                with open('crawler.json', 'w+b') as crawlerJSONFile:
                    crawlerJSONFile.seek(0)
                    if not crawlerJSONFile.read(1):
                        data = self.jsonDict
                    else:
                        data = json.load(crawlerJSONFile)
                        data[site_to_crawl] = self.jsonDict[site_to_crawl]
                    crawlerJSONFile.write(json.dumps([data], indent=4))
                    print str(len(self.jsonDict[site_to_crawl])) + " url fetched from " + site_to_crawl + " and dumped to crawler.json file"



if __name__ == "__main__":
    Main()


        
