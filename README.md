# Approach

<b>	Web Scraping: </b>
1. Web scrape the blogs in 'input.csv' through the URL using BeautifulSoup and request

<b> Text Analysis </b>
1. Use NLTK and syllapy to tokenize and calculate all the variables like positive and negative scores (using a positive and negative dictionary),
complex word count, syllable per word, etc.


# How to run the file:
1.	PRE: Install the dependencies specified below in the requirements
2.	STEP 1: First run the web_scrape.py file that creates an article directory to save all the blogs. It  also creates a 'combined.csv'  to save all the blogs in a single file for NLP
3.	STEP 2: Then run the 'txt_analysis.py' to perform all the analysis and output a CSV file 'output.csv' for the output
4.	Files Needed: The 'txt_analysis.py' needs the 'input.csv', 'MasterDictionary', 'StopWords', and 'articles'.

#	Requirements:
1.	pandas==1.5.3
2.	beautifulsoup4==4.12.2
3.	requests==2.28.2
4.	nltk==3.8.1
5.	syllapy==0.7.2
