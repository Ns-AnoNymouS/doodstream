import aiohttp


class InvalidApiKey(Exception):
    """ This error will be raised
    if an invalid token is passed"""
    
    def __str__(self):
        return "The API key provided by you is invalid."


class DoodStream:
    """ An unofficial asynchronous DoodStream API written in python.
    
    parameters:
        api_key (``str``):
            your doodstream api you can get this from https://doodstream.com/settings.
    """

    base_url = "https://doodapi.com/api"

    def __init__(self, api_key: str):
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

        Example:
            .. code-block:: python
                doodstream = DoodStream(api_key='34095e0kjrczf7fav728b')
                account_info = await doodstream.accountInfo()
                print(account_info)

        Output:
            {
                "msg": "OK",
                "server_time": "2017-08-11 04:30:07",
                "status": 200,
                "result": {
                    "email": "email@test.com",
                    "balance": "0.00000",
                    "storage_used" :"24186265",
                    "storage_left": 128824832615,
                    "premim_expire": "2025-10-24 21:00:00
                }
            }
        """

        url = f"{self.base_url}/account/info"
        params = {'key': self.api_key}
        return await self.request(url, params)


    ########## Remote Upload ##########

    async def addLink(self, url: str, folder_id: str = 0, title: str = ''):
        """ Add remote upload link

        parameters:
            url (``str``):
                a url path which should be added to upload queue.

            folder_id (``str``, *optional*):
                specify a folder id to upload file in specific folder. 

            title (``str``, *optional*):
                add this if you want to specify the file name
    

        Example:
            .. code-block:: python
                doodstream = DoodStream(api_key='34095e0kjrczf7fav728b')
                status = await doodstream.addLink('https://dropbox.com/hukbasd7k3fd')
                print(status)
        
        Output:
            {
                "msg": "OK",
                "server_time": "2017-08-11 04:30:07",
                "new_title": "",
                "status": 200,
                "total_slots": "100",
                "result": {
                    "filecode": "98zukoh5jqiw"
                },
                "used_slots": "0"
            }
        """

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
        """Get remote upload list

        Example:
            .. code-block:: python
                doodstream = DoodStream(api_key='34095e0kjrczf7fav728b')
                status = await doodstream.uploadList
                print(status)
        
        Output:
            {
                "msg": "OK",
                "server_time": "2017-08-11 04:30:07",
                "status": 200,
                "result": [
                    {
                        "bytes_total": "0",
                        "created": "2017-08-11 04:30:07",
                        "remote_url": "https://dropbox.com/hukbasd7k3fd",
                        "status": "working",
                        "file_code": "98zukoh5jqiw",
                        "bytes_downloaded": "0",
                        "folder_id": "0"
                    }
                ]
            }
        """

        url = f"{self.base_url}/urlupload/list"
        params = {
            'key': self.api_key
        }
        return await self.request(url, params)


    async def uploadStatus(self, file_id: str):
        """"Get remote upload status of a specific file

        parameters:
            file_id (``str``):
                a specific fileid to get the remote upload status.

        Example:
            .. code-block:: python
                doodstream = DoodStream(api_key='34095e0kjrczf7fav728b')
                status = await doodstream.uploadStatus('hjsnr087johj')
                print(status)
        
        Output:
            {
                "msg": "OK",
                "server_time": "2017-08-11 04:30:07",
                "status": 200,
                "result": [{
                    "bytes_total": "0",
                    "created": "2017-08-11 04:30:07",
                    "remote_url": "https://dropbox.com/hukbasd7k3fd",
                    "status": "working",
                    "file_code": "hjsnr087johj",
                    "bytes_downloaded": "0",
                    "folder_id": "0"
                }]
            }
        """

        url = f"{self.base_url}/urlupload/status"
        params = {
            'key': self.api_key,
            'file_code': file_id
        }
        return await self.request(url, params)


    @property
    async def uploadSlots(self):
        """Get remote upload status of a specific file

        Example:
            .. code-block:: python
                doodstream = DoodStream(api_key='34095e0kjrczf7fav728b')
                slots = await doodstream.uploadSlots
                print(slots)
        
        Output:
            {
                "msg": "OK",
                "server_time": "2017-08-11 04:30:07",
                "status": 200,
                "total_slots": "100",
                "used_slots": "10"
            }
        """

        url = f"{self.base_url}/urlupload/slots"
        params = {
            'key': self.api_key
        }
        return await self.request(url, params)

    
    async def uploadAction(
        self, 
        restart_errors: bool = False, 
        clear_errors: bool = False, 
        clear_all: bool = False, 
        file_id: str = None
    ):
        """Get remote upload status of a specific file

        parameters:
            restart_errors (``bool``, *optional*):
                set this to True to restart all errors
            
            clear_errors (``bool``, *optional*):
                set this to True to clear all errors

            clear_all (``bool``, *optional*):
                set this to True to clear all
            
            file_id (``bool``, *optional):
                pass a file id to clear the specified one

        Example:
            .. code-block:: python
                doodstream = DoodStream(api_key='34095e0kjrczf7fav728b')
                slots = await doodstream.uploadAction()
                print(slots)
        
        Output:
            {
                "msg": "Errors restarted",
                "server_time": "2017-08-11 04:30:07",
                "status": 200
            }
        """

        url = f"{self.base_url}/urlupload/actions?key={self.api_key}"
        url += "&restart_errors=1" if restart_errors else ''
        url += "&clear_errors=1" if clear_errors else ''
        url += "&clear_all=1" if clear_all else ''
        url += "&delete_code=1" if file_id else ''
        return await self.request(url)


    ########## Manage Folders ##########

    async def createFolder(self, name: str, parent_id: str = None):
        """Create a new folder

        parameters:
            name (``str``):
                the name of folder that should be created
            
            parent_id (``str``, *optional*):
                pass a parent id to create folder in that

        Example:
            .. code-block:: python
                doodstream = DoodStream(api_key='34095e0kjrczf7fav728b')
                sts = await doodstream.createFolder('New Folder')
                print(sts)
        
        Output:
            {
                "msg": "OK",
                "server_time": "2017-08-11 04:30:07",
                "status": 200,
                "result": {
                    "fld_id": "1234567"
                }
            }
        """

        url = f"{self.base_url}/folder/create?key={self.api_key}&name={name}"
        if parent_id:
            url += f'&parent_id={parent_id}'
        return await self.request(url, params)


    async def renameFolder(self, folder_id: str, name: str):
        """rename folder

        parameters:
            name (``str``):
                the name of folder that should be created
            
            folder_id (``str``):
                id of the folder that you need to rename

            name (``str``):
                pass the new folder name

        Example:
            .. code-block:: python
                doodstream = DoodStream(api_key='34095e0kjrczf7fav728b')
                sts = await doodstream.createFolder('New Folder')
                print(sts)
        
        Output:
            {
                "msg": "OK",
                "server_time": "2017-08-11 04:30:07",
                "status": 200,
                "result": "true"
            }
        """
        url = f"{self.base_url}/folder/rename"
        params = {
            'key': self.api_key,
            'fld_id': folder_id,
            'name': name
        }
        return await self.request(url, params)
    

    ########## Manage Files ##########

    async def listFiles(self, page=1, per_page=10, folder_id=0):
        """Create a new folder

        parameters:
            name (``str``):
                the name of folder that should be created
            
            parent_id (``str``, *optional*):
                pass a parent id to create folder in that

        Example:
            .. code-block:: python
                doodstream = DoodStream(api_key='34095e0kjrczf7fav728b')
                sts = await doodstream.createFolder('New Folder')
                print(sts)
        
        Output:
            {
                "msg": "OK",
                "server_time": "2017-08-11 04:30:07",
                "status": 200,
                "result": {
                    "fld_id": "1234567"
                }
            }
        """
        url = f"{self.base_url}/file/list"
        params = {
            'key': self.api_key,
            'page': page,
            'per_page': per_page,
            'fld_id': folder_id
        }
        return await self.request(url, params)
    


    async def getFileStatus(self, file_id):
        """Create a new folder

        parameters:
            name (``str``):
                the name of folder that should be created
            
            parent_id (``str``, *optional*):
                pass a parent id to create folder in that

        Example:
            .. code-block:: python
                doodstream = DoodStream(api_key='34095e0kjrczf7fav728b')
                sts = await doodstream.createFolder('New Folder')
                print(sts)
        
        Output:
            {
                "msg": "OK",
                "server_time": "2017-08-11 04:30:07",
                "status": 200,
                "result": {
                    "fld_id": "1234567"
                }
            }
        """
        url = f"{self.base_url}/file/check"
        params = {
            'key': self.api_key,
            'file_code': file_id
        }
        return await self.request(url, params)


    async def getFileInfo(self, file_id):
                """Create a new folder

        parameters:
            name (``str``):
                the name of folder that should be created
            
            parent_id (``str``, *optional*):
                pass a parent id to create folder in that

        Example:
            .. code-block:: python
                doodstream = DoodStream(api_key='34095e0kjrczf7fav728b')
                sts = await doodstream.createFolder('New Folder')
                print(sts)
        
        Output:
            {
                "msg": "OK",
                "server_time": "2017-08-11 04:30:07",
                "status": 200,
                "result": {
                    "fld_id": "1234567"
                }
            }
        """
        url = f"{self.base_url}/file/info"
        params = {
            'key': self.api_key,
            'file_code': file_id
        }
        return await self.request(url, params)


    async def getFileImage(self, file_id):
        """Create a new folder

        parameters:
            name (``str``):
                the name of folder that should be created
            
            parent_id (``str``, *optional*):
                pass a parent id to create folder in that

        Example:
            .. code-block:: python
                doodstream = DoodStream(api_key='34095e0kjrczf7fav728b')
                sts = await doodstream.createFolder('New Folder')
                print(sts)
        
        Output:
            {
                "msg": "OK",
                "server_time": "2017-08-11 04:30:07",
                "status": 200,
                "result": {
                    "fld_id": "1234567"
                }
            }
        """
        url = f"{self.base_url}/file/image"
        params = {
            'key': self.api_key,
            'file_code': file_id
        }
        return await self.request(url, params)


    async def renameFile(self, file_id, name):
        """Create a new folder

        parameters:
            name (``str``):
                the name of folder that should be created
            
            parent_id (``str``, *optional*):
                pass a parent id to create folder in that

        Example:
            .. code-block:: python
                doodstream = DoodStream(api_key='34095e0kjrczf7fav728b')
                sts = await doodstream.createFolder('New Folder')
                print(sts)
        
        Output:
            {
                "msg": "OK",
                "server_time": "2017-08-11 04:30:07",
                "status": 200,
                "result": {
                    "fld_id": "1234567"
                }
            }
        """
        url = f"{self.base_url}/file/rename"
        params = {
            'key': self.api_key,
            'file_code': file_id,
            'title': name
        }
        return await self.request(url, params)
    

    async def searchFiles(self, query):
        """Create a new folder

        parameters:
            name (``str``):
                the name of folder that should be created
            
            parent_id (``str``, *optional*):
                pass a parent id to create folder in that

        Example:
            .. code-block:: python
                doodstream = DoodStream(api_key='34095e0kjrczf7fav728b')
                sts = await doodstream.createFolder('New Folder')
                print(sts)
        
        Output:
            {
                "msg": "OK",
                "server_time": "2017-08-11 04:30:07",
                "status": 200,
                "result": {
                    "fld_id": "1234567"
                }
            }
        """
        url= f"{self.base_url}/search/videos"
        params = {
            'key': self.api_key,
            'search_term': query
        }
        return await self.request(url, params)