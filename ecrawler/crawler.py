from bs4 import BeautifulSoup
import urllib2

class Crawler(object):
    def __init__(self, site_to_crawl, look_up):
        self.site_to_crawl = site_to_crawl
        self.look_up = look_up
        self.output = {}

    def __repr__(self):
        return self.output

    def crawl(self):
        self.parseAddress()
        test_output = self.test_site_to_crawl()
        if test_output != "Success":
            self.output["error"] = test_output
        if not "error" in self.output:
            website = urllib2.urlopen(self.site_to_crawl)
            soup = BeautifulSoup(website)
            lu = soup.find_all(self.look_up)
            urls = [lookup.get('href', '/') for lookup in lu]
            self.output["result"] = urls
        return self.output

    def parseAddress(self):
        input = self.site_to_crawl
        if not ("https://" in input or "http://" in input):
            if input.find("://") != -1:
                self.output["error"] = "Error: Cannot retrive URL, address must be HTTP"
            else:
                self.site_to_crawl = "http://" + input

    def test_site_to_crawl(self):
        try:
            urllib2.urlopen(self.site_to_crawl)
            return "Success"
        except urllib2.HTTPError, e:
            return "Cannot retrieve URL: HTTP Error Code", e.code
        except urllib2.URLError, e:
            return "Cannot retrieve URL: " + e.reason[1]
        except:
            return "Cannot retrieve URL: unknown error"