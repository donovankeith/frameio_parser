"""Frame.io Directory Parser
Creates objects based on any text file contained in a "comments" directory.
"""

import os
import re

"""
Regular Expression Notes
========================

Character Types
---------------

\w -> any AAbb10_
\W -> anything that's not a word
\s -> whitespace
\S -> not whitespace
\d -> 0123456789
\D -> not a number
\b -> word boundaries / edges of a word
\B -> anything that ISN'T
\ -> Escape

lowercase -> MATCH
UPPERCASE -> Match NOT that Thing


Counts
------

{3}     Happens 3 times
{,3}    0-3 times
{3,}    3+ times
{3,5}   3, 4, or 5 times

? 0-1 times
* 0+ times
+ 1+ times


Sets
----

[aple] -> Any of these characters
[a-z] -> Lowercase letter between a & z
[^2] -> Anything that is *not* 2

Groups
------
(\w) -> Group a character
(P<name>\w) -> Name the group 'name'

regroup.groupdict() -> return the groups as named elements in a dictionary.

"""

"""

First Comment
-------------

ID: r'\d{3} - '

Timecode: r'\d\d:\d\d:\d\d:\d\d'
Time: r'\d{2}:\d{2}\w\w'


Flags
-----

re.IGNORECASE or re.I -> Ignores case
re.MULTILINE -> Each line as string
re.VERBOSE -> Use multiline comment string
re.X -> Verbose


Multiline Regex Comments
-------------------------
re.findall(r'''
    \w  # Find a word
    \d  # Find a digit
'''
, data, re.VERBOSE|re.IGNORECASE)

"""


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
        # print comments_file.text

        # print(re.findall(r"\d{2}:\d{2}:\d{2}:\d{2}", comments_file.text))

        lines = re.findall(r'''
            (?P<comment_id>\d{3})\s-\s  #Primary Comment ID
            (?P<first_name>\w+)\s  # First Name
            (?P<last_name>\w+)\s-\s  # Last Name
            (?P<hour>\d+):  # Hour
            (?P<minute>\d\d)  # Minute
            (?P<am_pm>\w\w)\s  # AM/PM
            (?P<month_name>\w+)\s  # Month
            (?P<day>\d{1,})\w\w,\s  # Day
            (?P<year>\d{4})  # Year
''', comments_file.text, re.VERBOSE)



if __name__ == '__main__':
    print_comments()