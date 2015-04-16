# -*- coding: utf-8 -*-

import dns.resolver
import urllib2
import re


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
    {prefix}-{code}.{domain}.

    Returns true if verification suceeded.
    """
    fqdn = '{}-{}.{}'.format(prefix, code, domain)
    try:
        return len(dns.resolver.query(fqdn, 'CNAME')) >= 1
    except:
        pass
    return False


def check_meta_tag(domain, prefix, code):
    """
    Validates a domain by checking the existance of a <meta name="{prefix}" content="{code}">
    tag in the <head> of the home page of the domain using either HTTP or HTTPs protocols.

    Returns true if verification suceeded.
    """
    url = '://{}'.format(domain)
    meta = re.compile('<meta\s+name="{}"\s+content="{}"/?>'.format(prefix, code),
                      flags=re.MULTILINE | re.IGNORECASE)
    for proto in ('http', 'https'):
        try:
            res = urllib2.urlopen(proto + url)
            if res.code == 200:
                content = res.read()
                res.close()
                m = meta.search(content)
                if m:
                    # Ensure the meta is in the head part
                    head = re.search(r'</head>', content, flags=re.IGNORECASE)
                    if head and m.start() < head.start():
                        return True
            else:
                res.close()
        except:
            pass
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
            res = urllib2.urlopen(proto + url)
            if res.code == 200:
                content = res.read()
                res.close()
                if token in content:
                    return True
            else:
                res.close()
        except:
            pass
    return False
