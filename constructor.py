import re
import pandas as pd
from collections import Counter
from pattern.text.en import singularize


class TextProcessor:

    def __init__(self, file_path):

        self.file_path = file_path

        # Imports the whole text to text_raw        
        with open(self.file_path, 'r') as file:
            self.text_raw = file.read()
        
        # splits the articles by the </doc> sinalizer 
        self.article_split('</doc>')

        # separates all words from the articles, excluding symbols and unwanted characters
        self.words_selector()

        # counts the frequency of every word in every article
        self.words_counters()


    def article_split(self, split_char):
        
        # splits the text in each article and stores each article in a position of a list
        self.texts_arts = self.text_raw.split(split_char)

        # remove last empty element from the list
        self.texts_arts.remove('')


    def words_selector(self):
        
        self.words_arts = []

        for art, text in enumerate(self.texts_arts):
            
            # remove all characters between <> from the raw texts
            self.texts_arts[art] = re.sub(r'\<(.*?)\>', '', text)
            
            # appends lists of all words in each article
            self.words_arts.append(re.compile(r'[a-zA-Z]\w*') \
                                .findall(self.texts_arts[art]))

            # remove all caps and transform all words in its singular version
            # so that i.e author, Author and authors are all counted together as one word
            self.words_arts[art] = [singularize(word.lower())
                                             for word in self.words_arts[art]]

    
    def words_counters(self):

        # creates a dict that has keys as article_n and values as a dict of words and the amount of times it is found in the article
        self.counters = {'article_'+str(num): dict(Counter(words)) 
                            for num, words in enumerate(self.words_arts, start = 1)}
    

    def df_creator(self):

        # creates a dataframe with the articles as columns, the words as indexes and the values as the amount of times the word appears in each article
        self.table_words = pd.DataFrame.from_dict(self.counters).fillna(0) \
                            .astype(
                                    {'article_1': int, 
                                     'article_2': int, 
                                     'article_3': int}
                                    ) \
                            .sort_values('article_1', ascending = False)

        return self.table_words
