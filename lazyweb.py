#!/usr/bin/env python
"""A lightweight script to compile static websites with jinja2 and structured data"""

import sys
import os
import argparse
import ujson as json
import cPickle as pickle
import jinja2


def load_template(input_path):
    '''Load the template data from the specified path.

    :parameters:
      - input_path : str
          Path to the template on disk

    :returns:
      - template : jinja2.Template
          The template object
    '''

    input_path = os.path.abspath(input_path)
    
    env = jinja2.environment.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(input_path)))

    return env.get_template(os.path.basename(input_path))

def load_data(data_file):
    '''Load structured data from the specified path'''

    try:
        with open(data_file, 'r') as f:
            return pickle.load(f)
    except:
        pass

    with open(data_file, 'r') as f:
        return json.loads(f.read())

    raise ValueError('Could not interpret data file: %s' % data_file)

def compile(input_template=None, data=None, output_path=None):
    '''Compile the template and save the output'''

    # First, get the template
    template    = load_template(input_template)

    # Render the output
    output = template.render(**data)

    if output_path is None:
        output_path = os.path.extsep.join([os.path.splitext(input_template)[0], 'html'])

    with open(output_path, 'w') as f:
        f.write(output)

def get_params():
    parser = argparse.ArgumentParser(description='Static compilation of jinja templates')

    parser.add_argument(    'input_template',
                            action      =   'store',
                            help        =   'path to the input template file')

    parser.add_argument(    dest        =   'data_files',
                            type        =   str,
                            nargs       =   '*',
                            help        =   'paths to data files (json or pickle)')

    parser.add_argument(    '-o',
                            '--output',
                            dest        =   'output_path',
                            required    =   False,
                            type        =   str,
                            help        =   'path to save the rendered template')

    return vars(parser.parse_args(sys.argv[1:]))

def main():
    args = get_params()
    compile(**args)

if __name__ == '__main__':
    main()

