# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import lazyweb
import os
import sys
import urllib2
import ujson as json

# <codecell>

def url_exists(url):
    '''
    Check if a file exists on the web.  From http://stackoverflow.com/questions/2486145/python-check-if-url-to-jpg-exists
    
    Input:
        url - url to the web resource
    Output:
        result - True or False, depending on if the file exists
    '''
    try:
        f = urllib2.urlopen(urllib2.Request(url))
        return True
    except:
        return False

# <codecell>

def error(message):
    '''
    Print an error message and exit.
    
    Input:
        message - error message to print
    '''
    print "ERROR: {}".format(message)
    sys.exit(-1)

# <codecell>

# Make sure the appropriate site directories exist
os.makedirs('site/people/')
os.makedirs('site/projects/')
os.makedirs('site/publications/')
os.makedirs('site/contact')

# <codecell>

# People page
print "Compiling people.tpl..."

# Permissable entries for the status field
statuses = ['Principal Investigator',
            'PhD Candidate',
            'Graduate Research Assistant',
            'Post-Doctoral Research Assistant',
            'Undergraduate Research Assistant',
            'Visiting Researcher',
            'PhD Graduate', 
            'Staff',
            'Other Researcher',
            'Friend',
            'Past Member/Visitor']

# Load in people .json file
with open('data/people.json', 'r') as f:
    people = json.loads(f.read())
# Validate all entries
for person in people['people']:
    # Check that their homepage exists
    if not url_exists(person['url']):
        error("{}'s URL {} does not exist (should be an absolute url, e.g. http://google.com).".format(person['name'], person['url']))
    # Check that the photo URL exists
    if not url_exists(person['photo']):
        error("{}'s photo {} does not exist (should be an absolute url, e.g. http://google.com/me.jpg).".format(person['name'], person['photo']))
    # Check that the status is valid
    if person['status'] not in statuses:
        error("{}'s status {} is not valid, should be one of {}".format(person['name'], person['status'], ", ".join(statuses)))
    # Check that their research description is not too long
    if len(person['research']) > 100:
        error("{}'s research description is too long (longer than 100 characters)".format(person['name']))

# Sort people list by status, according to the order of the statuses list
people['people'].sort(lambda a, b: cmp(statuses.index(a), statuses.index(b)), lambda x: x['status'])

# Write out the .html file
lazyweb.compile('templates/people.tpl', people, 'site/people/index.html')

# <codecell>

help(os.makedirs)

