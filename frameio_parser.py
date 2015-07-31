"""Frame.io Comment Export Parser
(Eventually will...) Takes a "export.txt" in the same directory and converts it into a usable format for pasting into GoogleSheets.

Looks for comments of this format:
CALLOUT: Command Name | Keyboard Shortcut
SECTION HEADING: This is The Heading
SECTION: Section Heading

"""

import os

def copy_to_clipboard(text):
    """Copy text to OS clipboard.
    Source: http://stackoverflow.com/questions/11063458/python-script-to-copy-text-to-clipboard
    Might only be MacOS compatible
    """

    os.system("echo '%s' | pbcopy" % text)

def main():
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

    with open('export.txt') as f:
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
            print "-------------------"
            print "Comment: ", comment

            def get_callout(comment, callout_pattern="CALLOUT: ", row_format=" \t%s\t%s\t%s"):
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

            callout = get_callout(comment)
            if callout:
                callouts.append(callout)

        headings = ["ID",
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

        output = ""
        for heading in headings:
            output += (heading + "\t")
        output += "\n"

        for callout in callouts:
            output += (callout + "\n")

        print output
        copy_to_clipboard(output)

if __name__ == "__main__":
    main()