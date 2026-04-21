import sys
import library

def days_worked(data, headers, factor = 1.5):
    keys = data.keys()
    days = {}

    for key in keys:
        if(key not in days):
            days[key] = 0
        for item in data[key]:
            try:
                time_ob = float(item["TOTAL %23 DAYS ON ON BOARD"])
                time_uw = float(item["TOTAL %23 OF DAYS UNDERWAY"])
                days[key] += time_uw * factor + (time_ob - time_uw)
            except:
                print(item)

    listOut = sorted([(k,v) for k,v in days.items()], key = lambda x:x[1])
    
    return listOut      

if __name__ == "__main__":
    testKey = ("STOFFEL", "JONATHAN")
    if len(sys.argv) < 2:
        print("Usage: python template.py <csvfile>")
        sys.exit(1)
    headers, data = library.read_once(sys.argv[1], "LAST NAME", "FIRST NAME")
    """print(headers)
    for a in data.items():
        print(a)
        print()
        """

    
    days = days_worked(data, headers)
    days2 = days_worked(data, headers, 2)

    #print(days)

    askAgain = True
    while(askAgain):
        try:
            numChoices = int(input("How many inspectors do you need? "))
            if(numChoices > len(days)):
                print(f"Number must be less than available inspectors: {len(days)}. Please choose again")
            elif(numChoices <= 0):
                print(f"Input {numChoices} invalid. Please choose again.")
            else:
                askAgain = False
        except:
            print("Error in input, please insert a number.")
    
    people = [x for x,y in days[:numChoices]]

    print(f"These are the next {numChoices} inspectors available:")
    for lname, fname in people:
        print(f"\t{lname}, {fname}")
    