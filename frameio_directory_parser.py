"""Frame.io Directory Parser
Creates objects based on any text file contained in a "comments" directory.
"""

import os

def iter_comment_files():
    """Yields each file_path for `.txt` files in `./comments` directory."""

    # Print all text files in "./comments" directory.
    for root, dirs, files in os.walk("./comments"):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                yield file_path

def print_comments():
    """Print the contents of all .txt comments files in comments directory."""

    for comments_file_path in iter_comment_files():
        comments_file = open(comments_file_path)
        comments_text = comments_file.read()
        print comments_text

if __name__ == '__main__':
    print_comments()