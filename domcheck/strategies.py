# -*- coding: utf-8 -*-

import dns.resolver
import re

try:
    # For Python 3.0 and later
    from urllib.request import urlopen, Request
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, Request


def check_dns_txt(domain, prefix, code):
    """
    Validates a domain by checking that {prefix}={code} is present in the TXT DNS record
    of the domain to check.

    Returns true if verification suceeded.
    """
    token = '{}={}'.format(prefix, code)
    try:
        for rr in dns.resolver.query(domain, 'TXT'):
            if token in rr.to_text():
                return True
    except:
        pass
    return False


def check_dns_cname(domain, prefix, code):
    """
    Validates a domain by checking the existance of the CNAME record on the domain as:
    {prefix}-{code}.{domain} pointing to a domain (usually yours) which the host is {prefix}
    (i.e.: {prefix}.yourdomain.com).

    Returns true if verification suceeded.
    """
    fqdn = '{}-{}.{}'.format(prefix, code, domain)
    try:
        for rr in dns.resolver.query(fqdn, 'CNAME'):
            if rr.to_text().startswith(prefix + '.'):
                return True
    except:
        pass
    return False


def search_meta_tag(html_doc, prefix, code):
    """
    Checks whether the html_doc contains a meta matching the prefix & code
    """
    regex = '<meta\s+(?:name=([\'\"]){0}\\1\s+content=([\'\"]){1}\\2|content=([\'\"]){1}\\3\s+name=([\'\"]){0}\\4)\s*/?>'.format(prefix, code)
    meta = re.compile(regex, flags=re.MULTILINE | re.IGNORECASE)
    m = meta.search(html_doc)
    if m:
        head = re.search(r'</head>', html_doc, flags=re.IGNORECASE)
        if head and m.start() < head.start():
            return True
    return False


def check_meta_tag(domain, prefix, code):
    """
    Validates a domain by checking the existance of a <meta name="{prefix}" content="{code}">
    tag in the <head> of the home page of the domain using either HTTP or HTTPs protocols.

    Returns true if verification suceeded.
    """
    url = '://{}'.format(domain)
    for proto in ('http', 'https'):
        req = Request(proto + url, headers={'User-Agent': 'Mozilla/5.0; Domcheck/1.0'})
        res = urlopen(req, timeout=2)
        if res.code == 200:
            # Expect the </head> to be found in the first 100k of the page
            content = res.read(100000)
            res.close()
            return search_meta_tag(content, prefix, code)
        else:
            res.close()
    return False


def check_html_file(domain, prefix, code):
    """
    Validates a domain by checking the existance of a file named {code}.html at the root of the
    website using either HTTP or HTTPS protocols. The file must contain {prefix}={code} in the
    body of the file to ensure the host isn't responding 200 to any requests.

    Returns true if verification suceeded.
    """
    url = '://{}/{}.html'.format(domain, code)
    token = '{}={}'.format(prefix, code)
    for proto in ('http', 'https'):
        try:
            req = Request(proto + url, headers={'User-Agent': 'Mozilla/5.0; Domcheck/1.0'})
            res = urlopen(req, timeout=2)
            if res.code == 200:
                # Read 10k max
                content = str(res.read(10000))
                res.close()
                if token in content:
                    return True
            else:
                res.close()
        except:
            pass
    return False
