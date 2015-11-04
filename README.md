# coding-challenge

## Insight Data Science Coding Challenge

This challenge is to implement two features:

1. Clean and extract the text from the raw JSON tweets that come from the Twitter Streaming API, and track the number of tweets that contain unicode.
2. Calculate the average degree of a vertex in a Twitter hashtag graph for the last 60 seconds, and update this each time a new tweet appears.

## Structure of this repo

├── README.md  
├── run.sh  
├── src  
│   ├── average_degree.py  
│   └── tweets_cleaned.py  
├── tweet_input  
│   └── tweets.txt  
└── tweet_output  
    ├── ft1.txt  
    └── ft2.txt  

## Info

1. Feature 1
2. Feature 2
3. Run the scripts

### Feature 1

> For challenge 1, the script can be found at `src/tweets_cleaned.py`.

> The following libraries were used:
* [os](https://docs.python.org/2/library/os.html)
* [re](https://docs.python.org/2/library/re.html)
* [sys](https://docs.python.org/2/library/sys.html)
* [json](https://docs.python.org/2/library/json.html)

> Explanation of the algorithm:
    1. Read from the source file one line (tweet) at a time
    2. The line will be parsed and encoded as JSON format
    3. Some lines may not have the necessary keys, so we need to check for that
    4. If the line does NOT contain the keys we are interested in, skip it (take another line)
    5. If the line contains the keys we are interested in, we will retrieve the values at `created_at` (timestamp)  and `text` (the content of the tweet)
    6. We clean the contents using `cleanString` function
    7. Next we check if the string returned at the previous step has non-ASCII characters
    8. If the contents of the extracted text (from key `text`) has only ASCII characters, remove escape characters and new-lines - this is achieved by function `transformString`
    9. If the contents of the extracted text (from key `text`) has extra characters (other than ASCII), remove those characters, remove escapes and new-lines - this is achieved by function `transformString`. At this step we also increment the unicode tweets counter
    10. Append the line to the text file with clean tweets
    11. All lines were curated and clean, so it's time to write the number of tweets at the end of the file

> How to use the script independently

```
# cd src/
# python tweets_cleaned.py ../tweet_input/tweets.txt ../tweet_output/ft1.txt
```

The output will be in `tweet_output/ft1.txt` file.

### Feature 2

> For challenge 2, the script can be found at `src/average_degree.py`.

> The following libraries were used:
* [os](https://docs.python.org/2/library/os.html)
* [re](https://docs.python.org/2/library/re.html)
* [sys](https://docs.python.org/2/library/sys.html)
* [time](https://docs.python.org/2/library/time.html)
* [itertools](https://docs.python.org/2/library/itertools.html)
* [igraph](http://igraph.org/python/)
* [datetime](https://docs.python.org/2/library/datetime.html)

> Explanation of the algorithm:

    1. Read from the source file one line (tweet) at a time
    2. The line (tweet) is being curated based on the `cleanData` function
    3. The curated line (tweet) with more than 1 hashtag will be returned in the form of a dictionary containing a list of hashtags, the timestamp and a list of edges formed between hashes
    4. The line is appended to a master stack list (`L`) - this stack will hold 60sec worth of tweets
    5. Check if there are any tweets older than 60 sec compared with the latest tweet
    6. If any old tweets, pop the first entry in the master list
    7. Else go on with checking if the new line (tweet) can contribute any new vertices (hashtags) to the master vertices list (`V`)
    8. Extend the master vertices list (V) with the new unique hashtags
    9. Create an adhoc list (E) of possible edges from all the tweets in the master list (`L`) This list will always be emptied when a new line (tweet) will be parsed
    10. The function `createGraph` will create a new graph based on the new edges (`E`) and vertices (`V`)
       and at the same time return the average degree of the graph
    11. The return from `createGraph` is written to file

> How to use the script independently

```
# cd src/
# python average_degree ../tweet_output/ft1.txt ../tweet_output/ft2.txt
```

**NOTE!!!** The input for this script is the file with all cleaned tweets that results from running the previous script

The output will be in `tweet_output/ft2.txt` file.

### Run the scripts

Alternatively you could run both scripts using the `run.sh` script in this folder.

```
# ./run.sh
```

**ENJOY!!!**
