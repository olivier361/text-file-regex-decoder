"""
Provided for you is the encryption alphabet used to encrypt the provided files.
This inclues: a-z, A-Z, 0-9, punctuation like .();, space and newline
"""

#decoder.py
#by Olivier Gervais-Gougeon

import sys
import re
import string
from cipher import *

alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation + " \n"


def main():
    #debug_print(alphabet)

    #declare variables related to user input:
    is_valid_file = False

    #ask the user for an encrypted file:
    #check if file exists and if not, prompt again:
    while(is_valid_file == False):
        filename = ask_for_input("Enter name of file: ")
    
        try:
            file_ptr = open(filename, "r")
            file_ptr.close()
            is_valid_file = True
        except:
            print("unable to open " + str(filename) + " for reading. Please provide another filename.")
            is_valid_file = False

    #ask the user for a password.
    #Check if valid with regex and decryption. Else prompt again:
    is_valid_password = False

    while(is_valid_password == False):
        password = ask_for_input("Enter password: ")
        #check with regex if the password is valid:
        is_valid_password = check_password(password)

        #if regex password invalid, ask again before decoding:
        if is_valid_password == False:
            continue
        debug_print("The provided password is of valid Regex format.")

        #if password is valid, create an instance of FileDecoder
        #with password, filename and alphabet:
        file_decoder = FileDecoder(key=password, filename=filename, alphabet=alphabet)

        #check if decoding works, otherwise ask for password again:
        try: #NOTE: try block might not be necessary here since it is handled in calculate()
            #file_decoder.decode()
            #file_decoder.print_lines(len(file_decoder)-5,len(file_decoder)+1) #TODO: Remove for final build.
            is_valid_password = calculate(file_decoder) #returns a boolean
        except DecryptException as e:
            print(e)
            is_valid_password = False

        #calculate() in the while loop builds the average ferry delays
        #aka output with the decoded CSV file by iterating through the decrypted rows.

#END OF MAIN()


#ask_for_input:
#function is essentially just input() but checks and
#exits program if q is typed.
def ask_for_input(string):
    result = input(string)
    
    if result == "q":
        print("'q' exit command entered. Exiting Program.") #TODO: Keep as a regular print of debug_print?
        sys.exit()

    return result


#check_password:
#Returns true if the password matches specifications.
def check_password(string):
    #Here we are doing a bunch of smaller REGEX tests to check for
    #individual requirements. This makes it more readble and less error prone.

    #1. Check that password has 6 to 8 characters:
    #source: https://stackoverflow.com/questions/33312175/matching-any-character-including-newlines-in-a-python-regex-subexpression-not-g/33312193
    debug_print(re.match(r'^[\w\W]{6,8}$', string)) 
    if re.match(r'^[\w\W]{6,8}$', string) == None:
        #debug_print("Failed REGEX Test: Not 6 to 8 characters")
        print("Provided password must contain 6 to 8 characters.")
        return False
    debug_print("Passed first REGEX Test: Between 6 to 8 characters")

    #2. Check that password has at least 1 uppercase letter:
    debug_print(re.search(r'[A-Z]', string))
    if re.search(r'[A-Z]', string) == None:
        #debug_print("Failed REGEX Test: Not at least 1 uppercase letter")    
        print("Provided password must contain at least 1 uppercase letter.")
        return False
    debug_print("Passed second REGEX Test: At least 1 uppercase letter")

    #3. Check that password has at least 2 numerical digits:
    debug_print(re.search(r'\d[\w\W]*\d', string))
    if re.search(r'\d[\w\W]*\d', string) == None:
        #debug_print("Failed REGEX Test: Not at least 2 digits")
        print("Provided password must contain at least 2 digits.")
        return False
    debug_print("Passed third REGEX Test: At least 2 digits")

    #4. Check that password has exactly 2 special characters !@#$*-_
    debug_print(re.search(r'^[^!@#$&*_.-]*[!@#$&*_.-][^!@#$&*_.-]*[!@#$&*_.-][^!@#$&*_.-]*$', string))
    if re.search(r'^[^!@#$&*_.-]*[!@#$&*_.-][^!@#$&*_.-]*[!@#$&*_.-][^!@#$&*_.-]*$', string) == None:
        debug_print("Failed REGEX Test: Not exactly 2 special characters !@#$&*._-")
        print("Provided password must contain exactly 2 special characters < !@#$&*._- >.")
        return False
    debug_print("Passed fourth REGEX Test: Exactly 2 special characters !@#$&*._-")
    
    #If no test has failed:
    return True


#calculate():
#iterates through the decrypted rows given in list form by the FileDecoder.
#At the same time, we are checking if the file has been properly decrypted.
#Parameters:
#fd: pointer to a FileDecoder object.
def calculate(fd):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    delay_table = {} #dictionary will hold lists of delays, at month of key.
    avg_delay = {} #dictionary stores calculated average delay for month of key.
    row_len = 18
    row_count = 0
    
    #The following variables are the index numbers we expect certain information at:
    i_sdep_month = 4 #scheduled_departure_month
    i_sdep_hour = 6 #scheduled_departure_hour
    i_sdep_min = 7 #scheduled_departure_minute
    i_adep_hour = 11 #actual_departure_hour
    i_adep_min = 12 #actual_departure_minute

    #Calculates the delays for each row and then the average delay and printing result:
    try:
        #calculates an average delay and creates a dictionary where months are the keys
        #and values store a list of the delay of every sailing in that month.
        for row in fd:
            if len(row) == row_len and row_count != 0: #verifying that row is a valid CSV entry and also not the header.
                #calculates the delay of a row in minutes:
                delay = (int(row[i_adep_hour])*60 + int(row[i_adep_min])) - (int(row[i_sdep_hour])*60 + int(row[i_sdep_min]))
                #add delay result to delay table under correct month.
                #creates a new month key if not already there.
                if int(row[i_sdep_month]) in delay_table:
                    delay_table[int(row[i_sdep_month])].append(delay)
                else:
                    delay_table[int(row[i_sdep_month])] = [delay]
            row_count += 1
        #debug_print("delay_table: " + str(delay_table))
        
        #calculates the average monthly delay from the table made above:
        for (k, v) in delay_table.items():
            avg_delay[k] = find_average(v)
        #print out results from the found average monthly delays:
        print_results(months, avg_delay, fd)

    except DecryptException as e:
        print(e)
        return False
    #if decryption was succesful.
    return True


#find_average(list of int):
#Given a list of integers (or floats technically),
#returns a float value for the average.
def find_average(li):
    total = 0
    for num in li:
        total = total + num
    return float(total/len(li))
        

#print_results(list of month names, dict with (int month, float delay), FileDecoder object):
#Given a dictionary with month number keys, float delay values
#and a pointer to a FileDecoder object. Prints out the results according to specs.
def print_results(month_names, di, fd):
    entries = len(fd) #calling this before printing RESULTS keyword so debug prints don't go in final output.
    print("")
    print("RESULTS")
    print("FileDecoder: " + str(fd))
    print("Entries: " + str(entries))

    for i in range(0,12):
        if (i+1) in di:
            print("    Average delay for " + month_names[i] + ": " + str(round(di[i+1], 2)))

    print("END")

#debug_print:
#is essentially just a way for me to Enable/Disable
#debugging print statements all at once by hard-coding.
def debug_print(string):
    #TODO TODO TODO:
    #Hardcoding True to print debug statements.
    #Change to False for final build.
    if False:
        print(string)


#Call main if this file is the original running file:
if __name__ == "__main__":
    main()
