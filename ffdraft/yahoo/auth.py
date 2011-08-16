import cgi
import urllib2
import httplib
import os
import time
import oauth.oauth as oauth

# ffdraft API keys registered with yahoo developer network
consumer_key='dj0yJmk9b1o2R1k2M3BDUFlqJmQ9WVdrOWNGQnhkMHB5TlRZbWNHbzlNalUzTVRJeE5UWXkmcz1jb25zdW1lcnNlY3JldCZ4PTE4'
consumer_secret='67ccb3a016bfa61e7e159b3936c8700af0b2f630'

token_url='https://api.login.yahoo.com/oauth/v2/get_request_token'
auth_url='https://api.login.yahoo.com/oauth/v2/request_auth'
access_url='https://api.login.yahoo.com/oauth/v2/get_token'

class OAuthWrapper(object):
    def __init__(self):
        self.consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
        self.signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
        self.update_access_token()

    def request(self, url):
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, self.access_token, http_url=url)
        oauth_request.sign_request(self.signature_method, self.consumer, self.access_token)
        response = urllib2.urlopen(oauth_request.to_url())
        return response

    def get_access_token(self):
        connection = httplib.HTTPSConnection('api.login.yahoo.com')
        signature_method = oauth.OAuthSignatureMethod_PLAINTEXT()
        # Step 1: Get a Request Token
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, callback='oob', http_url=token_url)
        oauth_request.sign_request(signature_method, self.consumer, None)
        connection.request(oauth_request.http_method, token_url, headers=oauth_request.to_header())
        response = connection.getresponse().read()
        request_token = oauth.OAuthToken.from_string(response)
        # Step 2: Get User Authorization
        print('Go to: {0}?oauth_token={1}'.format(auth_url, request_token.key))
        verifier = raw_input('Verification code: ')
        # Step 3: Exchange Request Token and Verifier for Access Token
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, request_token, verifier=verifier, http_url=access_url)
        oauth_request.sign_request(signature_method, self.consumer, request_token)
        connection.request(oauth_request.http_method, access_url, headers=oauth_request.to_header())
        response = connection.getresponse().read()
        params = cgi.parse_qs(response, keep_blank_values=False)
        self.session_handle = params['oauth_session_handle'][0]
        self.access_token = oauth.OAuthToken.from_string(response)

    def refresh_access_token(self):
        print('Refreshing access token...')
        connection = httplib.HTTPSConnection('api.login.yahoo.com')
        signature_method = oauth.OAuthSignatureMethod_PLAINTEXT()
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, self.access_token, http_url=access_url)
        oauth_request.set_parameter('oauth_session_handle', self.session_handle)
        oauth_request.sign_request(signature_method, self.consumer, self.access_token)
        connection.request(oauth_request.http_method, access_url, headers=oauth_request.to_header())
        response = connection.getresponse().read()
        params = cgi.parse_qs(response, keep_blank_values=False)
        self.session_handle = params['oauth_session_handle'][0]
        self.access_token = oauth.OAuthToken.from_string(response)
    
    def store_access_token(self, keypath):
        with open(keypath, 'w') as f:
            f.write('{0}\n'.format(self.access_token.key))
            f.write('{0}\n'.format(self.access_token.secret))
            f.write('{0}\n'.format(self.session_handle))

    def update_access_token(self):
        keypath='{0}/.ffdraft'.format(os.getenv('HOME'))
        try:
            with open(keypath, 'r') as f:
                key = f.readline().rstrip()
                secret = f.readline().rstrip()
                self.session_handle = f.readline().rstrip()
                self.access_token = oauth.OAuthToken(key, secret)
            if time.time() - os.path.getmtime(keypath) > 3000:
                self.refresh_access_token()
                self.store_access_token(keypath)
        except(IOError, OSError):
            self.get_access_token()
            self.store_access_token(keypath)


