import pandas as pd
import spacy
from sklearn.feature_extraction.text import CountVectorizer
import re


def user_desc(text):
    """
    takes user description and makes it into lemmas
    """
    # Helper functions
    def clean_text(text):
        """
        takes text cleans it, and lemmatizes it using spacy
        """
        text = str(text)  # ensures text input as string
        # only letters of the alphabet and whitespaces. no numbers or punctuation.
        text = re.sub(r"[^a-zA-Z\s]", " ", text)
        # replaces multi-whitespaces with one whitespace.
        text = re.sub(r"\s+", " ", text)
        # removes whitespaces at the ends, and normalizes the letter case.
        text = text.lower().lstrip().rstrip()
        return text

    def lemmatize(text):
        """
        uses spaCy to tokenize and lemmatize text
        """
        tokens = []
        for token in nlp(text):
            if (not token.is_stop) & (not token.is_punct) & (not token.is_space):
                tokens.append(token.lemma_)

        return [lemma for lemma in tokens if len(lemma) > 2]

    def clean_df(df):
        """
        Takes description and price, and ensures that they are lemmatized and integers
        """
        df['clean_text'] = df['description'].apply(clean_text)
        df['lemmas'] = df['clean_text'].apply(lemmatize)
        return df[['lemmas', 'clean_text']]

    # impact lemmas list
    impact_lemmas = ['downtown',
                     'private',
                     'restaurant',
                     'pool',
                     'park',
                     'clean',
                     'coffee',
                     'wifi',
                     'patio',
                     'backyard',
                     'share',
                     'free',
                     'spacious']

    # Spacy model
    nlp = spacy.load('en_core_web_sm')
    data = {'description': [text]}
    text_df = pd.DataFrame(data=data)

    # NLP description stuff
    mydf = clean_df(text_df)
    vect = CountVectorizer(tokenizer=lemmatize)
    vect.fit(mydf['clean_text'])
    dtm_tf = vect.transform(mydf['clean_text'])
    dtm_tf = pd.DataFrame(dtm_tf.todense(), columns=vect.get_feature_names())
    for lemma in impact_lemmas:
        if lemma in dtm_tf.columns:
            pass
        else:
            dtm_tf[lemma] = 0
    final_df = dtm_tf[impact_lemmas]

    return final_df
