# -*- coding: utf-8 -*-

__version__ = "1.1"

from .strategies import check_dns_txt, check_dns_cname, check_meta_tag, check_html_file


def check(domain, prefix, code, strategies='*'):
    """
    Check the ownership of a domain by going thru a serie of strategies.
    If at least one strategy succeed, the domain is considered verified,
    and this methods returns true.

    The prefix is a fixed DNS safe string like "yourservice-domain-verification"
    and the code is a random value associated to this domain. It is advised to
    prefix the code by a fixed value that is unique to your service like
    "yourservice2k3dWdk9dwz".

    By default all available strategies are tested. You can limit the check
    to a limited set of strategies by passing a comma separated list of
    strategy names like "nds_txt,dns_cname". See the "strategies" module
    for a full list of avaialble strategies.
    """
    if strategies == '*' or 'dns_txt' in strategies:
        if check_dns_txt(domain, prefix, code):
            return True
    if strategies == '*' or 'dns_cname' in strategies:
        if check_dns_cname(domain, prefix, code):
            return True
    if strategies == '*' or 'meta_tag' in strategies:
        if check_meta_tag(domain, prefix, code):
            return True
    if strategies == '*' or 'html_file' in strategies:
        if check_html_file(domain, prefix, code):
            return True
    return False
