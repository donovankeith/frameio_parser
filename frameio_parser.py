"""Frame.io Comment Export Parser
(Eventually will...) Takes a "export.txt" in the same directory and converts it into a usable format for pasting into GoogleSheets.
"""

import re

def main():
    timecode_style = "00:00:00:00"
    timecode_length = len(timecode_style)
    keywords = ["CALLOUT", "SECTION", "INFO"]

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

    with open('export.txt') as f:
        lines = f.readlines()

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

            print line

            #Get the callouts
            lead_in = timecode_string + " - "
            lead_in_length = len(lead_in)

            comment = line[lead_in_length:]
            print "Comment: ", comment





if __name__ == "__main__":
    main()