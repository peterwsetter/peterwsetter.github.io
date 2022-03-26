# Utility program
#   - Convert md to html
#   - Add html elements
# Created: 2022-03-19

import os
import sys

from bs4 import BeautifulSoup # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
import markdown # https://python-markdown.github.io/
import yaml

def add_stylesheet(self: BeautifulSoup, style_path: str):
    style = self.new_tag('link')
    style['rel'] = 'stylesheet'
    style['href'] = style_path
    self.head.append(style)

def add_custom_meta_tag(self: BeautifulSoup, tag_attr: str, tag_site: str, tag_type: str, tag_content: str):
    custom_tag = self.new_tag('meta')
    custom_tag.attrs[tag_attr] = tag_site + ':' + tag_type
    custom_tag.attrs['content'] = tag_content
    self.head.append(custom_tag)

BeautifulSoup.add_stylesheet = add_stylesheet
BeautifulSoup.add_custom_meta_tag = add_custom_meta_tag

# Get paths from the command line
input_path: str = sys.argv[1]
output_path: str = sys.argv[2]

if output_path == '--useinput':
    output_path = input_path.replace('.md', '.html')

if sys.argv[3]:
    with open(sys.argv[3], 'r') as template_file:
        templates: dict = yaml.safe_load(template_file)

# Read in markdown and convert to html
with open(input_path, 'r') as input_file:
    text: str = input_file.read()

md: markdown.core.Markdown = markdown.Markdown(extensions = ['meta'])
html: str = md.convert(text)

# Wrap
webpage: str = '<!DOCTYPE html><html><head></head><body>' + html + '</body></html>'
soup: BeautifulSoup = BeautifulSoup(webpage, 'html.parser')

# Style
if 'styles' in templates:
    style_path = (os.path.relpath(templates['styles'], input_path)).replace('../', '', 1)
    soup.add_stylesheet(style_path)

if 'styles' in md.Meta:
    for s in md.Meta['styles']:
        style = soup.new_tag('link')
        style['rel'] = 'stylesheet'
        style['href'] = s
        soup.head.append(style)

# Base
title = soup.new_tag('title')
title.string = md.Meta['title'][0]
soup.head.append(title)

# OG (Facebook)
soup.add_custom_meta_tag('property', 'og', 'title', md.Meta['title'][0])
soup.add_custom_meta_tag('property', 'og', 'description', md.Meta['description'][0])

# Twitter
if 'card' in md.Meta:
    soup.add_custom_meta_tag('name', 'twitter', 'card', md.Meta['card'][0])

if 'site' in md.Meta:
    soup.add_custom_meta_tag('name', 'twitter', 'site', md.Meta['site'][0])

soup.add_custom_meta_tag('name', 'twitter', 'title', md.Meta['title'][0])
soup.add_custom_meta_tag('name', 'twitter', 'description', md.Meta['description'][0])


# Write out
with open(output_path, 'wb') as output_file:
    output_file.write(soup.prettify('utf-8'))