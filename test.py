from domcheck.strategies import *

print check_html_file('localhost', 'valid', 'test')

print search_meta_tag('<meta name="foo" content="bar"></head>', 'foo', 'bar') == True
print search_meta_tag('<meta name="foo" content="bar"/></head>', 'foo', 'bar') == True
print search_meta_tag('<meta name="foo"  content="bar"   /></head>', 'foo', 'bar') == True
print search_meta_tag('<meta name=\'foo\' content=\'bar\'></head>', 'foo', 'bar') == True
print search_meta_tag('<meta content="bar" name="foo"></head>', 'foo', 'bar') == True
print search_meta_tag('<meta content=\'bar\' name=\'foo\'></head>', 'foo', 'bar') == True
print search_meta_tag('</head><meta content=\'bar\' name=\'foo\'>', 'foo', 'bar') == False
print search_meta_tag('</head><meta content=\'bar\' name=\'lol\'>', 'foo', 'bar') == False

print search_meta_tag('<meta name="foo\' content="bar"></head>', 'foo', 'bar') == False
print search_meta_tag('<meta name="foo" content=\'bar"></head>', 'foo', 'bar') == False
print search_meta_tag('<meta content="bar\' content="foo"></head>', 'foo', 'bar') == False
print search_meta_tag('<meta content="bar" content=\'foo"></head>', 'foo', 'bar') == False
