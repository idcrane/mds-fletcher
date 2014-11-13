### Classifying Political Blogs

Eventually there will be a blog post on this. 

This repo consists of a webapp (in 'webapp', oddly enough), as well as an IPython notebook that has code for training and playing around with different models. 

TODO: have everything be able to find blogclassify.py and textscrape.py.

Note that the core parts of the webapp (and IPython notebook) are in webapp/app/blogclassify.py and webapp/app/textscrape.py. The IPython notebook needs to import these to run. As it stands you will need to move them to same directory as IPython notebook, change the import statement to find them, or modify your PYTHONPATH environment variable to include their directory. 

The vectorizer pickle file webapp/vectorizer.pkl is not included in repo due to size (>100 MB compressed).
This is required for the webapp to run (path to the vectorizer is set in webapp/app/views.py), and may be generated from the IPython notebook. 

