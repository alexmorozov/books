#--coding: utf8--

import re


def canonicalize(url):
    """
    Remove querystrings from profile URLs
    """
    if 'linkedin.com/in/' in url:
        return re.sub(r'^([^\?]+)\?.+$', r'\1', url)
    return url
