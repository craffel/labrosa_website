Overview
========

This repository contains code for generating LabROSA's new (as of 2014) website.  The basic structure is as follows: Most of the editable data of the website is contained in .json files in the data directory.  The Python script compile.py reads in this data and populates .tpl templates in the templates directory and writes them out into the site directory.  The website can then be served statically from the site directory.

The file compile.py can be run by simply issuing
```
python compile.py
```
It contains code for not only populating the templates and converting them to HTML, but also for validating the content of the .json files (e.g. checking for broken links, obfuscating email addresses, etc.)

Editing content
===============

To change the content of the website, simply edit the appropriate .json file in the data directory. Guidelines for editing the content of each page follows.

People
------

Each entry in the people.json corresponds to a member (past or present) of LabROSA.  Each person has the following fieds:
* name - The person's name, e.g. Joe Davis
* photo - An absolute URL to a photo of the person, e.g. http://google.com/me.jpg The photo should be approximately 100 x 100 pixels. 
* email - The person's email, e.g. steve@apple.com - This will be automatically obfuscating by compile.py so you can just leave it as a plain, raw email address.
* status - The persons's status at LabROSA.  For consistency, it **must** be one of "Principal Investigator", "PhD Candidate", "Graduate Research Assistant", "Post-Doctoral Research Assistant", "Undergraduate Research Assistant", "Visiting Researcher", "PhD Graduate", "Staff", "Other Researcher", "Friend", or "Past Member/Visitor".
* research - A brief statement of the persons research focus, 100 characters or less.
* url - An absolute URL to the person's homepage, e.g. http://google.com


