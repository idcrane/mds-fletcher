from numpy import median
from flask import render_template, flash, redirect
from app import app
from .forms import DataUploadForm
from textscrape import *
from blogclassify import *
from os import environ

classify = BlogClassify()

###############################################################################
### User Specific Files
classify.load_vectorizer('vectorizer.pkl')
classify.load_model('model.pkl')
classify.set_num_sentences(10)
home_dir = environ['HOME']
num_posts_usable_warning_level = 50  # Warning will be produced if num_posts_usable
                                     # less than this number
GOOGLE_API_KEY = get_api_key(home_dir + '/metis/secure/google_api_key.password')
###############################################################################

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    ## Sanity Checks
    if classify.vectorizer == None:
        flash("FATAL ERROR: No vectorizer loaded! Contact website admin!")
    if classify.model == None:
        flash("FATAL ERROR: No model loaded! Contact website admin!")

    form = DataUploadForm()
    if form.validate_on_submit():
        data = []


        ## Are we scraping an RSS feed, or using Blogger API?
        if form.rss_bool.data == True:
            try:
                data = get_articles_rss(form.url.data)
            except:
                flash("CLASSIFICATION ABORTED: Issue getting RSS data. Please check this is a valid RSS URL.")
                return redirect('/index')
        else:
            try:
                data = get_articles_blogger(form.url.data, GOOGLE_API_KEY, onlyposts=True)
            except:
                #TODO: Except only google api HttpErrors (they're not urllib2 errors)
                flash("CLASSIFICATION ABORTED: Issue getting Google Blogger data. Please check this is a valid URL.")
                return redirect('/index')


        ## Get information on what we've scraped
        num_posts = len(data)
        if num_posts == 0:
            flash("CLASSIFICATION ABORTED: No posts can be scraped from this URL")
            redirect('/index')
        try:
            data = [unicode(post) for post in data]
            sentence_lengths = [len(sent_tokenize(post.encode('ascii', errors='ignore'))) for post in data]
            median_sent_len = median(sentence_lengths)
        except:
            flash("CLASSIFICATION ABORTED: Unable to decode posts to Unicode. Total posts scraped: %i" % (num_posts))
            return redirect('/index')


        basic_data = {'url': form.url.data,
                        'rss_bool': str(form.rss_bool.data),
                        'num_posts': num_posts,
                        'median_sent_len': median_sent_len,
                         }

        ## Do the modeling, handle various cases where modeling fails gracefully.
        class_status = False
        try:
            classification, classification_details, num_posts_usable = classify.political_blog_model(data)
        except:
            flash("CLASSIFICATION ABORTED: Classifier Exception")
            return render_template('datauploadform.html',
                                    form=form,
                                    basic_data=basic_data)
        else:
            if num_posts_usable == 0:
                flash("CLASSIFICATION ABORTED: No posts gathered met criteria to be classified!")
                return render_template('datauploadform.html',
                                    form=form,
                                    basic_data=basic_data)
            else:
                class_status = True

        ## Return stuff and render page
        if class_status:
            if num_posts_usable < num_posts_usable_warning_level:
                flash("WARNING: There are fewer than %i usable posts. Classifier's accuracy is diminished." % (num_posts_usable_warning_level))
            c_data = {'num_posts_usable': num_posts_usable,
                        'classification': str(classification),
                        'details': str(classification_details)
                        }
            return render_template('datauploadform.html',
                                    form=form,
                                    basic_data=basic_data,
                                    c_data=c_data)

        # turn redirect('/index')

    return render_template('datauploadform.html',
                            form=form)

