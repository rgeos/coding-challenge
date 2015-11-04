#!/usr/bin/env python

'''
Part of the INSIGHT coding challenge.

This script will calculate the average degree of a vertex
in a Twitter hashtag graph for the last 60 seconds,
and update this each time a new tweet appears.
'''

import os
import re
import sys
import time
import itertools
from igraph import *
from datetime import datetime

# check the CLI arguments
arguments = sys.argv 
if len(arguments) < 3:
    print "Give me some more arguments to do my work ;)"
    print "\tUsage: "
    print "\t#python ", __file__, "/path/to/source/file /path/to/dst/file"
    sys.exit(0)
else:
    try:
        open(arguments[1], 'r')
    except Exception: #IOError
        print "I got lost trying to find this file ", arguments[1]
        print "Please point me into the right direction"
        sys.exit(0)

source_file = arguments[1]
target_file = arguments[2]



# this is the main function
def ft2(source,target):
    '''
    Main function of the script.
    
    Algorithm description:
    
    1. Read from the source file one line (tweet) at a time
    2. The line (tweet) is being curated based on the [cleanData] function
    3. The curated line (tweet) with more than 1 hashtag will be returned in the form of a dictionary
       containing a list of hashtags, the timestamp and a list of edges formed between hashes
    4. The line is appended to a master stack list (L) - this stack will hold 60sec worth of tweets
    5. Check if there are any tweets older than 60 sec compared with the latest tweet
    6. If any old tweets, pop the first entry in the master list
    7. Else go on with checking if the new line (tweet) can contribute any new vertices (hashtags)
       to the master vertices list (V)
    8. Extend the master vertices list (V) with the new unique hashtags
    9. Create an adhoc list (E) of possible edges from all the tweets in the master list (L)
       This list will always be emptied when a new line (tweet) will be parsed
    10.The function [createGraph] will create a new graph based on the new edges (E) and vertices (V)
       and at the same time return the average degree of the graph
    11.The return from [createGraph] is written to file
    '''
    
    f = open(target, "a")                   # this is the target file where we write the average degree of the graph
    
    V = []                                  # master list with all the unique hashtags instantiated empty
    L = []                                  # master list with all the data from the last 60 sec instantiated empty

    for line in open(source,'r').readlines(): # loop one line at the time, reading from the source file
    
        E = []                              # master list of all the edges is reset every time we get a new tweet
        
        l = cleanData(line)                 # the line (tweet) is being cleaned up and returned as dictionary   
        #print l

        if(l):                              # if the line (tweet) has data append it to the master list L
            L.append(l)                     # append
            
            # we need to check if the first entry in the master list is older than 60 sec compared with the latest
            while ((L[-1]['timestamp'] - L[0]['timestamp'] > 60) and (L[-1]['timestamp'] > L[0]['timestamp'])):
                del L[0]                    # remove the first entry in the master list
            
            D = uniqueTags(V, l['tags'])    # return the difference of elements between the master vertex list and the new entry
            V.extend(D)                     # append unique hashtags to V as vertices
            
            # we create a list of edges based on the current entries in the master list L
            E = list(set(itertools.chain.from_iterable([i['edges'] for i in L])))
            
            # draw the graph and calculate the average degree
            average_degree = createGraph(E, V)

            f.write(str(average_degree)+'\n')    # write to file and we are done with this line

def cleanTimestamp(timestamp):
    '''
    This function will transform the timestamp
    into epoch format for ease of calculation
    
    Returns the time in seconds in POSIX format
    '''
    
    date_format = '%a %b %d %H:%M:%S %Y'                    # this is the desired time format
    strip_offset = re.sub(r"[+-]([0-9])+", "", timestamp)   # we strip the offset I always got an error trying to parse it
    
    t = datetime.strptime(strip_offset, date_format)        # this is the time format that we need (POSIX format)
    
    return int(time.mktime(t.timetuple()))                  # time in seconds since the dawn of time (sort of)

def cleanData(line):
    '''
    This function will parse and curate the lines (tweets)
    If one line (tweet) has more than 1 hashtag, this function
    will return a dictionary with 3 keys:
        - tags:        all hashtags in that particular line (tweet)
        - timestamp:   the timestamp in POSIX format of the tweet
        - edges:       all possible unique combinations between vertices (a,b) == (b, a) 
    '''
    
    pattern_hash = re.compile(r'(#\w{1,})')                 # pattern for hashtags
    pattern_timestamp = re.compile(r'\(timestamp: (.*)\)')  # pattern for timestamp
    
    match_hash = set([x.lower() for x in pattern_hash.findall(line)]) # all unique matches for hashtags in lower cases
    match_timestamp = pattern_timestamp.findall(line)       # all mathches for timestamp (it should be only 1)
    
    h = list(match_hash)                                    # create a list of hashtags
    
    try:    # hey Python, you can't handle an empty line on your own, really ????
        t = cleanTimestamp(match_timestamp[0])              # timestamp is always on the first position
    except Exception:
        t = '0000000000'
        
    e = list(itertools.combinations(match_hash,2))          # create a list of all possible edges by using combinations of 2
    
    if len(match_hash) > 1:                                 # check if we have more than 1 hashes and return a dict if true
        return {"tags": h, "timestamp": t, "edges": e}      # here we will return all unique hashtags

def uniqueTags(l1, l2):
    '''
    This function will return the difference between 2 lists
    It is used for updating the master vertices list (V)
    '''
    # this looks UGLY
    intersection = [val for val in l2 if val in l1]             # common hashes between the two lists
    difference = [val for val in l2 if val not in intersection] # different hashes
    
    return difference

def createGraph(e,v):
    '''
    This function will create a new graph every time is called.
    It will return the degree of the graph
    '''
    g = Graph()                             # instantiating the graph
    
    for i in v: g.add_vertex(i)             # creating the vertices
    for i in e: g.add_edge(i[0],i[1])       # add a link between the vertices
    
    try:
        return round(sum(g.degree())/float(len(g.degree())),2) 
    except Exception:
        return 0



# the moment of truth; may the FUNCTION2 be with you
ft2(source_file, target_file)