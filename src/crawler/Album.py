from datetime import date


class Album:
    def __init__(self, title="", url=""):
        self.images = []  # Initialize images as an empty list for each instance
        self.title = title
        self.url = url
        self.tags = []
        self.path = ""

    def GetAsDict(self) -> {}:
        album = {
            "name": self.title,
            "tags": self.tags,
            "url": self.url,
            "latest update": str(date.today())
        }
        return album

    def __str__(self):
        output: str = str(f"Album: {self.title}\n size: {len(self.images)}\n url: {self.url} \n @: {self.path}")
        return output
