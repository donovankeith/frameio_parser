"""Print Callouts
Prints a list of all timecode callouts by file.
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

def main():
    for comment_file_path in iter_comment_files():
        comment_file = open(comment_file_path)

        # Get the filename w/o extension
        video_name = comment_file.readline()[:-5]
        print video_name

        comment_file_text = comment_file.read()

        timecode_comment_pattern = re.compile(r'''
            (?P<timecode>\d\d:\d\d:\d\d:\d\d)  # Timecode
            \s-\s[CALLOUT]+:  # 'CALLOUT' Token
            (?P<heading>.+)\|(?P<text>.+)
            ''', re.VERBOSE)

        callouts = []

        for match in timecode_comment_pattern.finditer(comment_file_text):
            callout = {
                timecode
            }

if __name__ == "__main__":
    main()