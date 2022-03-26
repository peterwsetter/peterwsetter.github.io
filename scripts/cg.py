# Utility program
#   - Convert md to html
#   - Add html elements
# Created: 2022-03-19

import sys

from bs4 import BeautifulSoup # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
import markdown # https://python-markdown.github.io/

# Get paths from the command line
input_path: str = sys.argv[1]
output_path: str = sys.argv[2]


def add_custom_meta_tag(self: BeautifulSoup, tag_attr: str, tag_site: str, tag_type: str, tag_content: str):
    custom_tag = self.new_tag('meta')
    custom_tag.attrs[tag_attr] = tag_site + ':' + tag_type
    custom_tag.attrs['content'] = tag_content
    self.head.append(custom_tag)

BeautifulSoup.add_custom_meta_tag = add_custom_meta_tag

# Read in markdown and convert to html
with open(input_path, 'r') as input_file:
    text: str = input_file.read()

md: markdown.core.Markdown = markdown.Markdown(extensions = ['meta'])
html: str = md.convert(text)

# Wrap
webpage: str = '<!DOCTYPE html><html><head></head><body>' + html + '</body></html>'
soup: BeautifulSoup = BeautifulSoup(webpage, 'html.parser')

# Style
if md.Meta['styles']:
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
soup.add_custom_meta_tag('name', 'twitter', 'card', md.Meta['card'][0])
soup.add_custom_meta_tag('name', 'twitter', 'site', md.Meta['site'][0])
soup.add_custom_meta_tag('name', 'twitter', 'title', md.Meta['title'][0])
soup.add_custom_meta_tag('name', 'twitter', 'description', md.Meta['description'][0])


# Write out
with open(output_path, 'wb') as output_file:
    output_file.write(soup.prettify('utf-8'))