import requests, re

class LinkValidator():

    def __init__(self,domain,paths=[]):
        self.domain=domain
        self.paths=paths

    def can_follow_link(self,url):
        if not url.startswith(self.domain):
            return False
        else:
            for path in self.paths:
                if re.match(re.escape(self.domain)+re.escape(path),url):
                    return False
        return True
    
def parse_robots(domain_name):
    """Returns the list of paths to exclude from domain_name's robots.txt file."""
    true_domain="https://"+domain_name.split('/')[2]
    website=requests.get(true_domain+'/robots.txt')
    return re.findall(r"Disallow: (.+)\n",website.text)

if __name__=='__main__':
    # Tests
    forbidden=parse_robots("https://cs111.byu.edu/proj/proj4/assets/page1.html")
    tester=LinkValidator(
        'https://cs111.byu.edu/proj/proj4/assets/page1.html',
        forbidden)
    print(tester.can_follow_link('https://cs111.byu.edu/proj/proj4/assets/page3.html'))