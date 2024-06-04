import os
import re
import sys
import urllib.parse as ulparse
from pathlib import Path

from src.Utility import *
from src.crawler.Album import Album


class Buondua:
    def __init__(self,save_dir):
        self.base_url = 'https://buondua.com/'
        self.save_dir = save_dir

        self.black_list = ["tag"]
        self.hostname = "buondua"
        self.log = "Log.txt"

    def Download(self, downloader, url: str, overwrite: bool = True, headless: bool = False, indexOnly: bool = False):

        def getImagesFromPage(url: str):
            images = list()
            img_urls = openUrl(url).find(class_='article-fulltext').find_all('img')
            for i, img_url in enumerate(img_urls):
                image_url = img_url['src']
                exts = image_url.split("/")
                ext = exts[-1].split("?")[0]
                images.append((Path(ext).with_suffix(''), image_url))
            return images

        def getAlbum(url: str):
            album = Album()
            site = openUrl(url)

            if site is None:
                raise Exception(f"url is not correct or site is unreachable")

            album.url = url
            title = site.find(class_="article-header").find("h1").text
            page_urls = site.find(class_="pagination-list").select("span > a")
            album.tags = [span.text for span in site.find(class_="tags").select("a > span")]
            album.title = re.sub(r'[\\/:\*\?"<>\|]', "-", title)
            album.cache = openUrl(url, raw=True).content
            if len(page_urls) <= 0:
                raise print(f"Failed to find Album")

            for i, page_url in enumerate(page_urls):
                albumpage_url = ulparse.urljoin(self.base_url, page_url['href'])
                page_images = getImagesFromPage(albumpage_url)
                album.images += page_images
            return album

        album = getAlbum(url)
        album_path = os.path.join(self.save_dir, slugify(album.title))
        try:
            Path(album_path).mkdir(parents=True, exist_ok=overwrite)

            for index in range(len(album.images)):
                name, images = album.images[index]
                file_path = Path(os.path.join(album_path, str(index + 1))).with_suffix('.png')
                downloader.download_image_buondua(images, os.path.abspath(file_path))

                sys.stdout.write('\r')
                j = (index + 1) / len(album.images)
                sys.stdout.write(f'[{index + 1}|{len(album.images)}]\t')
                sys.stdout.write("[%-20s] %d%%" % ('=' * int(20 * j), 100 * j))
                sys.stdout.write(f' @ {os.path.abspath(album_path)}')
                sys.stdout.flush()

        except FileExistsError:
            print(album.title, " already exists")
        finally:
            with open(os.path.join(album_path, "!Info.txt"), "w", encoding="utf-8") as file:
                file.write(album.url)
                tags = '\n'.join(album.tags)
                file.write(f"\n\nTags: \n{tags}")
            print("\n")

    def DownloadAlbums(self, downloader, file: str, overwrite: bool = True, headless: bool = False,
                       indexOnly: bool = False):
        def is_blacklisted(url):
            # Parse the URL
            parsed_url = ulparse.urlparse(url)
            path = parsed_url.path
            # Check if any blacklisted word is in the path
            contains_blacklist = any(word in path for word in self.black_list)

            # URL must contain at least one required word and no blacklisted words
            return contains_blacklist

        with open(file, 'r', encoding="utf-8") as file:
            with open(self.log, "a", encoding="utf-8") as log:
                lines = file.readlines()
                for index in range(len(lines)):
                    line = lines[index]

                    if is_blacklisted(line):
                        log.writelines(str(line))

                    print(f"[{index + 1}|{len(lines)}] Album:")
                    self.Download(downloader, line, overwrite, headless, indexOnly)
