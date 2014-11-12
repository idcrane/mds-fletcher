import textscrape as tscrape
from collections import Counter
from operator import itemgetter

import sklearn.metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib

class BlogClassify(object):
    def __init__(self, vectorizer=None, model=None, num_sentences=5):
        self.load_model(model)
        self.load_vectorizer(vectorizer)
        self.set_num_sentences(num_sentences)

    def load_model(self, path):
        if path == None:
            self.model = None
        else:
            self.model = joblib.load(path)

    def load_vectorizer(self, path):
        if path == None:
            self.vectorizer = None
        else:
            self.vectorizer = joblib.load(path)

    def set_num_sentences(self, num_sentences):
        self.num_sentences = num_sentences

    def political_blog_model(self, rawpostlist):
        """ Function to apply model to a list of posts from a single blog.
        """
        postlist = tscrape.sentence_count_filter(rawpostlist, num_sentences=self.num_sentences)
        if len(postlist) == 0:
            return -1, -1, 0

        # Actually make predictions
        vectorized_posts = self.vectorizer.transform(postlist)
        model_predictions = self.model.predict(vectorized_posts)

        # Format results
        counted_predictions = sorted(Counter(model_predictions).items(), key=itemgetter(1), reverse=True)
        single_prediction = counted_predictions[0][0]
        prediction_ratio = float(counted_predictions[1][1]) / float(counted_predictions[0][1])
        if prediction_ratio > 0.8:
            single_prediction = 'Tie'
        return single_prediction, counted_predictions, len(postlist)

    # def build_political_blog_model(self, rawdictlist):

