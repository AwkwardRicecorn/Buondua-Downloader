class Album:
    def __init__(self, title="", url=""):
        self.images = []  # Initialize images as an empty list for each instance
        self.title = title
        self.url = url
        self.tags = []

    def __str__(self):
        output: str = str(f"Album: {self.title}\n size: {len(self.images)}\n url: {self.url}")
        return output
