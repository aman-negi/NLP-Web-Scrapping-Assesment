import nltk

# nltk.download('averaged_perceptron_tagger')
# nltk.download('stopwords')
# nltk.download('punkt')

import pandas as pd

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
import re



# TASK 1 -> Sentiment Analysis
sia = SentimentIntensityAnalyzer()

# Create A positive negative Word Dictionary
def createDictionary(filtered_sentence):
    pos_dic =[]
    neg_dic = []
    for i in filtered_sentence:
        # We check the polarity score of each word and based on that decide wether its +ve or -ve
        score = sia.polarity_scores(i)
        if(score['compound'] >0):
            pos_dic.append(i)
        elif(score['compound']<0):
            neg_dic.append(i)
    return pos_dic,neg_dic
    
# Calculate Various Polarity scores
    
def ScoreCalculator(filtered_sentence):
    pos_score = 0
    neg_score = 0
    pol_score = 0
    sub_score = 0
    for i in filtered_sentence:
        score = sia.polarity_scores(i)
        if(score['compound'] >0):
            pos_score += 1
        elif(score['compound']<0):
            neg_score -= 1
    
    neg_score = neg_score * (-1)
    pol_score = (pos_score - neg_score)/ ((pos_score + neg_score) + 0.000001)
    sub_score = (pos_score + neg_score)/ ((len(filtered_sentence)) + 0.000001)
    
    return pos_score,neg_score,pol_score,sub_score
  

def sentimentAnalysis(content):
        
    # Convert our file text to tokens
    word_tokens = word_tokenize(content)
    stop_words = set(stopwords.words('english'))
    # remove the stop words
    filtered_sentence = [w for w in word_tokens if (not w.lower() in stop_words) and len(w) >1 ]

    # get the list of positive and negative words in the sentence
    pos_dic,neg_dic = createDictionary(filtered_sentence)

    pos_score,neg_score,pol_score,sub_score = ScoreCalculator(filtered_sentence)

    
    return pos_score,neg_score,pol_score,sub_score,len(filtered_sentence)
    
    
 

def syllable_count(word):
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count += 1
    return count



def readabilityAnalysis(content):
    # sentenceList = list(sent_tokenize(content))
    sentenceList = [ i for i in list(re.split('[\n.]', content)) if len(i) > 2 ] 
    
    totalWords = 0
    totalSentence = len(sentenceList)
    complexWord = 0
    syllable_per_word = 0
    total_len_word = 0
    total_PRP = 0
    for i in sentenceList:
        wordList=[j for j in list(re.split('[ \n]', i)) if(len(j) > 0)]
        # to find the totalword we created a list of words
        totalWords += len(wordList)
        
        # Count The no. Of Personal Pronouns
        for k in list(nltk.pos_tag( wordList)):
            if(k[1] =='PRP'):
                total_PRP+=1
        
        # for complex words we are checking wether they have syllables in it or not
        for word in wordList:
            total_len_word += len(word)
            syllable_per_word += syllable_count(word)
            if(syllable_count(word)>2):
                complexWord+=1 
                    
    avg_sen_len = totalWords/totalSentence
    syllable_per_word /= totalWords 
    avg_word_len = total_len_word/totalWords
    return avg_sen_len,complexWord,totalWords,syllable_per_word,avg_word_len,total_PRP
  
  
  
def textAnalysisTask(filePath):

    with open(filePath,encoding="utf-8") as f:
        content = f.read()
    content = content.casefold()    
    
    # Task 1 Sentiment Analysis on our data
    pos_score,neg_score,pol_score,sub_score,totalfilteredWords = sentimentAnalysis(content)
    
    # Task 2 Get the various counts
    avg_sen_len, totalcomplexWord, totalWords, syllable_per_word,avg_word_len,total_PRP = readabilityAnalysis(content)
    per_comp_word = totalcomplexWord/totalWords
    fog_index = 0.4 * (avg_sen_len + per_comp_word)
    
    AnalysisDic = {}
    AnalysisDic['pos_score'] = pos_score
    AnalysisDic['neg_score'] = neg_score
    AnalysisDic['pol_score'] = pol_score
    AnalysisDic['sub_score'] = sub_score
    AnalysisDic['totalfilteredWords'] = totalfilteredWords
    AnalysisDic['avg_sen_len'] = avg_sen_len
    AnalysisDic['totalcomplexWord'] = totalcomplexWord
    AnalysisDic['syllable_per_wordv'] = syllable_per_word
    AnalysisDic['avg_word_len'] = avg_word_len
    AnalysisDic['total_PRP'] = total_PRP
    AnalysisDic['per_comp_word'] = per_comp_word
    AnalysisDic['fog_index'] = fog_index
    
    return AnalysisDic
    
def main():
    print("main")
    df = pd.read_excel("Output Data Structure.xlsx")
    
    print(df.head())
    n,m = df.shape
    for i in range(0,n):
        filePath = f"articleData/{df['URL_ID'][i]}.txt"
        try:
            result = textAnalysisTask(filePath)
            df['POSITIVE SCORE'][i] = result['pos_score']
            df['NEGATIVE SCORE'][i] = result['neg_score']
            df['POLARITY SCORE'][i] = result['pol_score']
            df['SUBJECTIVITY SCORE'][i] = result['sub_score']
            df['AVG SENTENCE LENGTH'][i] = result['avg_sen_len']
            df['PERCENTAGE OF COMPLEX WORDS'][i] = result['per_comp_word']
            df['FOG INDEX'][i] = result['fog_index']
            df['AVG NUMBER OF WORDS PER SENTENCE'][i] = result['avg_sen_len']
            df['COMPLEX WORD COUNT'][i] = result
            df['WORD COUNT'][i] = result['totalfilteredWords']
            df['SYLLABLE PER WORD'][i] = result['totalcomplexWord']
            df['PERSONAL PRONOUNS'][i] = result['total_PRP']
            df['AVG WORD LENGTH'][i] = result['avg_word_len']
        except:
            pass
        
    df.to_excel("Result_Output_Data_Structure.xlsx")
    print("Successfully Done the analysis")

        
    
    
    
    
        
main()
    
    