import logging
log = logging.getLogger(__name__)

import aiohttp


def DetectFileSize(url):
    r = requests.get(url, allow_redirects=True, stream=True)
    total_size = int(r.headers.get("content-length", 0))
    return total_size


async def isdownloadable_link(link):
    """Return (downloadable or not, filename)"""
    
    filename = 'Unknown'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link, timeout=aiohttp.ClientTimeout(total=30)) as response:
                content_type = response.content_type
                filesize = int(response.headers.get("Content-Length", 0))
                if 'text' in content_type.lower() or 'html' in content_type.lower() or filesize < 100:
                    filename = link.rsplit("/")[-1]
                    filename = await replace(filename)
                    return False, filename
                else:
                    try:
                        filename = response.content_disposition.filename
                    except:
                        pass
                    
                    if not filename:
                        filename = response._real_url.name
                    if not '.' in filename:
                        # add ext
                        filename += '.' + content_type.split('/')[-1]

                    filename = await replace(filename)
                    return True, filename

    except Exception as e:
        print(e)
        filename = link.rsplit("/")[0]
        filename = await replace(filename)
        return False, filename
