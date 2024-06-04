## Buondoa Album images Downloader 

#### Abilities and Requirements
    - Download Album(s)
    - Will download images as screenshots
    - Requires Firefox
    - Windows only tested
    - Sometimes while downloading nothing will happen for several seconds. This is due to inconsistency in the website code and partially Cloudflare. To reduce amount of wrong downloads, the code will wait several seconds before attempting another approach. 
    - Wrong downloads will happen. !Info will provide the url to the website with images. Simply redownload it.  
    - Might need to install Pillow and beautifulsoup4 libary. Run Requirements.cmd

#### Startup
    - Execute by open in folder of main.py Windows-Terminal
    - Call python3 main.py (with parameters)
#### Downloading Album(s)
Will get all images from all pages of the album and download
##### Direct
- Downloading new Album:
    - python3 main.py -l [URL]
    OR
    Save at designated location. Default is Album
    - python3 main.py -l [URL] -output [folderPath]
- Updating existing Albums
    Overwrite existing images
  - python3 main.py -l [URL] -o
  - python3 main.py -l [URL] -o -output [folderPath]

    OR
    Index Only but don not download images
  - python3 main.py -l [URL] -i
  - python3 main.py -l [URL] -o -output [folderPath]

Possible to download multiple Albums at once by seperating via spaces
##### Indirect via txt-file
Default name for txt-file is albumList.txt
- Downloading new Album:
    - python3 main.py -f [fileLocation]
    OR
    Save at designated location. Default is Album
    - python3 main.py -f [fileLocation] -output [folderPath]
- Updating existing Albums
    Overwrite existing images
  - python3 main.py -f [fileLocation] -o
  - python3 main.py -f [fileLocation] -o -output [folderPath]

    OR
    Index Only but don not download images
  - python3 main.py -f [fileLocation] -i
  - python3 main.py -f [fileLocation] -o -output [folderPath]
Possible to download multiple Albums at once by seperating in linebreaks

#### Limits
    - No Multithreading
    - No Tags Download

#### Customizazion
##### Running Without window
    You might get stuck in cloudflare protection window - Restarting might be the only option
    Can be executed without window but will still require firefox
    In main.py change headless parameter from  *headless: bool = False* to *headless: bool = True*

#####  Changing browser:
In src/Downloader.py only changes in __init__() and of course import are required 
For what to change, look up https://www.selenium.dev/documentation/webdriver/browsers/


#### Acknowlegement:
Remesh of multiple abandoned git-projects:
  - https://github.com/faberuser/buondua-downloader
  - https://github.com/sugihara1212/buondua-downloader
