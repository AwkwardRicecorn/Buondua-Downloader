import argparse


class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Process some inputs.")
        self.parser.add_argument("-l",
                                 "--link",
                                 "--links",
                                 "-u",
                                 "--url",
                                 "--urls",
                                 nargs="+",
                                 type=str,
                                 help="URLs of albums or tags, seperate with space", )
        self.parser.add_argument("-f",
                                 "--file",
                                 "-t",
                                 "--text",
                                 nargs="*",
                                 type=str,
                                 help="Use text file instead of --links parameter, leave blank to use list_of_links.txt or pass a absolute path to file to download from", )
        self.parser.add_argument("-overwrite","-o",
                                 action="store_true",
                                 help="Overwrites existing", )
        self.parser.add_argument("-indexOnly","-i",
                                 action="store_true",
                                 help="Does not save images only create index. Does not check for not existing ones", )
        self.parser.add_argument("--output",
                                 type=str,
                                 default = "Albums",
                                 help="sets parent folder store default is current folder Albums ")

    def parse_args(self):
        args = self.parser.parse_args()
        return args

    def print_help(self, value):
        self.parser.print_help(value)
