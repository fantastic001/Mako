
class MakoWebService(object):

    """
    This interface represents needed methods which every class has to implement if it wants to be ued 
    in MakoWebServiceDatabase. 

    These classes represent access to OAuth-based web ervices.
    """

    def __init__(self, token=None):
        self.token = token
    
    def getAccessToken(self):
        return self.token

    def getAuthURL(self):
        """
        Returns authentication URL ued in OAuth
        """
        pass

    def login(self, code):
        """
        Returns new access token based on authentication code 
        """
        pass

    def uploadData(self, identifier, data):
        """
        Uploads data given as string
        """
        pass

    def downloadData(self, identifier):
        """
        Downloads data which is found by identifier

        Returns None if there's no data with given identifier.
        """
        pass

