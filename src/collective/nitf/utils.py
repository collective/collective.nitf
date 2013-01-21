
# TODO: This recursive function will clean HTML code to be valid as
#       NewsML body. Leaving it here for the future.

from lxml.html import fromstring
from lxml.html import tostring


def cleanup_body_html(elem):
    
    safe_attribs = ['href']
    # valid_tags = ['p', 'ul', 'hedline', 'hl1', 'media']
    for tag in elem:
        cleanup_body_html(tag)
        
        for aname in tag.attrib:
            # Remove unsafe attributes
            if aname not in safe_attribs:
                del tag.attrib[aname]

        if tag.tag == 'h2':
            tag.tag = 'p'
        elif tag.tag == 'span':
            tag.unwrap()
        elif tag.tag == 'ol':
            tag.tag = 'ul'