"""
    @file: instagram.py
    @author: spencer
    @Date: 4/23/2019
    @Description: Instagram wrapper for social engagement tech.
    Helps with companies, individuals social presence online. 

"""

import requests
import json


class Instagram:
    BASE = 'https://www.instagram.com/'
    header = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; '
                      'Nexus 5 Build/MRA58N) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/46.0.2490.76 Mobile Safari/537.36',
    }

    def __init__(self):
        self.session = False

    def login(self, username, password): 
        """
            login(username, password) -> session
        """
        # Create session
        session = requests.Session()

        # Capture response headers for site
        session.headers.update(self.header)

        # Use the session to HTTP GET requested site data , handshake with site
        req = session.get('https://www.instagram.com/')

        # Add required headers to HTTP header
        session.headers.update({'x-csrftoken': req.cookies['csrftoken']})

        # Post account credentials to login script
        res = session.post('https://www.instagram.com/accounts/login/ajax/',
                           data={'username': username, 'password': password})

        # Check http request response status codes
        if res.status_code == 200:
            auth = json.loads(res.text)

            # Check for True authenticated status
            if auth['authenticated']:
                print("Successful login.")

                session.headers.update({'x-csrftoken': res.cookies['csrftoken']})
                self.session = session

            elif auth['authenticated'] is False:
                print("AUTHENTICATION IS FALSE")
                return False
        else:
            print("Response Error Status Code {0}".format(res.status_code))
            print(res.status_code)
            return False

    def explore_tags(self, tag):
        results = []
        raw = self.session.request('GET',
                                   self.BASE + 'explore/tags/{0}/?__a=1'.format(tag))

        media = json.loads(raw.text)
        for node in media['graphql']['hashtag']['edge_hashtag_to_top_posts']['edges']:
            results.append(InstagramMediaPost(node['node']))
        return results

class InstagramMediaPost:
    def __init__(self, node):
        self.node = node
    
    @property
    def id(self):
        return self.node['id']
    
    @property
    def caption(self): # load all possible captions .ig - caption returns a list[]
        return [text['node']['text'] for text in self.node['edge_media_to_caption']['edges']]

    @property
    def shortcode(self):
        return self.node['shortcode']
    
    @property
    def displayUrl(self):
        return self.node['display_url']

    @property
    def likedBy(self):
        return self.node['edge_liked_by']

    @property
    def owner(self):
        return self.node['owner']['id']

    @property
    def isVideo(self):
        return self.node['is_video']

    def __str__(self):
        return self.id

    