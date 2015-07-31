"""Frame.io Comment Export Parser
(Eventually will...) Takes a "export.txt" in the same directory and converts it into a usable format for pasting into GoogleSheets.
"""

def main():
    with open('export.txt') as f:
        lines = f.readlines()

        for line in lines:
            print line

if __name__ == "__main__":
    main()