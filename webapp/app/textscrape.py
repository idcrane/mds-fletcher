import goose3
import feedparser
import apiclient
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize

def get_articles_urls(urllist, verbose=True):
    cleaned_articles = []
    if type(urllist) == str:
        urllist = [urllist]

    g = goose3.Goose()
    for url in urllist:
        article = g.extract(url=url)
        text = text_clean(article.cleaned_text)
        cleaned_articles.append(text)
    cleaned_articles = [post for post in cleaned_articles if post]

    if verbose:
        print("Number of urls to attempt: %i" % len(urllist))
        print("Number of posts successfully scraped: %i" % len(cleaned_articles))
    return cleaned_articles

def get_articles_rss(url, verbose=True):
    feeds = feedparser.parse(url)
    cleaned_articles = [text_clean(post['summary']) for post in feeds['entries']]
    if verbose:
        print("Number of posts recovered: %i" % len(cleaned_articles))
    cleaned_articles = [post for post in cleaned_articles if post]
    return cleaned_articles

def get_articles_blogger(blogurl, developerKey, onlyposts=False):
    """ Use blogger api to get all blog posts from blogurl
        (Obviously, only for blogs on Blogger)

        If onlyposts=False (default), returns list of dictionaries,
        one per blog post. Dictionaries have post metadata as well as
        raw html.

        If onlyposts=True, returns list of posts (just the post text)
    """
    blog_post_count = 0
    blog_posts = []
    blogger = apiclient.googleapiclient.discovery.build('blogger', 'v3', developerKey=developerKey)

    # Get blogID
    bloginfo = blogger.blogs().getByUrl(url=blogurl, view='READER').execute()

    # Get posts from that blog, looping over paginations in while loop
    postrequest = blogger.posts().list(blogId=bloginfo['id'], maxResults=500)
    while ( postrequest != None ):
        results = postrequest.execute()
        for post in results['items']:
            # Build dictionary of data
            d = {'blog_url': blogurl,
                 'blog_id': bloginfo['id'],
                 'blog_platform': 'blogger',
                 'post_url': post['url'],
                 'post_updated': post['updated'],
                 'post_id': post['id'],
                 'post_content': text_clean(post['content'], html=True),
                 'post_raw_data': post,
                }
            blog_posts.append(d)
            blog_post_count += 1
        postrequest = blogger.posts().list_next(postrequest, results)

    if onlyposts:
        return [post['post_content'] for post in blog_posts]
    else:
        return blog_posts
###############################################################################
# Helper functions

def text_clean(text, html=False):
    """ Get clean text

        If html=True, will strip html tags from text.
        Default is html=False
    """
    if html:
        soup = BeautifulSoup(text)
        text = soup.text

    # More cleaning
    text = text.replace('\n', ' ')

    # Deal with unicode
    text = text.replace(u'\xa0', ' ').replace(u'\u2019', """'""")
    return text

def sentence_count_filter(rawpostlist, num_sentences=5):
    """ From list of strings, returns only those strings
        that have more then num_sentences=5 sentences.
    """
    # Excepting stupid unicode errors for now, TODO
    postlist = []

    # unicode() doesn't exist in Python 3
    # rawpostlist = [unicode(post) for post in rawpostlist]
    rawpostlist = postlist


    for post in rawpostlist:
        sentence_length = 9999999
        try:
            sentence_length = len(sent_tokenize(post.encode('ascii', errors='ignore')))
        except UnicodeDecodeError:
            print('Unicode Error')
        if sentence_length > num_sentences:
            postlist.append(post)
    print("Number of posts meeting criteria: %i" % len(postlist))
    return postlist

def url_clean(url):
     return url.replace('http:', '').replace('/', '')

def get_api_key(path):
    with open(path, 'r') as infile:
        google_api_key = infile.read()
    return google_api_key