#!/usr/bin/env bash -x


# the input to the Python script is a file with uncurated tweets
# the otput is a file with clean tweets

echo Starting to clean the tweets
python $PWD/src/tweets_cleaned.py $PWD/tweet_input/tweets.txt $PWD/tweet_output/ft1.txt

# the input is the file with clean tweets
# the output is a file with the averege degree of the graph

echo Creating the graph
python $PWD/src/average_degree.py $PWD/tweet_output/ft1.txt $PWD/tweet_output/ft2.txt

echo DONE!!! Have a nice day.
