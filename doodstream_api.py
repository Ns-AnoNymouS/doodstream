import aiohttp


class InvalidApiKey(Exception):
    """ This error will be raised
    if an invalid token is passed"""
    
    def __str__(self):
        return "The API key provided by you is invalid."


class DoodStream:
    """ A simple api written according to my convenience"""

    base_url = "https://doodapi.com/api"

    def __init__(self, api_key):
        self.api_key = api_key


    @staticmethod
    async def request(url, params=None):
        """ For calling the http requests

        parameters:
            url (``str``):
                a url path to which get request should be called.

            params (``dict``, *optional*):
                a python dictionary for any additional data that should be passed with get request.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                data = await response.json()
                if data["msg"] in ["Wrong Auth", "Invalid key"]:
                    raise InvalidApiKey
                else:
                    return data


    async def accountInfo(self):
        """ For calling the http requests

        parameters:
            url (``str``):
                a url path to which get request should be called.

            params (``dict``, *optional*):
                a python dictionary for any additional data that should be passed with get request.
        """
        url = f"{self.base_url}/account/info"
        params = {'key': self.api_key}
        return await self.request(url, params)


    ########## Remote Upload ##########

    async def addLink(self, url, folder_id=0, title=''):
        url = f"{self.base_url}/upload/url"
        params = {
            'key': self.api_key,
            'url': url,
            'fld_id': folder_id,
            'new_title': title
        }
        return await self.request(url, params)


    @property
    async def uploadList(self):
        url = f"{self.base_url}/urlupload/list"
        params = {
            'key': self.api_key
        }
        return await self.request(url, params)


    async def uploadStatus(self, file_id):
        url = f"{self.base_url}/urlupload/status"
        params = {
            'key': self.api_key,
            'file_code': file_id
        }
        return await self.request(url, params)


    @property
    async def uploadSlots(self):
        url = f"{self.base_url}/urlupload/slots"
        params = {
            'key': self.api_key
        }
        return await self.request(url, params)

    
    async def uploadAction(self, restart_errors=False, clear_errors=False, clear_all=False, file_id=None):
        url = f"{self.base_url}/urlupload/actions?key={self.api_key}"
        url += "&restart_errors=1" if restart_errors else ''
        url += "&clear_errors=1" if clear_errors else ''
        url += "&clear_all=1" if clear_all else ''
        url += "&delete_code=1" if file_id else ''
        return await self.request(url)


    ########## Manage Folders ##########

    async def createFolder(self, name, parent_id):
        url = f"{self.base_url}/folder/create"
        params = {
            'key': self.api_key,
            'name': name,
            'parent_id': parent_id
        }
        return await self.request(url, params)


    async def renameFolder(self, folder_id, name):
        url = f"{self.base_url}/folder/rename"
        params = {
            'key': self.api_key,
            'fld_id': folder_id,
            'name': name
        }
        return await self.request(url, params)
    

    ########## Manage Files ##########

    async def listFiles(self, page=1, per_page=10, folder_id=0):
        url = f"{self.base_url}/file/list"
        params = {
            'key': self.api_key,
            'page': page,
            'per_page': per_page,
            'fld_id': folder_id
        }
        return await self.request(url, params)
    


    async def getFileStatus(self, file_id):
        url = f"{self.base_url}/file/check"
        params = {
            'key': self.api_key,
            'file_code': file_id
        }
        return await self.request(url, params)


    async def getFileInfo(self, file_id):
        url = f"{self.base_url}/file/info"
        params = {
            'key': self.api_key,
            'file_code': file_id
        }
        return await self.request(url, params)


    async def getFileImage(self, file_id):
        url = f"{self.base_url}/file/image"
        params = {
            'key': self.api_key,
            'file_code': file_id
        }
        return await self.request(url, params)


    async def renameFile(self, file_id, name):
        url = f"{self.base_url}/file/rename"
        params = {
            'key': self.api_key,
            'file_code': file_id,
            'title': name
        }
        return await self.request(url, params)
    

    async def searchFiles(self, query):
        url= f"{self.base_url}/search/videos"
        params = {
            'key': self.api_key,
            'search_term': query
        }
        return await self.request(url, params)
