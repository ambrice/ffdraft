import cgi
import urllib2
import httplib
import oauth.oauth as oauth

# ffdraft API keys registered with yahoo developer network
consumer_key='dj0yJmk9b1o2R1k2M3BDUFlqJmQ9WVdrOWNGQnhkMHB5TlRZbWNHbzlNalUzTVRJeE5UWXkmcz1jb25zdW1lcnNlY3JldCZ4PTE4'
consumer_secret='67ccb3a016bfa61e7e159b3936c8700af0b2f630'

token_url='https://api.login.yahoo.com/oauth/v2/get_request_token'
auth_url='https://api.login.yahoo.com/oauth/v2/request_auth'
access_url='https://api.login.yahoo.com/oauth/v2/get_token'

class OAuthWrapper(object):
    def __init__(self, access_token_key=None, access_token_secret=None, session_handle=None):
        self.consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
        self.signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
        if access_token_key and access_token_secret:
            self.access_token = oauth.OAuthToken(access_token_key, access_token_secret) 
        else:
            self.access_token = None
        self.session_handle = session_handle
        self.token_update_callbacks = []

    def add_token_update_callback(self, cb):
        self.token_update_callbacks.append(cb)

    def request(self, url):
        if not self.access_token or not self.session_handle:
            return None
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, self.access_token, http_url=url)
        oauth_request.sign_request(self.signature_method, self.consumer, self.access_token)
        response = None
        try:
            response = urllib2.urlopen(oauth_request.to_url())
        except urllib2.HTTPError as e:
            print 'Received HTTP Error {0}'.format(e.code)
            if e.code == 401:
                self.refresh_access_token()
                oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, self.access_token, http_url=url)
                oauth_request.sign_request(self.signature_method, self.consumer, self.access_token)
                try:
                    response = urllib2.urlopen(oauth_request.to_url())
                except urllib2.HTTPError:
                    pass
        return response.read() if response else None

    def create_access_token(self):
        request_token = self.get_request_token()
        verifier = self.get_user_authorization(request_token)
        self.access_token, self.session_handle = self.get_access_token(self, request_token, verifier)

    def get_request_token(self):
        # Step 1: Get a Request Token
        connection = httplib.HTTPSConnection('api.login.yahoo.com')
        signature_method = oauth.OAuthSignatureMethod_PLAINTEXT()
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, callback='oob', http_url=token_url)
        oauth_request.sign_request(signature_method, self.consumer, None)
        connection.request(oauth_request.http_method, token_url, headers=oauth_request.to_header())
        response = connection.getresponse().read()
        token = oauth.OAuthToken.from_string(response)
        params = cgi.parse_qs(response, keep_blank_values=False)
        token.set_callback(params['xoauth_request_auth_url'][0])
        return token

    def get_user_authorization(self, request_token):
        # Step 2: Get User Authorization
        print('Go to: {0}?oauth_token={1}'.format(auth_url, request_token.key))
        return raw_input('Verification code: ')

    def get_access_token(self, request_token, verifier):
        # Step 3: Exchange Request Token and Verifier for Access Token
        connection = httplib.HTTPSConnection('api.login.yahoo.com')
        signature_method = oauth.OAuthSignatureMethod_PLAINTEXT()
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, request_token, verifier=verifier, http_url=access_url)
        oauth_request.sign_request(signature_method, self.consumer, request_token)
        connection.request(oauth_request.http_method, access_url, headers=oauth_request.to_header())
        response = connection.getresponse().read()
        params = cgi.parse_qs(response, keep_blank_values=False)
        return (oauth.OAuthToken.from_string(response), params['oauth_session_handle'][0])

    def refresh_access_token(self):
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
        for cb in self.token_update_callbacks:
            cb(self.access_token.key, self.access_token.secret, self.session_handle)

if __name__ == "__main__":
    auth = OAuthWrapper()
    token = auth.get_request_token()
    print token.get_callback_url()
