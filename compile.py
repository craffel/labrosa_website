'''
Compiles the LabROSA webpage.
'''

import lazyweb
import os
import urllib2
import ujson as json
import re
import urlparse
import PIL.Image
import io

BASE_URL = 'http://labrosa.ee.columbia.edu/'


def url_exists(url):
    '''
    Check if a file exists on the web.  From
    http://stackoverflow.com/questions/2486145/python-check-if-url-to-jpg-exists

    :parameters:
        - url : str
            URL to the web resource
    '''
    print '  Checking URL {}'.format(url)
    # Check if the URL is relative to document root
    if url[:len('http://')] != 'http://':
        url = urlparse.urljoin(BASE_URL, url)
    try:
        urllib2.urlopen(urllib2.Request(url))
    except:
        raise ValueError('The URL {} is not reachable.'.format(url))


def validate_image(url, max_size_kb=100, wh_ratio_min=.5, wh_ratio_max=1.8):
    '''
    Makes sure the provided URL points to a valid image which is within the
    provided size constraints.  Portions from
    http://effbot.org/zone/pil-image-size.htm

    :parameters:
        - url : str
            URL of some image, absolute or relative to document root
        - max_size_kb : float
            Maximum size of the image in kilobytes
        - wh_ratio_min : float
            Minimum value of (image width/image height)
        - wh_ratio_max : float
            Maximum value of (image width/image height)
    '''
    # Make sure the URL is valid
    url_exists(url)
    # Check if the URL is relative to document root
    if url[:len('http://')] != 'http://':
        url = urlparse.urljoin(BASE_URL, url)
    image_file = urllib2.urlopen(url)
    # Try to get the image size in bytes from the content header
    size = image_file.headers.get("content-length")
    # Some URLS don't return this, in which case we need to load the image
    if size is None:
        size = len(image_file.read())
    # Convert to an integer value
    size = int(size)
    # Check size in kb
    if size/1000 > max_size_kb:
        raise ValueError('The image {} is larger than the maximum size of {} '
                         'kB.'.format(url, max_size_kb))
    # Read in image to get dimensions
    image = PIL.Image.open(io.BytesIO(image_file.read()))
    wh_ratio = image.size[0]/float(image.size[1])
    if wh_ratio < wh_ratio_min or wh_ratio > wh_ratio_max:
        raise ValueError("The image {} has a width of {} and a height of {}, "
                         "which doesn't satisfy the specified {} < "
                         "width/height < {}".format(
                             url, image.size[0], image.size[1], wh_ratio_min,
                             wh_ratio_max))

    image_file.close()


def obfuscate_string(value):
    '''
    Turns a string into a hex representation. From
    https://github.com/morninj/django-email-obfuscator

    :parameters:
        - value : str
            String to obfuscate.
    :returns:
        - obfuscated_value : str
            Obfuscated string.
    '''
    return ''.join(['&#{0:s};'.format(str(ord(char))) for char in value])


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
    url_exists(person['url'])
    # Check that the photo is valid
    validate_image(person['photo'])
    # Check that the status is valid
    if person['status'] not in statuses:
        raise ValueError("{}'s status {} is not valid, should be one of "
                         "{}".format(
                             person['name'], person['status'],
                             ", ".join(statuses)))
    # Check that their research description is not too long
    if len(person['research']) > 120:
        raise ValueError("{}'s research description is too long (longer than "
                         "120 characters)".format(person['name']))

# Sort people list by status, according to the order of the statuses list
people['people'].sort(lambda a, b: cmp(statuses.index(a), statuses.index(b)),
                      lambda x: x['status'])

# TODO: Obfuscate all email addresses
for person in people['people']:
    person['email'] = obfuscate_string(person['email'])

# Write out the .html file
lazyweb.compile('templates/people.tpl', people, 'site/people/index.html')


# Publications, which is just retrieved from DAn's page via some hacks
print "Compiling publications.tpl..."
# URL of DAn's publications page
DPWE_PUBS_URL = 'http://www.ee.columbia.edu/~dpwe/pubs/'
# Make sure it still exists/is reachable
url_exists(DPWE_PUBS_URL)
# Get the raw HTML from DAn's pub page
raw_pubs_data = urllib2.urlopen(DPWE_PUBS_URL).read().decode('ascii', 'ignore')
# Find the start and end of the actual pubs table
table_start = raw_pubs_data.find(
    '<TABLE BORDER="0" CELLSPACING="5" CELLPADDING="5" WIDTH="100%">')
# Raise an error if the HTML has changed
if table_start == -1:
    raise ValueError("Couldn't find the start of the publications table from "
                     " {}. Its format may have changed.".format(DPWE_PUBS_URL))
table_end = raw_pubs_data.find(
    '<TD VALIGN="TOP" BGCOLOR="#fff4e6" COLSPAN="3">\n<H4>2000</H4>')
if table_end == -1:
    raise ValueError("Couldn't find the end of the publications table from {}."
                     "  Its format may have changed.".format(DPWE_PUBS_URL))
# Extract just the table HTML
pubs_table = raw_pubs_data[table_start:table_end]
# Change some formatting to make it fit in
pubs_table = pubs_table.replace('<A NAME', '<A STYLE="color:black" NAME')
pubs_table = pubs_table.replace('<H3>', '<H3 STYLE="text-align:center">')
# Change relative links to absolute
pubs_table = re.sub(r'HREF="(?!http)(.*)"',
                    r'HREF="{}\1"'.format(DPWE_PUBS_URL),
                    pubs_table)
# Write out .html file
lazyweb.compile('templates/publications.tpl', {'table': pubs_table},
                'site/publications/index.html')

# Contact, which is just a static page
print "Compiling contact.tpl..."
lazyweb.compile('templates/contact.tpl', {}, 'site/contact/index.html')

# Index, also a static HTML page
print "Compiling index.tpl..."
lazyweb.compile('templates/index.tpl', {}, 'site/index.html')

# Projects page
print "Compiling projects.tpl..."

# Load in projects .json file
with open('data/projects.json', 'r') as f:
    projects = json.loads(f.read())
# Validate all entries
for project in projects['projects']:
    # Check that their homepage exists
    url_exists(project['url'])
    # Check that the photo URL exists
    validate_image(project['image'])
    # Check that the description is not too long
    if len(project['description']) > 200:
        raise ValueError("Project {}'s description is too long (longer than "
                         "200 characters)".format(project['name']))

# Write out the .html file
lazyweb.compile('templates/projects.tpl', projects, 'site/projects/index.html')
