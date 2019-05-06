# cp Clone in Python
# By josh Rachford
#

import sys
import os
import getopt


FILE_NOT_FOUND, OVERWRITE, USAGE_ERROR, COPY_ERROR, DIRECTORY_EXISTS = 'FILE_NOT_FOUND', 'OVERWRITE', 'USAGE_ERROR', 'COPY_ERROR', 'DIRECTORY_EXISTS'

# Default values    
verbose, directory_tree, no_overwrite = False, False, False

def copyfile (source, target):
    global verbose

    try:
        source_file = open(source)
        target_file = open(target, "w")

        for x in source_file:
            target_file.write(x)
    
        target_file.close()
        source_file.close()
        if verbose:
            print(source + " -> " + target)
    except:
        resultMessage(COPY_ERROR, (source, target))
        
def resultMessage(error_code, content):
    if error_code == FILE_NOT_FOUND:
        try:
            print ("%s: No such file or directory." % content)
        except:
            print ("No such file or directory.")
    elif error_code == OVERWRITE:
        print ("Will not overwrite file!")
    elif error_code == USAGE_ERROR or error_code == FILE_NOT_FOUND:
        print ("usage: jcp.py [-R] [-H] [-n] source_file target_file")
        print ("       jcp.py [-R] [-H] [-n] source_file target_directory")
    elif error_code == COPY_ERROR:
        print("Error copying!")
        print(content)
    elif error_code == DIRECTORY__EXISTS:
        print("Directory exists!")
    else:
        print (error_code, content)
    exit()

def copydir (source, target):
    # get globals
    global verbose
    global directory_tree
    
    # source is a directory
    if os.path.isdir(target):
        ###
        resultMessage(DIRECTORY_EXISTS, 0)
    else:
        if directory_tree:
            try:
                os.mkdir(target)
                for x in os.listdir(source):
                    if os.path.isdir(source + "/" + x):
                    
                        if verbose:
                            print (source + "/" + x + " -> " + target + "/" + x)
                        copydir(source + "/" + x, target + "/" + x)
                    
                    elif os.path.isfile(source + "/" + x):
                        copyfile(source + "/" + x, target + "/" + x)
            
            except:
                print "Error copying!"
    
# Get arguments

#try:
options, args = getopt.getopt(sys.argv[1:], 'RHvn', ['','help', 'verbose'])

#except:
 #   print ("couldn't get options and args")
    
try:
    #options, args = getopt.getopt(sys.argv[1:], '-H', 'help')

#    print (options, args)
#    print len(args)
    #if len(args) == 0:
    #   resultMessage(USAGE_ERROR, 0)
    #  exit()
        
    for opt, value in options:
        if opt == '-H':
            resultMessage(USAGE_ERROR, 0)
        elif opt == '-v':
            verbose = True
        elif opt == '-R':
            directory_tree = True
        elif opt == '-n':
            no_overwrite = True

    # If there are exactly two arguments
    if len(args) == 2:

        # What kind of arguments are they? Files, directories, or neither?
        if os.path.isfile(args[0]):
            # It's a file!
            # For now, let's not overwrite stuff
            # real cp does overwrite stuff
            if os.path.isfile(args[1]) and no_overwrite:
                if verbose:
                    print ("%s not overwritten" % args[1])
                # could replace by opening file in x mode
            elif os.path.isdir(args[1]):
                copyfile (args[0], args[1] + "/" + args[0])
                
            else:
                # Seems to be no problem. Copy it!
                try:
                    copyfile(args[0], args[1])
                except:
                    print("Mysterious copy error!")
                    
        elif os.path.isdir(args[0]):
            # It's a directory!                            
            # Again, not going to overwrite a target
            # The cp implementation on my MacBook returns:
            # cp: foo is a directory (not copied).
                    
            if os.path.exists(args[1]):
                if verbose:
                    print ("%s not overwritten" % args[1])
            elif len(args[1]) > 0:    
                copydir(args[0], args[1])
                
        else:
            resultMessage(FILE_NOT_FOUND, args[0])
    elif len(args) == 1:
        resultMessage(USAGE_ERROR, 0)
        #print ("%s: No such file" % arguments[0])
           # print ("Usage: cp source_file target_file")
    
    
except getopt.error, msg:
    resultMessage(USAGE_ERROR, 0)


