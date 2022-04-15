#!/usr/bin/python3

'''
Author: Daniel Okuniewicz Jr.
Date: 15 April 2022
Description: Maintain sidenav text throughout entire website,
             easily update changes to sidenav.
'''

import os

current_dir = os.getcwd()
file_list = []
# loop through website directory to get all html files
for root, dirs, files in os.walk(current_dir):
    # select file name
    for file in files:
        # check the extension of files
        if file.endswith('.html'):
            # print whole path of files
            file_list += [os.path.join(root, file)]

# loop through html files and replace old sidenav text
for item in file_list:
    # file containing sidenav html
    with open('sidenav.txt', 'r') as f:
        contents = f.read()
    # file containing old sidenav html to replace
    with open(item, 'r') as g:
            to_replace = g.read()

    start_bound = '<!-- START SIDENAV -->'
    end_bound = '<!-- END SIDENAV -->'

    # replace old sidenav html with new sidenav html
    replace_text =to_replace[to_replace.find(start_bound)+len(start_bound):to_replace.rfind(end_bound)]
    new_text = to_replace.replace(replace_text, '\n' + contents)
    overwritefile = open(item, 'w')
    overwritefile.write(new_text)
    overwritefile.close()
