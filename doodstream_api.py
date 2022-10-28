import aiohttp


class InvalidApiKey(Exception):
    """ This error will be raised
    if an invalid api key was passed
    """

    def __str__(self):
        return "The API key provided by you is invalid."


class ApiKeyExpired(Exception):
    """ This error will be raised
    if an api key expired"""
    
    def __str__(self):
        return "The API key provided by you is expired."


class DoodStream:
    """ An unofficial asynchronous DoodStream API written in python.
    
    parameters:
        api_key (``str``, *optional*):
            your doodstream api you can get this from https://doodstream.com/settings.
        cookies (``str``, *optional*):
            you cookes returened by login method.
    """

    base_url = "https://doodapi.com/api"
    base_url2 = "https://doodstream.com"

    def __init__(self, api_key: str = None, cookies: str = None):
        self.api_key = api_key
        self.cookies = cookies


    @staticmethod
    async def request(url, params=None):
        """ For calling the http requests

        parameters:
            url (``str``):
                a url path to which get request should be called.

            params (``dict``, *optional*):
                a python dictionary for any additional data that should be passed with get request.
            
            json (``bool``, *optioal*):
                pass False to get response back else you will get a json file
        """

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if 'text/html' in response.content_type:
                    return await response.text()
                data = await response.json()
                if 'msg' in data and data["msg"] in ["Wrong Auth", "Invalid key"]:
                    raise InvalidApiKey
                elif 'status' in data and data['status'] == 403:
                    raise ApiKeyExpired
                else:
                    return data


    async def login(self, username: str, password: str, otp: int = ''):
        """ get the required cookies

        parameters:
            username (``str``):
                username or email of you doodstream account.

            password (``str``):
                password of the doodstream.

            otp (``int`` *optional*):
                otp if sent.
        """

        url = f"{self.base_url2}/"
        params = {
            'op':'login_ajax',
            'login': username,
            'password': password, 
            'loginotp': otp,
            'g-recaptcha-response': ''
        }
        data = await self.request(url, params)
        print(data, type(data))



    async def accountInfo(self):
        """ For calling the http requests

        Example:
            .. code-block:: python
                doodstream = DoodStream(api_key='34095x0xxxxxx7xxx728x')
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
                doodstream = DoodStream(api_key='34095x0xxxxxx7xxx728x')
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
                doodstream = DoodStream(api_key='34095x0xxxxxx7xxx728x')
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
                doodstream = DoodStream(api_key='34095x0xxxxxx7xxx728x')
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
                doodstream = DoodStream(api_key='34095x0xxxxxx7xxx728x')
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
                doodstream = DoodStream(api_key='34095x0xxxxxx7xxx728x')
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
    
    async def getAll(
        self, 
        folder_id: int = 0,
        page: int = 1, 
        per_page: int = 10
    ):
        """get files and folders combinedly

        parameters:
            folder_id (``int``, *optional*):
                the id of folder which files you want 
            
            page (``int``, *optional*):
                page no of the data
            
            per_page (``int``, *optional*):
                no of files should present per page

        Example:
            .. code-block:: python
                doodstream = DoodStream(api_key='34095x0xxxxxx7xxx728x')
                sts = await doodstream.getAll('New Folder')
                print(sts)
        
        Output:
            {
                "msg":"OK",
                "server_time":"2022-10-27 14:42:26",
                "status":200,
                "next_page_available":False,
                "result":{
                    [{"type": "folder", "name":"test file1","fld_id":"12345","code":"xxxxxx"},
                    {"type": "folder", "name":"test file2","fld_id":"67891","code":"xxxxxx"}],
                    {"type": "file", "download_url":"https://dood.la/d/xxxxxxx","single_img":"https://img.doodcdn.co/snaps/fkszt9c0xxxxxxx.jpg","file_code":"xxxxxxx","canplay":1,"length":"8436","views":"0","uploaded":"2022-10-22 09:01:41","public":"0","fld_id":"0","title":"Bimbisara (2022) Telugu HQ HDRip - 400MB - AAC - ESub"}]}}
        """

        url = f"https://doodapi.com/api/folder/list?fld_id=0&key=34095bvht3uqdobt8e0i4"
        params = {
            'fld_id': folder_id,
            'key': self.api_key
        }
        response = await self.request(url)

        if response['status'] == 200:
            data = response.copy()
            data['result'] = []
            data['next_page_available'] = False
            folders = response['result']['folders']
            total_folders = len(folders)
            files = []
            folder_start_index, folder_end_index = (page-1)*per_page, page*per_page
            folders = folders[folder_start_index:folder_end_index]
            if total_folders < folder_end_index:
                files_start_index = folder_start_index - total_folders
                files_end_index = files_start_index + per_page
                allfiles = response['result']['files']
                if len(allfiles) >= files_end_index:
                    data['next_page_available'] = True
                files = allfiles[files_start_index:files_end_index]
            else:
                data['next_page_available'] = True

            for folder in folders:
                folder['type'] = 'folder'
                data['result'].append(folder)
            for file in files:
                file['type'] = 'file'
                data['result'].append(file)
        else:
            data = response
        return data


    async def createFolder(self, name: str, parent_id: str = None):
        """Create a new folder

        parameters:
            name (``str``):
                the name of folder that should be created
            
            parent_id (``str``, *optional*):
                pass a parent id to create folder in that

        Example:
            .. code-block:: python
                doodstream = DoodStream(api_key='34095x0xxxxxx7xxx728x')
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
        return await self.request(url)


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
                doodstream = DoodStream(api_key='34095x0xxxxxx7xxx728x')
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

    async def listFiles(
        self, 
        page: int = 1,
        per_page: int = 10,
        folder_id: str = 0
    ):
        """get the list of files.

        parameters:
            page (``int``, *optional*):
                the page no you want

            per_page(``int``, *optional*):
                no of files to be included in the result
            
            folder_id (``str``, *optional*):
                pass a folder id to get the files from specified list

        Example:
            .. code-block:: python
                doodstream = DoodStream(api_key='34095x0xxxxxx7xxx728x')
                sts = await doodstream.listFiles()
                print(sts)
        
        Output:
            {
                "msg": "OK",
                "server_time": "2017-08-11 04:30:07",
                "status": 200,
                "result": {
                    "total_pages": 1,
                    "files": [
                        {
                        "download_url": "https://dood.to/d/xxx",
                        "single_img": "https://img.doodcdn.com/snaps/xxx.jpg",
                        "file_code": "xxx",
                        "canplay": 1,
                        "length": "1234",
                        "views": "1",
                        "uploaded": "2017-08-11 04:30:07",
                        "public": "1",
                        "fld_id": "0",
                        "title": "test_file"
                        }
                    ],
                    "results_total": "1",
                    "results": 1
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
    


    async def getFileStatus(self, file_id: str):
        """get the status of a file

        parameters:
            file_id (``str``):
                pass a file id, which you need to get the status

        Example:
            .. code-block:: python
                doodstream = DoodStream(api_key='34095x0xxxxxx7xxx728x')
                sts = await doodstream.getFileStatus('xxx')
                print(sts)
        
        Output:
            {
                "msg": "OK",
                "server_time": "2017-08-11 04:30:07",
                "status": 200,
                "result": [
                    {
                    "status": "Active",
                    "filecode": "xxx"
                    }
                ]
            }
        """

        url = f"{self.base_url}/file/check"
        params = {
            'key': self.api_key,
            'file_code': file_id
        }
        return await self.request(url, params)


    async def getFileInfo(self, file_id):
        """get the information about a file using its fileId

        parameters:
            file_id (``str``):
                pass a file id, from which you need to get the information

        Example:
            .. code-block:: python
                doodstream = DoodStream(api_key='34095x0xxxxxx7xxx728x')
                sts = await doodstream.createFolder('New Folder')
                print(sts)
        
        Output:
            {
                "msg": "OK",
                "server_time": "2017-08-11 04:30:07",
                "status": 200,
                "result": [
                    {
                    "single_img": "https://img.doodcdn.com/snaps/xxx.jpg",
                    "status": 200,
                    "filecode": "xxx",
                    "splash_img": "https://img.doodcdn.com/splash/xxx.jpg",
                    "canplay": 1,
                    "size": "123456",
                    "views": "0",
                    "length": "123456",
                    "uploaded": "2017-08-11 04:30:07",
                    "last_view": "",
                    "protected_embed": "/e/yyy",
                    "protected_dl": "/d/zzz",
                    "title": "test_file"
                    }
                ]
            }
        """

        url = f"{self.base_url}/file/info"
        params = {
            'key': self.api_key,
            'file_code': file_id
        }
        return await self.request(url, params)


    async def getFileImage(self, file_id: str):
        """get the thumb and all availabele images of a file 

        parameters:
            file_id (``str``):
                pass a file id, which you need to get the images

        Example:
            .. code-block:: python
                doodstream = DoodStream(api_key='34095x0xxxxxx7xxx728x')
                sts = await doodstream.getFileImage('xxx')
                print(sts)
        
        Output:
            {
                "msg": "OK",
                "server_time": "2017-08-11 04:30:07",
                "status": 200,
                "result": [
                    {
                    "status": 200,
                    "filecode": "xxx",
                    "title": "test_file",
                    "single_img": "https://img.doodcdn.com/snaps/xxx.jpg",
                    "thumb_img": "https://img.doodcdn.com/thumbnails/xxx.jpg",
                    "splash_img": "https://img.doodcdn.com/splash/xxx.jpg"
                    }
                ]
            }
        """

        url = f"{self.base_url}/file/image"
        params = {
            'key': self.api_key,
            'file_code': file_id
        }
        return await self.request(url, params)


    async def renameFile(self, file_id: str, name: str):
        """rename a file by its fileId

        parameters:
            file_id (``str``):
                pass a file id which you need to rename
            
            name (``str``):
                the new name of file

        Example:
            .. code-block:: python
                doodstream = DoodStream(api_key='34095x0xxxxxx7xxx728x')
                sts = await doodstream.renameFile('xxx', 'New Name')
                print(sts)
        
        Output:
            {
                "msg": "OK",
                "server_time": "2017-08-11 04:30:07",
                "status": 200,
                "result": "true"
            }
        """

        url = f"{self.base_url}/file/rename"
        params = {
            'key': self.api_key,
            'file_code': file_id,
            'title': name
        }
        return await self.request(url, params)
    

    async def searchFiles(self, query: str):
        """Create a new folder

        parameters:
            query (``str``):
                the term that need to be searched for.

        Example:
            .. code-block:: python
                doodstream = DoodStream(api_key='34095x0xxxxxx7xxx728x')
                sts = await doodstream.searchFiles()
                print(sts)
        
        Output:
            {
                "msg": "OK",
                "server_time": "2017-08-11 04:30:07",
                "status": 200,
                "result": "true"
            }
        """
        
        url= f"{self.base_url}/search/videos"
        params = {
            'key': self.api_key,
            'search_term': query
        }
        return await self.request(url, params)