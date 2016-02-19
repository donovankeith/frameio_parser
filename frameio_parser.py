"""Frame.io Comment Export Parser
(Eventually will...) Take "comments.txt" from the script's directory and convert it a tab-delimited format
 for pasting into GoogleSheets.

 It looks for comments in a format extremely particular to my workflow, and is probably not of general use without
 extensive rewrites.

Looks for comments of this format:
CALLOUT: Copy | Ctrl/Cmd + C
HEADER: Part 02 | Modeling the Ship
INFO: Longer strings should go in here. Yep, that's definitely true.

It also gracefully handles these typos / alternates:
SECTION:
SECTOIN:
SECTION HEADING:
SECTOIN HEADING
HEADING
HEADER

TO DO
-----

- [ ] Handle "&gt;" => ">" conversion
- [ ] Do a more thorough parsing of all content, not just the comments you most care about
- [ ] Write a Frame.io video comments class
- [ ] Generate a TOC based on chapter headings
- [ ] Add a few meaningful characters to the filename
- [ ] Export markers than can be imported into Camtasia (if that's possible)
- [ ] Auto-Generate the Google Spreadsheet
- [ ] Format the Google Sheet more intelligently

"""

import os

HEADINGS = ["Video",
            "Timecode",
            "CommandName",
            "CommandNameBar",
            "KeyboardShortcut",
            "KeyboardShortcutBar",
            "SectionNumber",
            "SectionNumberBar",
            "SectionTitle",
            "SectionTitleBar",
            "AdditionalInfo",
            "AdditionalInfoBar"]

def copy_to_clipboard(text):
    """Copy text to OS clipboard.
    Source: http://stackoverflow.com/questions/11063458/python-script-to-copy-text-to-clipboard
    Might only be MacOS compatible
    """

    os.system("echo '%s' | pbcopy" % text)

def get_callout(timecode_string, comment, callout_pattern="CALLOUT: ", row_format=" \t%s\t%s\t%s"):
    """Converts a raw comment into a timecode, first_half, second_half tuple."""

    if not comment:
        return

    #Get the keyboard callouts
    callout_pattern = callout_pattern.lower()
    callout_pattern_length = len(callout_pattern)

    if comment[:callout_pattern_length].lower() == callout_pattern:
        callout_string = comment[callout_pattern_length:]

        #Get the first and second halves, don't split the second half if you see more "|"
        callout_components = callout_string.split("|", 1)

        def strip_components(components):
            new_components = []
            for component in components:
                new_components.append(component.strip())
            return new_components

        callout_components = strip_components(callout_components)

        first_half = callout_components[0]
        second_half = ""

        if len(callout_components) > 1:
            second_half = callout_components[1]

        return row_format % (timecode_string, first_half, second_half)

def parse_file(filename):
    timecode_style = "00:00:00:00"
    timecode_length = len(timecode_style)

    def is_timecode(stub):
        """Return True if `stub` matches pattern ##:##:##:##"""

        #Split the stub into chunks at the ":"s
        chunks = stub.split(":")
        if len(chunks) != 4:
            return False

        #Are all of the chunks numbers?
        for chunk in chunks:
            if not chunk.isdigit():
                return False

        return True

    with open(filename) as f:
        video_filename = f.readline()[:-5]
        lines = f.readlines()

        callouts = []
        for line in lines:

            #Don't read in lines that don't have timecode style + " - " delimeter
            if len(line) < timecode_length + 3:
                continue

            timecode_string = line[:timecode_length]

            #Skip this line if it's not timecode formatted
            if not is_timecode(timecode_string):
                continue

            #Convert the timecode chunks into usable ints
            hour, minute, second, frame = map(int, timecode_string.split(":"))

            #Get the callouts
            lead_in = timecode_string + " - "
            lead_in_length = len(lead_in)

            comment = line[lead_in_length:]
            # print "-------------------"
            # print "Comment: ", comment

            section_format = " %s\t\t\t\t\t%s\t\t%s"

            callout_types = [
                ("CALLOUT: ", " %s\t%s\t\t%s"),

                ("SECTION: ", section_format),
                ("SECTOIN: ", section_format),
                ("SECTION HEADING: ", section_format),
                ("SECTOIN HEADING: ", section_format),
                ("HEADING: ", section_format),
                ("HEADER: ", section_format),
                ("INFO: ", " %s\t\t\t\t\t\t\t\t\t%s %s")
            ]

            for callout_type in callout_types:
                callout_pattern, row_format = callout_type
                callout = get_callout(timecode_string, comment, callout_pattern, row_format)

                if callout:
                    callouts.append(callout)

        output = ""

        for callout in callouts:
            output += (video_filename + "\t" + callout + "\n")

        return output


def main():
    output = ''
    for heading in HEADINGS:
        output += (heading + "\t")
    output += "\n"

    for root, dirs, files in os.walk("./comments"):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                output += parse_file(file_path)

    print output

if __name__ == "__main__":
    main()