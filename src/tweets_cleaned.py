#!/usr/bin/env python
'''
Part of the INSIGHT coding challenge.

This script will clean and extract the text from the raw JSON tweets
that come from a file, and track the number of tweets that contain unicode.
'''

import os
import re
import sys
import json

# check the CLI arguments
arguments = sys.argv 
if len(arguments) < 3:
    print "Give me some more arguments to do my work ;)"
    print "\tUsage: "
    print "\t#python ", __file__, "/path/to/source/file /path/to/dst/file"
    sys.exit(0)
else:
    try:
        open(str(arguments[1]), 'r')
    except Exception: #IOError
        print "I got lost trying to find this file ", arguments[1]
        print "Please point me into the right direction"
        sys.exit(0)

source_file = arguments[1]
target_file = arguments[2]

# this is the main function
def ft1(source, target):
    '''
    Main function of the script.
    
    Algorithm description:
    
    1. Read from the source file one line (tweet) at a time
    2. The line will be parsed and encoded as JSON format
    3. Some lines may not have the necessary keys, so we need to check for that
    4. If the line does NOT contain the keys we are interested in, skip it (take another line)
    5. If the line contains the keys we are interested in, we will retrieve the values
       at 'created_at' (timestamp)  and 'text' (the content of the tweet)
    6. We clean the contents using [cleanString] function
    7. Next we check if the string returned at the previous step has non-ASCII characters
    8. If the contents of the extracted text (from key 'text') has only ASCII characters,
       remove escape characters and new-lines - this is achieved by function [transformString]
    9. If the contents of the extracted text (from key 'text') has extra characters (other than ASCII),
       remove those characters, remove escapes and new-lines - this is achieved by function [transformString].
       At this step we also increment the unicode tweets counter
    10.Append the line to the text file with clean tweets
    11.All lines were curated and clean, so it's time to write the number of tweets at the end of the file
    '''
    
    unicode_tweets = 0                                  # start with 0 unicode tweets
    
    f = open(target, "a")                               # open the target file
    
    for line in open(source, 'r').readlines():          # loop one line at a time
        if ('created_at' not in cleanString(line) or 'text' not in cleanString(line)):
            continue                                    # some of the tweets, or entries may not fit the pattern we are looking for 
        else:
            timestamp = cleanString(line)['created_at'] # retrieve the value of the 'created_at' key
            record = cleanString(line)['text']          # retrieve the value of the 'text' key 

            if(onlyAscii(record)):                      # check if the value of 'text' key has only ASCII characters
                record = transformString(record, True)  # transform the string
            else:
                record = transformString(record)        # transform the string
                unicode_tweets += 1                     # increment the counter for unicode tweets
    
            s = "%s (timestamp: %s) \n" % (record, timestamp) # clean string  
            f.write(s)                                  # write to file the clean string
    
    s_unicode = "\n %d tweet(s) contained unicode" % unicode_tweets
    f.write(s_unicode)                                  # write to file the number of unicode tweets

def cleanString(twitter_line):
    '''
    This function will prepare a string for JSON encoding
    There are values not surrounded by quotes eg: ["favorited":false]
    Due to these values, the string will not be properly encoded as JSON
    
    The function will return a dictionary (JSON format)
    '''
    
    #pattern = re.compile(r":([a-zA-Z]{1,}),")          # the pattern of the strings not surrounded by quotes
    pattern = re.compile(r":(false|true|null),")        # the pattern of the strings not surrounded by quotes
    clean_line = pattern.sub(r':"\1",',twitter_line)    # surrounding the matched pattern with quotes
    json_line = json.loads(clean_line)                  # load the line in JSON format
    
    return json_line

def onlyAscii(text):
    '''
    This function will return True if all characters in the text are ASCII,
    and False otherwise.
    '''

    try:
        ascii_line      = len(text.decode('unicode_escape').encode('ascii', 'ignore'))  # check the length of the string when all characters are ASCII
        unicode_line    = len(text.encode('ascii', 'ignore').decode('unicode_escape'))  # some characters are converted into their unicode representation
        
        return ascii_line == unicode_line

    except Exception as e:      # return False if their length is not the same
        return False
        raise                   # do you really need this???

def transformString(text, only_escapes = False):
    '''
    This function will clean the text received.
    If the text contains non-ASCII characters, they will be striped off
    Empty lines and new lines will be removed also.
    Finally, escape characters will be removed and return a clean string
    '''
    
    if(not only_escapes):           # this will cleanup the non-ASCII characters
        text = ''.join([x for x in text if ord(x) < 128])
        
    text = re.sub(r'\s+|\r|\n|\t',' ',text)    # residue empty lines, new lines
    
    escapes = re.compile(r'(\\|\n){1,}(.)')  # this is the pattern for the escape character
    
    return escapes.sub(r'\2',text)


# the moment of truth; may the FUNCTION1 be with you
ft1(source_file, target_file)
