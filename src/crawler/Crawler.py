import os
import urllib.parse as ulparse
from pathlib import Path

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

from src.Utility import *
from src.crawler.Album import Album
import winshell
from typing import Optional


class Buondua:
    def __init__(self, save_dir):
        self.base_url = 'https://buondua.com/'
        self.save_dir = save_dir
        self.hostname = "buondua"

    def __getImagesFromPage(self, url: str):
        images = list()
        img_urls = openUrl(url).find(class_='article-fulltext').find_all('img')
        for i, img_url in enumerate(img_urls):
            image_url = img_url['src']
            exts = image_url.split("/")
            ext = exts[-1].split("?")[0]
            images.append((Path(ext), image_url))
        return images

    def ExtractAlbumsFromPage(self, url):  # ->Album:
        site = openUrl(url)
        albumURLs = [ulparse.urljoin(self.base_url, albumURL.find(class_="item-link").attrs["href"]) for albumURL
                     in
                     site.find_all(class_="item-thumb")]
        return albumURLs

    def ExtractAlbumFromURL(self, url) -> Optional[Album]:
        album = Album()
        site = openUrl(url)

        album.title = slugify(os.path.basename(url), True)  # re.sub(r'[\\/:\*\?"<>\|]', "-", title)
        album.path = os.path.join(self.save_dir, slugify(album.title, True))
        if Path(album.path).exists():
            return None

        album.url = url
        album.tags = [span.text for span in site.find(class_="tags").select("a > span")]

        page_urls = site.find(class_="pagination-list").select("span > a")
        if len(page_urls) <= 0:
            raise print(f"Failed to find Album")

        for i, page_url in enumerate(page_urls):
            albumpage_url = ulparse.urljoin(self.base_url, page_url['href'])
            page_images = self.__getImagesFromPage(albumpage_url)
            album.images += page_images

        return album

    def ExtractFromTag(self, url) -> List[Album]:
        maxAlbumsPerPage = 20
        site = openUrl(url)
        albums = list()

        # 1 tag -> albumURLs
        albumURLs = list()
        pageAmount = max(len(site.find_all(class_="pagination-link")), 1)
        pages = [url + f"?start={pageIndex * maxAlbumsPerPage}" for pageIndex in range(pageAmount)]
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.ExtractAlbumsFromPage, url) for url in pages]
            for future in as_completed(futures):
                albumURLs += (future.result())
        print()
        # 2 albumURLs-> albums
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.ExtractAlbumFromURL, url) for url in albumURLs]
            for future in as_completed(futures):
                albums.append(future.result())
        albums = [item for item in albums if item is not None]
        return albums

    def DownloadAlbum(self, album: Album):
        result = list()

        try:
            Path(album.path).mkdir(parents=True)
        except Exception as e:
            return result

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(DownloadImage, url, os.path.join(album.path, name)) for name, url in
                       album.images]
        for future in as_completed(futures):
            re_success, re_url, re_path = future.result()
            if not re_success:
                result.append((re_path, re_url))
        self.CreateJSON(album)
        self.CreateTagShortcutFolders(album)
        return result

    def CreateJSON(self, album):
        filepath = os.path.join(album.path, "info.json")
        data = (album.GetAsDict())
        return CreateJSON(filepath, data)

    def CreateTagShortcutFolders(self, album: Album):
        generalTagPath = os.path.join(self.save_dir, "!Tags")
        for tag in album.tags:
            tagPath = os.path.join(generalTagPath, tag)
            Path(tagPath).mkdir(parents=True, exist_ok=True)
            shortcut_path = os.path.join(tagPath, album.title + ".lnk")
            shortcut = winshell.Shortcut(shortcut_path)
            shortcut.path = album.path
            shortcut.write()

    def ExtractFromURL(self, urls: List[str]):

        def sort(link:str):
            albums: List[Album] = list()
            try:
                if "tag" in link:
                    albums += (self.ExtractFromTag(link))
                else:
                    album = self.ExtractAlbumFromURL(link)
                    if album is not None:
                        albums.append(album)
            except Exception as e:
                print(f"Error with {link}")
                raise e
            return albums

        albums = list()
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(sort, url) for url in urls]
            for future in as_completed(futures):
                albums.append(future.result())
