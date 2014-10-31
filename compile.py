'''
Compiles the LabROSA webpage.
'''

import lazyweb
import os
import sys
import urllib2
import ujson as json


def url_exists(url):
    '''
    Check if a file exists on the web.  From
    http://stackoverflow.com/questions/2486145/python-check-if-url-to-jpg-exists

    Input:
        url - url to the web resource
    Output:
        result - True or False, depending on if the file exists
    '''
    try:
        urllib2.urlopen(urllib2.Request(url))
        return True
    except:
        return False


def error(message):
    '''
    Print an error message and exit.

    Input:
        message - error message to print
    '''
    print "ERROR: {}".format(message)
    sys.exit(-1)


# Make sure the appropriate site directories exist
for directory in ['people', 'projects', 'publications', 'contact']:
    try:
        os.makedirs(os.path.join('site', directory))
    except:
        pass

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
        error("{}'s URL {} does not exist (should be an absolute url, e.g."
              " http://google.com).".format(person['name'], person['url']))
    # Check that the photo URL exists
    if not url_exists(person['photo']):
        error("{}'s photo {} does not exist (should be an absolute url, e.g."
              " http://google.com/me.jpg).".format(
                  person['name'], person['photo']))
    # Check that the status is valid
    if person['status'] not in statuses:
        error("{}'s status {} is not valid, should be one of {}".format(
            person['name'], person['status'], ", ".join(statuses)))
    # Check that their research description is not too long
    if len(person['research']) > 100:
        error("{}'s research description is too long (longer than 100 "
              "characters)".format(person['name']))

# Sort people list by status, according to the order of the statuses list
people['people'].sort(lambda a, b: cmp(statuses.index(a), statuses.index(b)),
                      lambda x: x['status'])

# TODO: Obfuscate all email addresses
# for person in people['people']:
# person['email'] = obfuscate_email(person['email'])

# Write out the .html file
lazyweb.compile('templates/people.tpl', people, 'site/people/index.html')


# Publications, which is just retrieved from DAn's page via some hacks
print "Compiling publications.tpl..."
# URL of DAn's publications page
DPWE_PUBS_URL = 'http://www.ee.columbia.edu/~dpwe/pubs/'
# Make sure it still exists/is reachable
if not url_exists(DPWE_PUBS_URL):
    error("Couldn't access the publications page {}".format(DPWE_PUBS_URL))
# Get the raw HTML from DAn's pub page
raw_pubs_data = urllib2.urlopen(DPWE_PUBS_URL).read().decode('ascii', 'ignore')
# Find the start and end of the actual pubs table
table_start = raw_pubs_data.find(
    '<table border="0" cellspacing="5" cellpadding="5" width="100%">')
# Raise an error if the HTML has changed
if table_start == -1:
    error("Couldn't find the start of the publications table from {}. Its "
          "format may have changed.".format(DPWE_PUBS_URL))
table_end = raw_pubs_data.find(
    '<td valign="TOP" bgcolor="#fff4e6" colspan="3">\n<h4>2000</h4>')
if table_end == -1:
    error("Couldn't find the end of the publications table from {}. Its "
          "format may have changed.".format(DPWE_PUBS_URL))
# Extract just the table HTML
pubs_table = raw_pubs_data[table_start:table_end]
# Change some formatting to make it fit in
pubs_table = pubs_table.replace('<a name', '<a style="color:black" name')
pubs_table = pubs_table.replace('<h3>', '<h3 style="text-align:center">')
# Write out .html file
lazyweb.compile('templates/publications.tpl', {'table': pubs_table},
                'site/publications/index.html')
