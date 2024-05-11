# Import the libraries
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
import syllapy
import string
import nltk
import re

# import the data and make a copy
articles = pd.read_csv('combined.csv')
df = articles.copy()

# delete leading and trailing spaces
df['text'] = df['text'].str.strip()


# Sentimental Analysis

# Remove special html characters \r \n \xa0
def clean_text(text):
    cleaned_text = re.sub(r'[\r\n\t\xa0]+', ' ', text)
    return cleaned_text


df['text'] = df['text'].apply(clean_text)

# Making a copy of data for personal pronouns metric
metric_df = df.copy()

# lower text
df['text'] = df['text'].str.lower()

# remove words that start with a number and ends with a number
pattern = r'\b\d+\b'
df['text'] = df['text'].str.replace(pattern, '', regex=True)

# Tokenize the text using NLTK library to create a list of words.
df['text'] = df['text'].apply(word_tokenize)

# Creating a copy of the dataframe for other text analysis where we need sentence and word lengths
seo_analysis = df.copy()

# Extracting the stop words from files

# StopWords_Auditor
stopwords_auditor = []
with open('StopWords/StopWords_Auditor.txt', 'r') as file:
    for line in file:
        stopwords_auditor.append(line.strip())

# StopWords_Currencies | (Assuming only the currency needs to be removed)
stopwords_currencies = []
with open('StopWords/StopWords_Currencies.txt', 'r') as file:
    for line in file:
        stopwords_currencies.append(line.strip())

stopwords_currencies = [s.split('|')[0].strip() for s in stopwords_currencies]

# StopWords_DatesandNumbers
stopwords_datesandnumbers = []
with open('StopWords/StopWords_DatesandNumbers.txt', 'r') as file:
    for line in file:
        stopwords_datesandnumbers.append(line.strip())
stopwords_datesandnumbers = [s.split('|')[0].strip() for s in stopwords_datesandnumbers]

# StopWords_Generic
stopwords_generic = []
with open('StopWords/StopWords_Generic.txt', 'r') as file:
    for line in file:
        stopwords_generic.append(line.strip())

# StopWords_GenericLong
stopwords_genericlong = []
with open('StopWords/StopWords_GenericLong.txt', 'r') as file:
    for line in file:
        stopwords_genericlong.append(line.strip())

# Remove single alphabetic characters from the list | To remove word anchoring
stopwords_genericlong = [word for word in stopwords_genericlong if not re.match(r'^[a-zA-Z]$', word)]

# StopWords_Geographic
stopwords_geographic = []
with open('StopWords/StopWords_Geographic.txt', 'r') as file:
    for line in file:
        stopwords_geographic.append(line.strip())
stopwords_geographic = [s.split('|')[0].strip() for s in stopwords_geographic]

# stopwords_names
stopwords_names = []
with open('StopWords/StopWords_Names.txt', 'r') as file:
    for line in file:
        stopwords_names.append(line.strip())
stopwords_names = [s.split('|')[0].strip() for s in stopwords_names]

# Combine all the stop words in one list
all_stopwords = []

# Adding all stop words lists to the combined list
all_stopwords.extend(stopwords_auditor)
all_stopwords.extend(stopwords_currencies)
all_stopwords.extend(stopwords_datesandnumbers)
all_stopwords.extend(stopwords_generic)
all_stopwords.extend(stopwords_genericlong)
all_stopwords.extend(stopwords_geographic)
all_stopwords.extend(stopwords_names)

# Removing duplicates by converting the list to a set and back to a list
all_stopwords = list(set(all_stopwords))

all_stopwords = [word.lower() for word in all_stopwords]  # Converting words to lower


# Removing stop words from df
def remove_stopwords(tokens, stopwords):
    return [token for token in tokens if token not in stopwords]


# Using lambda to apply remove_stopwords on each row
df['text'] = df['text'].apply(lambda x: remove_stopwords(x, all_stopwords))

# Making the dict of positive and negative words
negative_dict = {}
positive_dict = {}

with open('MasterDictionary/negative-words.txt', 'r') as file:
    negative_words = [line.strip() for line in file if
                      line.strip() not in all_stopwords]  # Remove words that are in stopwords
    negative_dict['negative_words'] = negative_words

with open('MasterDictionary/positive-words.txt', 'r') as file:
    positive_words = [line.strip() for line in file if line.strip() not in all_stopwords]
    positive_dict['positive_words'] = positive_words


# Extracting derived variables
# Positive Score
def positive_scores(text, positive_dict):
    count = 0
    for i in text:
        if i in positive_dict['positive_words']:
            count += 1
    return count


# Apply positive_scores function on df['text'] column
df['POSITIVE SCORE'] = df['text'].apply(lambda x: positive_scores(x, positive_dict))


# Negative Score
def negative_score(text, negative_dict):
    count = 0
    for i in text:
        if i in negative_dict['negative_words']:
            count -= 1
    return count * -1


# Apply positive_scores function on df['text'] column
df['NEGATIVE SCORE'] = df['text'].apply(lambda x: negative_score(x, negative_dict))

# Polarity Score
df['POLARITY SCORE'] = round((df['POSITIVE SCORE'] - df['NEGATIVE SCORE']) / (
        (df['POSITIVE SCORE'] + df['NEGATIVE SCORE']) + 0.000001), 2)

# Subjectivity Score
df['SUBJECTIVITY SCORE'] = round((df['POSITIVE SCORE'] + df['NEGATIVE SCORE']) / ((df['text'].apply(len)) + 0.000001), 2)

# Analysis of Readability

# Assuming the stopwords mentioned earlier should not be removed
count_punctuation = lambda text: sum(text.count(p) for p in [".", "...", "!", "?"])  # Count the number of sentences
seo_analysis['sentences_count'] = seo_analysis['text'].apply(count_punctuation)


# Remove Punctuations
def count_words(tokenized_text):
    words = [token for token in tokenized_text if token not in string.punctuation]  # Filter out punctuation tokens
    return words


seo_analysis['text'] = seo_analysis['text'].apply(count_words)

# Counting the number of words for readability metrics
seo_analysis['total_words'] = seo_analysis['text'].apply(len)

seo_analysis['AVG SENTENCE LENGTH'] = round(seo_analysis['total_words'] / seo_analysis['sentences_count'], 2)


# Complex Word Count
# The remaining analysis  of readability metrics for which complex words are req

# Count the number of complex words(Words with more than 2 Syllables)
def count_complex_words(text):
    complex_word_count = 0
    for word in text:
        syllable_count = syllapy.count(word)  # Count the number of syllables in the word

        if syllable_count > 2:
            complex_word_count += 1

    return complex_word_count


seo_analysis['COMPLEX WORD COUNT'] = seo_analysis['text'].apply(count_complex_words)

seo_analysis['PERCENTAGE OF COMPLEX WORDS'] = round(seo_analysis['COMPLEX WORD COUNT'] / seo_analysis['total_words'], 2)

seo_analysis['FOG INDEX'] = round(0.4 * (seo_analysis['AVG SENTENCE LENGTH'] + seo_analysis['PERCENTAGE OF COMPLEX WORDS']), 2)

# Word Count
# Assuming that the stop words needs to be cleaned for all the metrics below

nltk.download('stopwords')  # Download the nltk stopwords

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    words = [word for word in text if word.lower() not in stop_words]
    return words

# Apply the remove_stopwords function to each row in the 'text' column
seo_analysis['text'] = seo_analysis['text'].apply(remove_stopwords)

# Word Count
seo_analysis['WORD COUNT'] = seo_analysis['text'].apply(len)

# Average Number of Words Per Sentence
seo_analysis['AVG NUMBER OF WORDS PER SENTENCE'] = round(seo_analysis['WORD COUNT'].sum() / seo_analysis['sentences_count'].sum(), 2)

# Syllable Count Per Word
# Assuming average syllable per word is needed and not a list of all syllable for every words

def count_syllables(word):
    vowels = 'aeiouy'
    # Remove trailing 'es', 'ed'
    word = re.sub(r'es$|ed$', '', word)
    # Count the vowels except for the ones that come after another vowel
    return len(re.findall(r'[aeiouy]+', word, re.IGNORECASE))

def count_syllables_in_text(tokens):
    syllable_counts = [count_syllables(word) for word in tokens]
    # Calculate the average number of syllables per word
    average_syllables = sum(syllable_counts) / len(tokens)
    return round(average_syllables, 2)

seo_analysis['SYLLABLE PER WORD'] = seo_analysis['text'].apply(count_syllables_in_text)

# Personal Pronouns
# For this we need an earlier state of data which was not converted into lower to deal with the (us and US interchange)

metric_df['text'] = metric_df['text'].apply(word_tokenize)

# Counting Pronouns
def count_personal_pronouns(tokenized_text):
    pattern = r'\b(?:I|we|my|ours|us)\b'
    text = ' '.join(tokenized_text)

    # Exclude the country name "US"
    text = re.sub(r'\bUS\b', '', text)

    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    count = len(matches)

    return count

metric_df['PERSONAL PRONOUNS'] = metric_df['text'].apply(count_personal_pronouns)

# Average Word Length
def average_word_length(text):
    total_chars = sum(len(word) for word in text)  # Sum of the total number of characters in each word
    total_words = len(text)
    return round(total_chars / total_words, 2)

seo_analysis['AVG WORD LENGTH'] = seo_analysis['text'].apply(average_word_length)

# Merge all the files and import
# Getting the original file to get the links
links = pd.read_excel('Input.xlsx')

# Merge the DataFrames on ID with inner join
merged_df = pd.merge(df, seo_analysis, on='URL_ID', how='inner')
merged_df = pd.merge(merged_df, metric_df, on='URL_ID', how='inner')
merged_df = pd.merge(merged_df, links, on='URL_ID', how='inner')

# Selecting and ordering the column names
selected_columns = ['URL_ID', 'URL', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 'SUBJECTIVITY SCORE', 'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX', 'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT', 'WORD COUNT', 'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH']

final_df = merged_df.loc[:, selected_columns]

# Save the final file to csv
final_df.to_csv('output.csv', index=False)