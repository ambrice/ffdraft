import cgi
import urllib2
import httplib
import time
import Queue
import oauth.oauth as oauth
from PyQt4 import QtCore

# ffdraft API keys registered with yahoo developer network
consumer_key='dj0yJmk9b1o2R1k2M3BDUFlqJmQ9WVdrOWNGQnhkMHB5TlRZbWNHbzlNalUzTVRJeE5UWXkmcz1jb25zdW1lcnNlY3JldCZ4PTE4'
consumer_secret='67ccb3a016bfa61e7e159b3936c8700af0b2f630'

token_url='https://api.login.yahoo.com/oauth/v2/get_request_token'
auth_url='https://api.login.yahoo.com/oauth/v2/request_auth'
access_url='https://api.login.yahoo.com/oauth/v2/get_token'

queue = Queue.PriorityQueue()

class RequestThread(QtCore.QThread):
    response_available = QtCore.pyqtSignal(int, QtCore.QByteArray)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

    def run(self):
        while True:
            (priority, request_id, url) = queue.get()
            try:
                response = urllib2.urlopen(url)
            except:
                print 'Error loading url {0}'.format(url)
                raise
            self.response_available.emit(request_id, QtCore.QByteArray(response.read()))
            queue.task_done()

class OAuthWrapper(QtCore.QObject):
    def __init__(self, access_token_key=None, access_token_secret=None, session_handle=None, access_expires=None):
        QtCore.QObject.__init__(self)
        self.consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
        self.signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
        self.set_access(access_token_key, access_token_secret, session_handle, access_expires)
        self.token_update_callbacks = []
        self.request_threads = []
        # 5 worker threads
        for i in xrange(5):
            thread = RequestThread()
            thread.response_available.connect(self.handle_response)
            thread.start()
            self.request_threads.append(thread)
        self.request_id = 0
        self.callback_map = {}

    def set_access(self, access_token_key, access_token_secret, session_handle, access_expires):
        if access_token_key and access_token_secret:
            self.access_token = oauth.OAuthToken(access_token_key, access_token_secret) 
        else:
            self.access_token = None
        self.session_handle = session_handle
        self.access_expires = access_expires

    def add_token_update_callback(self, cb):
        self.token_update_callbacks.append(cb)

    def request(self, url, skip_auth=False):
        if not skip_auth and (not self.access_token or not self.session_handle):
            raise RuntimeError('OAuth Request made without access token')
        if time.time() > self.access_expires:
            self.refresh_access_token()
        if not skip_auth:
            oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, self.access_token, http_url=url)
            oauth_request.sign_request(self.signature_method, self.consumer, self.access_token)
            url = oauth_request.to_url()
        response = urllib2.urlopen(url)
        return response.read()

    def request_async(self, url, callback, priority=3, skip_auth=False):
        if not skip_auth and (not self.access_token or not self.session_handle):
            return None
        if time.time() > self.access_expires:
            self.refresh_access_token()
        if not skip_auth:
            oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, self.access_token, http_url=url)
            oauth_request.sign_request(self.signature_method, self.consumer, self.access_token)
            url = oauth_request.to_url()
        self.callback_map[self.request_id] = callback
        queue.put( (priority, self.request_id, url) )
        self.request_id += 1

    @QtCore.pyqtSlot(int, QtCore.QByteArray)
    def handle_response(self, request_id, response):
        if request_id in self.callback_map and response:
            self.callback_map[request_id](response)
            del self.callback_map[request_id]

    def create_access_token(self):
        request_token = self.get_request_token()
        verifier = self.get_user_authorization(request_token)
        self.access_token, self.session_handle, self.access_expires  = self.get_access_token(self, request_token, verifier)

    def get_request_token(self):
        # Step 1: Get a Request Token
        connection = httplib.HTTPSConnection('api.login.yahoo.com')
        # Using PLAINTEXT instead of HMAC_SHA1 because yahoo has a bug where they return the wrong error codes for HMAC_SHA1, and it's https 
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
        request_time = int(time.time())
        connection.request(oauth_request.http_method, access_url, headers=oauth_request.to_header())
        response = connection.getresponse().read()
        params = cgi.parse_qs(response, keep_blank_values=False)
        expire_time = request_time + int(params['oauth_expires_in'][0])
        return (oauth.OAuthToken.from_string(response), params['oauth_session_handle'][0], expire_time)

    def refresh_access_token(self):
        connection = httplib.HTTPSConnection('api.login.yahoo.com')
        signature_method = oauth.OAuthSignatureMethod_PLAINTEXT()
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, self.access_token, http_url=access_url)
        oauth_request.set_parameter('oauth_session_handle', self.session_handle)
        oauth_request.sign_request(signature_method, self.consumer, self.access_token)
        request_time = int(time.time())
        connection.request(oauth_request.http_method, access_url, headers=oauth_request.to_header())
        response = connection.getresponse().read()
        params = cgi.parse_qs(response, keep_blank_values=False)
        self.session_handle = params['oauth_session_handle'][0]
        # Adding a 1 minute fudge factor to avoid race condition, I'm not sure how this expiration thing works.  What
        # if I send a valid token at the time the request is made but it expires before yahoo processes it?
        self.access_expires = request_time + int(params['oauth_expires_in'][0]) - 60
        self.access_token = oauth.OAuthToken.from_string(response)
        for cb in self.token_update_callbacks:
            cb(self.access_token.key, self.access_token.secret, self.session_handle, self.access_expires)

if __name__ == "__main__":
    auth = OAuthWrapper()
    token = auth.get_request_token()
    print token.get_callback_url()
