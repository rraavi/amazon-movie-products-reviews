import nltk
import random
import operator
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange,MonthLocator,date2num
from matplotlib.legend_handler import HandlerLine2D

#finds bag of words in the document
def find_features(document):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features

#generates corresponding lists for date, positive and negative reviews
def convert_tuple_list(list_tuple_pos,list_tuple_neg):
    list_date_unix = []
    list_freq_unix = []
    list_freq_unix_neg = []
    print list_tuple_neg
    for (date_unix,freq) in list_tuple_pos:
        list_date_unix.append(date_unix)
        list_freq_unix.append(freq)
    for date_unix_neg,freq_neg in list_tuple_neg:
        if date_unix_neg in list_date_unix:
            list_freq_unix_neg.append(freq_neg)
    return list_date_unix,list_freq_unix,list_freq_unix_neg

#code for plotting the graph based on the generated data
def plot_graph(data):
    list_date,list_freq_emotions,list_freq_emotions_neg = data
    dates_list_formatted = []
    print list_freq_emotions
    print list_freq_emotions_neg
    for unix_date in list_date:
        dates_list_formatted.append(date2num(datetime.datetime.utcfromtimestamp(unix_date)))
    print dates_list_formatted
    fig, ax = plt.subplots()
    line1, =ax.plot_date(dates_list_formatted, list_freq_emotions,'-o',label='Positive Reviews')
    ax.plot_date(dates_list_formatted, list_freq_emotions_neg,'-ro',label='Negative Reviews')
    plt.legend(handler_map={line1: HandlerLine2D(numpoints=2)})
    ax.set_xlim(dates_list_formatted[0], dates_list_formatted[-1])
    # The hour locator takes the hour or sequence of hours you want to
    # tick, not the base multiple
    ax.xaxis.set_major_locator(MonthLocator(interval=12))
    ax.xaxis.set_minor_locator(MonthLocator())
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
    fig.autofmt_xdate()
    plt.xlabel('Time in years')
    plt.ylabel('No of Reviews')
    plt.title('Trend Analysis')
    plt.show()

def define_years_unixTime(unix_time_value_str):
    # print unix_time_value_str
    unix_time_value = int(unix_time_value_str)
    # int(unix_time_value)
    x = 0
    if unix_time_value >1104537600 and unix_time_value <1136073600:         #2005-06
        x =  1104537600
    elif unix_time_value >1136073600 and unix_time_value <1167609600:       #2006-07
        x =  1136073600
    elif unix_time_value >=1167609600 and unix_time_value <1199145600:      #2007-08
        x =  1167609600
    elif unix_time_value >=1199145600 and unix_time_value <1230768000:      #2008-09
        x =  1199145600
    elif unix_time_value >=1230768000 and unix_time_value <1262304000:      #2009-10
        x =  1230768000
    elif unix_time_value >=1262304000 and unix_time_value <1293840000:      #2010-11
        x =  1262304000
    elif unix_time_value >=1293840000 and unix_time_value <1325376000:      #2011-12
        x =  1293840000
    elif unix_time_value >=1325376000 and unix_time_value <1356998400:      #2012-13
        x =  1325376000
    return x

def trendAnalysis(list_tuples_unixtime_emotion):
    dict_pos = {}
    dict_neg = {}
    for (unixtime,emotion_tag) in list_tuples_unixtime_emotion:
        base_year = define_years_unixTime(unixtime)
        if emotion_tag == 'pos':
            if base_year in dict_pos:
                dict_pos[base_year] += 1
            else:
                dict_pos[base_year] = 1
        else:
            if base_year in dict_neg:
                dict_neg[base_year] += 1
            else:
                dict_neg[base_year] = 1
    sorted_x_pos = sorted(dict_pos.items(), key=operator.itemgetter(0))
    sorted_x_neg = sorted(dict_neg.items(), key=operator.itemgetter(0))
    return sorted_x_pos,sorted_x_neg
f = open('Cars_data.txt', 'r')                       #check and place the correct path containing the dataset file
t = []
t_emotions = []
all_words = []
flag = 0
list_time_stamp = []
for line_seq_file in f:
    if line_seq_file.find('product/productId:') > -1:
        flag = 0
    if line_seq_file.find('review/score') > -1:
        review_rating = line_seq_file[line_seq_file.find('review/score') + 14 : line_seq_file.find('review/score') + 17]
    if line_seq_file.find('review/text:')>-1:
        review_text = line_seq_file[line_seq_file.find('review/text:')+13:len(line_seq_file)-1]
        flag = 1
    if line_seq_file.find('review/time')>-1:
        review_date_unix = line_seq_file[line_seq_file.find('review/time')+13:line_seq_file.find('review/time')+23]
    if flag ==1:
        reviewText_words = review_text.split()
        for w in reviewText_words:
            all_words.append(w.lower())
        t.append((list(reviewText_words),review_rating))
        if float(review_rating) <= 3.0:
            emotion = 'neg'
        else:
            emotion = 'pos'
        t_emotions.append((review_date_unix,emotion))
        flag = 0

allfreq_words = nltk.FreqDist(all_words)
word_features = list(allfreq_words.keys())[:3000]
featuresets = [(find_features(rev), category) for (rev, category) in t]
print 'number of reviews = '+str(len(featuresets))
no_of_reviews = len(featuresets)
training_set = featuresets[150:]
testing_set = featuresets[:150]
classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Classifier accuracy percent:",(nltk.classify.accuracy(classifier, testing_set))*100)
classifier.show_most_informative_features(150)
list_date_frequency_pos,list_date_frequency_neg = trendAnalysis(t_emotions)
plot_graph(convert_tuple_list(list_date_frequency_pos,list_date_frequency_neg))             #plots the positive and negative review frequency