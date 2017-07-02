

from .MakoWebService import * 

import dropbox

import random

class MakoDropboxWebService(MakoWebService):
    
    APP_KEY = "psav4u6w4erjyjn"
    APP_SECRET = "2i9nu38xax4hkqy"

    def getAuthURL(self):
        """
        Returns authentication URL ued in OAuth
        """
        self.flow = dropbox.DropboxOAuth2FlowNoRedirect(self.APP_KEY, self.APP_SECRET)
        authorize_url = self.flow.start()
        return authorize_url

    def login(self, code):
        """
        Returns new access token based on authentication code 
        """
        access_token = self.flow.finish(code).access_token
        return access_token

    def uploadData(self, identifier, data):
        """
        Uploads data given as string
        """
        access_token = self.getAccessToken()
        client = dropbox.Dropbox(access_token)
        name = "/tmp/mako_temp_file-%d" % int(random.random()*100000)
        f = open(name, "w")
        f.write(data)
        f.close()
        f = open(name, "rb")
        client.files_alpha_upload(f.read(), "/" + identifier)
        f.close()

    def downloadData(self, identifier):
        """
        Downloads data which is found by identifier

        Returns None if there's no data with given identifier.
        """
        access_token = self.getAccessToken()
        client = dropbox.Dropbox(access_token)
        try:
            f,r = client.files_download("/%s" % identifier)
            return r.text
        except dropbox.exceptions.ApiError:
            return None
