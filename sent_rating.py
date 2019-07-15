# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 17:57:01 2019

@author: RZ0001
"""
import csv
import os
import sys

def load_neg_words():
    
    neg_files = os.path.join('data', 'negative_words.csv')    
    neg_words = []
    
     # Read in the Negative words CSV file
    with open(neg_files, 'r') as csvfile:
        # Split the data on commas
        csvreader = csv.reader(csvfile, delimiter=',')

        header = next(csvreader)

        # Loop through the data
        for row in csvreader:

            #Populate the negative words array 
            neg_words.append(row[0])
            
    return(neg_words)
    
def load_pos_words():
    
    pos_files = os.path.join('data', 'positive_words.csv')    
    pos_words = []   
    
    # Read in the Positive words CSV file
    with open(pos_files, 'r') as csvfile1:
        # Split the data on commas
        csvreader1 = csv.reader(csvfile1, delimiter=',')

        header1 = next(csvreader1)

        # Loop through the data
        for row in csvreader1:
            #Populate the negative words array 
            pos_words.append(row[0])
            
    return(pos_words)
    
def cleanse_text(tw_js):
    
    tw_js = tw_js.replace(',', '')
    tw_js = tw_js.replace('(', '')
    tw_js = tw_js.replace(')', '')
    tw_js = tw_js.replace(';', '')
    tw_js = tw_js.replace('!', '')
    tw_js = tw_js.replace('#', '')
    tw_js = tw_js.replace('$', '')
    tw_js = tw_js.replace('.', '')
    tw_js = tw_js.replace('+', '')
    tw_js = tw_js.replace('-', '')
    tw_js = tw_js.replace('_', '')
    tw_js = tw_js.replace('<', '')
    tw_js = tw_js.replace('>', '')
    tw_js = tw_js.replace('*', '')
    tw_js = tw_js.replace('/', '')
    tw_js = tw_js.replace('\\', '')  
    
    return (tw_js)        
    
def get_rating(tw_js):     
    
    n_count = 0 
    p_count = 0
    
    n_data = load_neg_words()    
    #print("Number of Negative words : " + str(len(n_data)))
    
    p_data = load_pos_words()    
    #print("Number of Positive words : " + str(len(p_data)))
    
    #print("Analyzing Sentence : " + tw_js)
    tw_js = cleanse_text(tw_js)    
    #print("Cleansed Sentence : " + tw_js)
    
    for word in tw_js.split(" "):
        
        try:            
            if word.lower() in n_data:
                n_count = n_count + 1
                #print("Negative Word : " + word)
            elif word.lower() in p_data:
                p_count = p_count + 1
                #print("Positive Word : " + word)                
        except:            
            print ("Non Ascii Character : " + word)
            
    if ( n_count < p_count):
        print ("Positive Tweet : " + str(p_count))
        return ("Positive")
    elif ( n_count > p_count):
        print ("Negative Tweet : " + str(n_count))
        return ("Negative")
    elif (n_count == p_count ):
        print ("Neutral Tweet : " + " Positive : " +  str(p_count) + " Negative : " + str(n_count) )
        return ("Neutral")      
    
if __name__ == "__main__":    
    get_rating(str(sys.argv[1]))

    
        
    
    
    
    