## Author: Jennine Nash
## Code project for python developer position
## Powerball entries
##
## Note: I thought it was a bit vague in the instructions, but I assumed that when 
## it said to "randomly select the tied number" in case of a tie, it meant to 
## select it from among the tied numbers, not to randomly generate a new number.
## I also allow the user to enter all employees before calculating the winning number.

import random


class Powerball:
    """Defines the first 5 numbers and powerball number of a Powerball entry
        plus the frequencies with which numbers are chosen"""

    freqs = {}
    pb_freqs = {}

    def __init__(self, nums, pball):
        self.nums = nums
        self.pball = pball
    
    def to_str(self):
        return " ".join(str(n) for n in self.nums) + " Powerball: " + str(self.pball)


class Employee:
    """Defines an employee by their name and powerball entry and keeps track of all employees"""

    emps = []

    def __init__(self, fname, lname, pball):
        self.pball = pball
        self.fname = fname
        self.lname = lname

    def to_str(self):
        return self.fname + " " + self.lname + " " + self.pball.to_str()


# computes the most commonly occurring choices for both the first 5 and the powerball number
# chooses the winner based on which numbers were chosen most often
def find_win():

    # sorts list of entries (first 5 numbers) and finds the most common entries
    # sets aside numbers which must be included, i.e. not tied to be in the top 5
    freq_kv = sorted([(k,v) for k,v in Powerball.freqs.items()], key=lambda x: -x[1])
    top5 = freq_kv[:5]
    cutoff = 0 if len(freq_kv) <= 5 else freq_kv[5][1]
    wins_kv = [(k,v) for (k,v) in top5 if v > cutoff]

    # need to find rest of winners if fewer than 5 have been set aside
    # choose from numbers that were tied for next most common occurrence
    if len(wins_kv) < 5:
        rmndr = 5 - len(wins_kv) 
        pickfrom = [(k,v) for (k,v) in freq_kv if v == cutoff]
        wins_kv += random.sample(pickfrom, rmndr)
    
    wins = [k for (k,v) in wins_kv]
    
    # find most common powerball number entry, choosing randomly in case of a tie
    pb_kv = [(k,v) for k,v in Powerball.pb_freqs.items()]
    max_pb = max(pb_kv, key=lambda x: x[1])[1]
    pbwin = random.choice([k for (k,v) in pb_kv if v == max_pb])

    winner = Powerball(wins, pbwin)
    return "\nPowerball winning number:\n" + winner.to_str()


# returns a string expressing which numbers have already been drawn
def exclude(used):
    if len(used) == 0:
        return ""

    pre = " (1-69 except "
    suf = ")"
    if len(used) == 1:
        return pre + str(used[0]) + suf
    
    for i in range(0, len(used)):
        if i < len(used) - 2:
            pre += str(used[i]) + ", "
        elif i == len(used) - 2:
            pre += str(used[i]) + " and "
        else:
            pre += str(used[i]) + suf
    return pre


if __name__ == "__main__":
    
    cont = True

    # continue looping until all employees have been entered
    while cont:
        used = []
        fname = raw_input("Enter your first name: ")
        lname = raw_input("Enter your last name: ")

        # record and validate each of first 5 entries
        for i in range(1, 6):

            ex = exclude(used)
            while True:
                n = raw_input("Select number #" + str(i) + ex + ": ")
                try:
                    n = int(n)
                except ValueError:
                    print "Invalid input"
                    continue
        
                if n >= 1 and n <= 69 and n not in used:
                    used.append(n)
                    if n in Powerball.freqs:
                        Powerball.freqs[n] += 1
                    else:
                        Powerball.freqs[n] = 1
                    break
                else:
                    print "Invalid input"

        # record and validate powerball number entry
        while True:
            n = raw_input("Select Powerball number (1-26): ")
            try:
                n = int(n)
            except ValueError:
                print "Invalid input"
                continue

            if n >= 1 and n <= 26:
                pball = Powerball(used, n)
                emp = Employee(fname, lname, pball)
                if n in Powerball.pb_freqs:
                    Powerball.pb_freqs[n] += 1
                else:
                    Powerball.pb_freqs[n]= 1
                break
            else:
                print "Invalid input"

        Employee.emps.append(emp)

        c = raw_input("Do you want to enter another employee? (y/n) ")
        cont = True if c[0].lower() == "y" else False
        print ""

    for e in Employee.emps:
        print e.to_str()

    print find_win()

            
        
