import sys
import library

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python template.py <csvfile>")
        sys.exit(1)
    headers, data = library.read_once(sys.argv[1], "EVENT ID")

    #print(data)

    cmd = ""
    while(cmd not in {"q", "Q", "quit", "Quit", "QUIT"}):
        cmd = input("What would you like to do to the data? (Sort, Count, Display)\n")
        if(cmd not in {"Sort", "sort", "count", "count", "q", "Q", "quit", "Quit", "QUIT", "disp", "Disp", "display", "Display"}):
            print(f"Invalid command {{{cmd}}}!")
        elif(cmd in {"Sort", "sort"}):
            head = input(f"Which header would you like to sort on?\n{{{headers}}}\n")
            val = input("Which value would you like to sort for?\n")
            sorted = library.getAll(data, head.upper(), val.upper()).values()
            if(len(sorted) == 0):
                print(f"ERROR! Could not find key {val}")
            else:
                for block in sorted:
                    for item in block:
                        print(item)
        elif(cmd in {"disp", "Disp", "display", "Display"}):
            eid = input("Which event ID would you like to display")
            for block in data[(eid)]:
                print(block)
        