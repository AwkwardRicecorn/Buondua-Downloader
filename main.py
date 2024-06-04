import time

from src.ArgParser import *
from src.crawler.Crawler import *
from src.crawler.Downloader import *

folderPath = "Albums"
fileLocation = "albumList.txt"
url = "https://buondua.com/xiuren-no-6512-%E9%B1%BC%E5%AD%90%E9%85%B1fish-81-photos-36226"
overwrite: bool = True
headless: bool = False
indexOnly: bool = False
crawl = Buondua(folderPath)
parser = ArgParser()


def django_validate(url: str):
    # From https://github.com/django/django/blob/stable/4.1.x/django/core/validators.py

    ul = "\u00a1-\uffff"  # Unicode letters range (must not be a raw string).

    # IP patterns
    ipv4_re = (
        r"(?:0|25[0-5]|2[0-4][0-9]|1[0-9]?[0-9]?|[1-9][0-9]?)"
        r"(?:\.(?:0|25[0-5]|2[0-4][0-9]|1[0-9]?[0-9]?|[1-9][0-9]?)){3}"
    )
    ipv6_re = r"\[[0-9a-f:.]+\]"  # (simple regex, validated later)

    # Host patterns
    hostname_re = (
            r"[a-z" + ul + r"0-9](?:[a-z" + ul + r"0-9-]{0,61}[a-z" + ul + r"0-9])?"
    )
    # Max length for domain name labels is 63 characters per RFC 1034 sec. 3.1
    domain_re = r"(?:\.(?!-)[a-z" + ul + r"0-9-]{1,63}(?<!-))*"
    tld_re = (
            r"\."  # dot
            r"(?!-)"  # can't start with a dash
            r"(?:[a-z" + ul + "-]{2,63}"  # domain label
                              r"|xn--[a-z0-9]{1,59})"  # or punycode label
                              r"(?<!-)"  # can't end with a dash
                              r"\.?"  # may have a trailing dot
    )
    host_re = "(" + hostname_re + domain_re + tld_re + "|localhost)"

    regex = re.compile(
        r"^(?:[a-z0-9.+-]*)://"  # scheme is validated separately
        r"(?:[^\s:@/]+(?::[^\s:@/]*)?@)?"  # user:pass authentication
        r"(?:" + ipv4_re + "|" + ipv6_re + "|" + host_re + ")"
                                                           r"(?::[0-9]{1,5})?"  # port
                                                           r"(?:[/?#][^\s]*)?"  # resource path
                                                           r"\Z",
        re.IGNORECASE,
    )
    return re.match(regex, url) is not None


def main(args: list):
    """Check if args is link or file"""
    downloader = ImageDownloader()
    start = time.time()
    if args != []:
        for arg in args:
            if not validate(str(arg)) or not str(arg).startswith(
                    "https://buondua.com/"
            ):  # check if url is validated, if not then assume that is a file
                try:
                    open(arg).close()  # check file is validated, if not then throw error
                    crawl.DownloadAlbums(downloader=downloader, file=arg, overwrite=overwrite, indexOnly=indexOnly)
                except Exception as e:
                    print(e)
            else:  # if url is validated
                crawl.Download(downloader=downloader, url=arg, overwrite=overwrite, indexOnly=indexOnly)
    else:  # if no arg was provided with --file parameter, download from list_of_links.txt
        crawl.DownloadAlbums(downloader=downloader, file=fileLocation, overwrite=overwrite, indexOnly=indexOnly)
    end = time.time()
    downloader.Quit()
    print(f'Finished Crawler with {round(end - start, 2)}s')


if __name__ == "__main__":
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    validate = django_validate

    folderPath = args.output
    crawl.save_dir = folderPath
    overwrite = args.overwrite
    indexOnly = args.indexOnly
    if args.file or args.file == []:
        main(args.file)
    elif args.link:
        main(args.link)
