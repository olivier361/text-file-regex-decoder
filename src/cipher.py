"""
In this file, you need to add your FileDecoder class
See readme.md for details

WE WILL EVALUATE YOUR CLASS INDIVIDUAL, SO MAKE SURE YOU READ
THE SPECIFICATIONS CAREFULLY.
"""

#cipher.py
#by Olivier Gervais-Gougeon

import string #NOTE: Only used for the testing() function.

class DecryptException(Exception):
    #Called when there's some sort of error in decrypting
    #the given file with the given key and alphabet.
    pass

class FileDecoder:

    def __init__(self, key, filename, alphabet):
        self.key = key              #the password for decryption
        self.filename = filename    #the file to decrypt
        self.alphabet = alphabet    #the alphabet used in the file and key
        self.decrypted_lines = []   #stores the decrypted file as a list of lines.
        self.line_counter = 0       #counts the number of lines (differs from len() by 1 due to implementation)

    #debug_print2:
    #is essentially just a way for me to Enable/Disable
    #debugging print statements all at once by hard-coding.
    def debug_print2(self, string):
        #TODO TODO TODO:
        #Hardcoding True to print debug statements.
        #change to False for final build.
        if False:
            print(string)

    #decode():
    #attempts to decrypt the given file. Raises a DecryptException
    #if a decryption error occurs or if the result is not properly decrypted.
    def decode(self):
        self.debug_print2("Attempting to decode file...")
        
        #Open file for reading. If it fails stop function:
        file_buffer = None
        self.decrypted_lines = [] #reset if previous decoded lines were already here.

        try:
            file_ptr = open(self.filename, "r")
            file_buffer = file_ptr.read()
            #print(file_buffer)
            file_ptr.close()
        except:
            raise DecryptException("unable to open " + str(self.filename) + " for reading")
            self.debug_print2("Continue after raise exception!!!")
            return
        
        #declare variable used for the decryption process:
        decrypted_buffer = ""
        alphabet_len = len(self.alphabet)
        key_len = len(self.key)
        cursor = 0        

        #Decrypt the file with the given key & alphabet:
        #source: https://stackoverflow.com/questions/2294493/how-to-get-the-position-of-a-character-in-python
        for char in file_buffer:
            try:
                shift = self.alphabet.index(self.key[cursor%key_len])
            except ValueError:
                #self.debug_print2("ERROR: A character in the key is not part of the supplied alphabet")
                raise DecryptException("Failed to decrypt file: A character in the password is not part of the supplied alphabet. Please provide another password.")
            try:
                new_char_val = int(self.alphabet.index(char) - shift)
            except ValueError:
                raise DecryptException("Failed to decode file: A character in the file is not part of the supplied alphabet. Press 'q' to exit and re-run with a different file.")

            try:
                decrypted_buffer +=  self.alphabet[new_char_val%alphabet_len]
            except:
                raise DecryptException("ERROR in FileDecoder.decode(): Index out of bounds for given alphabet. This shouldn't be possible.")            

            cursor += 1
        
        #self.debug_print2("decrypted_buffer is:\n" + decrypted_buffer)

        #Split the decrypted file into lines stored in a list:
        self.decrypted_lines = decrypted_buffer.split("\n")
        
        #self.debug_print2(self.decrypted_lines[0])
        self.debug_print2("number of lines found: " + str(len(self.decrypted_lines)))


        #check that the file has been decoded into a valid CSV ferry file by checking the first line:
        check_header = "departure_terminal,arrival_terminal,vessel_name,scheduled_departure_year,scheduled_departure_month,scheduled_departure_day,scheduled_departure_hour,scheduled_departure_minute,actual_departure_year,actual_departure_month,actual_departure_day,actual_departure_hour,actual_departure_minute,arrival_year,arrival_month,arrival_day,arrival_hour,arrival_minute" 
 
        try:
            if self.decrypted_lines[0] == check_header:
                self.debug_print2("File was decoded successfully.")
                return
            else:
                raise DecryptException("The given file could not be decoded with the given password. Please provide another password.")
        except IndexError as e:
            self.debug_print2(e)
            raise DecryptException("The given file could not be decoded with the given password. Please provide another password.")
 

    #print_lines(start, end):
    #prints the lines from the decoded file as a list. Use start/end parameters to specify
    #which range of lines to print. Parameters out of bounds will
    #be auto-adjusted by the function. Mostly used for debugging.
    def print_lines(self, start, end):
        count = 0
        print("Printing decrypted lines " + str(start) + " to " + str(end) + " of file " + str(self.filename) + ":")
        try:
            for row in self:
                if count >= start and count <= end:
                    print(row)
                count += 1
        except DecryptException as e:
            print(e)
        print("iterated though " + str(count) + " lines while printing.")
 

    #__str__:
    #defines how the string representation of an instance is defined.
    #this is what is used for print(<instance of this class>).
    def __str__(self):
        return "FileDecoder(key='" + str(self.key) + "', file='" + str(self.filename) + "')"

    #__repr__:
    #defines how the string representation of an instance is defined in a developer context.
    #this is what is used for printing a list containing instances of this class.
    def __repr__(self):
        return "FileDecoder(key='" + str(self.key) + "', file='" + str(self.filename) + "')"


    # __len__:
    #defines the result of calling len() on a FileDecoder instance.
    def __len__(self):
        try:
            self.decode()
            return len(self.decrypted_lines)-1
            #doing len()-1 since the way the split("\n") in decode() works,
            #it always adds an empty list (aka "extra line") for the
            #last newline in the file.
        except DecryptException:
            return 0

    #__iter__:
    #Used to iterate through the lines of the decoded file.
    def __iter__(self):
       self.decode()
       self.line_counter = 0
       while self.line_counter < len(self.decrypted_lines):
            yield self.decrypted_lines[self.line_counter].split(",")
            self.line_counter += 1
            

def testing():
    alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation + " \n"

    print("Testing print() on a FileDecoder instance:")
    fd = FileDecoder(key="A00!$a", filename="../cases/ferry1.out", alphabet=alphabet)
    print(fd)

    print("Testing print() on a list containing a FileDecoder instance")
    list = [fd]
    print(list)

    print("testing file read by calling decode()")
    try:
        fd.decode()
        pass
    except DecryptException as e:
        print("Caught DecryptException: an error decrypting the file occured.")
        print(e)

    #print("521%3 = " + str(521%3) + " (should be 2).")
    try:
        count = 0
        for row in fd:
            if count%50 == 0:
                print(row)
            count += 1
        print("iterated though " + str(count) + " lines.")
    except DecryptException as e:
        print("Exception Caught while testing iteration.")
        print(e)

    print("Length of FileDecoder instance using __len__ is: " + str(len(fd)))


#TODO TODO TODO:
#remember to comment this out for final build.

#testing()


