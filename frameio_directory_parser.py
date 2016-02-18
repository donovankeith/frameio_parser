"""Frame.io Directory Parser
Creates objects based on any text file contained in a "comments" directory.
"""

import os
import re

def iter_comment_files():
    """Yields each file_path for `.txt` files in `./comments` directory."""

    # Print all text files in "./comments" directory.
    for root, dirs, files in os.walk("./comments"):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                yield file_path

class FrameioVideo:
    """Class for storing Frame.io Video Info from Comments.txt exports."""

    def __init__(self, file_path):
        self.file_path = file_path
        self.file = open(file_path)
        # self.video_file_name = self.file.readline()
        self.text = self.file.read()


    def __str__(self):
        return self.text

def print_comments():
    """Print the contents of all .txt comments files in comments directory."""

    for comments_file_path in iter_comment_files():
        comments_file = FrameioVideo(comments_file_path)
        # print comments_file.video_file_name
        print comments_file.text

if __name__ == '__main__':
    print_comments()