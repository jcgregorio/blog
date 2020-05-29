#! /usr/bin/env python

import sys, string, re

scan_re = re.compile(
    r"(?:(?P<emph>'{2,3})"
    + r"|(?P<url>\[http[^\]]*\])"
    + r"|(?P<li>^\s+\*.*$)"
    + r"|(?P<pre>(\{\{\{|\}\}\}))"
    + r"|(?P<header>^={1,5}\s.*$)"
    + r")")
blank_re = re.compile("^\s*$")
bullet_re = re.compile("^\s+\*")
eol_re = re.compile(r'\r?\n')
 
class Formatter:
    """Turn Wiki markup into HTML.  """
    def __init__(self, raw, word):
        self.raw = raw
        self.word = word
        self.in_pre = 0

    def _emph_repl(self, word):
        if len(word) == 3:
            return ['</b>', '<b>'][self.is_b]
        else:
            return ['</em>', '<em>'][self.is_em]

    def _header_repl(self, word):
        word, value = word.split(' ', 1)
        n = len(word)
        return "\n<h%d>%s</h%d>\n" % (n, value, n) 

    def _url_repl(self, word):
        word, value = word[1:-1].split(' ', 1)
        if not value:
            value = word
        return '<a href="%s">%s</a>' % (word, value)

    def _li_repl(self, match):
        value = match.split('*', 1)[1]
        return '  <li>%s</li>' % value


    def _pre_repl(self, word):
        if word == '{{{' and not self.in_pre:
            self.in_pre = 1
            return '<pre>'
        elif self.in_pre:
            self.in_pre = 0
            return '</pre>'
        else:
            return ''

    def replace(self, match):
        for type, hit in match.groupdict().items():
            if hit:
                return apply(getattr(self, '_' + type + '_repl'), (hit,))
        else:
            raise "Can't handle match " + `match`
        

    def get_html(self):
        res = ["<h1>%s</h1>" % self.word]
        raw = string.expandtabs(self.raw)
        for line in eol_re.split(raw):
            if not self.in_pre:
                if blank_re.match(line):
                    res.append('<p>')
                    continue
            res.append(re.sub(scan_re, self.replace, line))
            res.append("\n")
        if self.in_pre: 
            res.append('</pre>')
        return "".join(res)
        
