from timeit import default_timer as timer
from src.crawler.Crawler import *

folderPath_Album = "H:\Pictures\Scrapper\Buondua-Downloader\Albums"
links = ["https://buondua.com/tag/mu-mu-7749", "https://buondua.com/tag/liang-ren-9887",
         "https://buondua.com/tag/zhang-mi-10050"]
links_tag = ["https://buondua.com/tag/%E5%88%A9%E4%B8%96-10566",
             "https://buondua.com/tag/hebe%E9%9F%A9%E5%BF%83%E9%9B%A8-11190",
             "https://buondua.com/tag/%E5%91%A8jojobaby-11313",
             "https://buondua.com/tag/%E6%96%87%E8%8A%AEjeninfer-10699"]

crawl = Buondua(folderPath_Album)
if __name__ == "__main__":

    albums = list()
    urls = list()
    with open(r"H:\Pictures\Scrapper\Buondua-Downloader\tagList.txt", "r") as file:
        pass
        urls = file.readlines()
    urls = ["https://buondua.com/tag/%E8%BD%A9%E8%90%A7%E5%AD%A6%E5%A7%90-11756"]
    analyzed = 0

    albums = crawl.ExtractFromURL(urls)
    """ 
    for link in urls:
        start = timer()
        if "tag" in link:
            albums += (crawl.ExtractFromTag(link))
        else:
            albums.append(crawl.ExtractAlbumFromURL(link))
            
        end = timer()
        analyzed+=1
        print(f"{analyzed}/{len(urls)} albums extracted @ {end - start}")
    """
    for album in albums:
        start = timer()
        result = crawl.DownloadAlbum(album)
        end = timer()
        print(
            f"{end - start}s for downloading {len(album.images)} images ({(end - start) / (len(album.images))} s/image)@ {album.path}")
        if len(result) > 0:
            print("\n".join(result))
