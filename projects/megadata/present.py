import sys, string, re

scan_re = re.compile(
    r"(?:(?P<emph>'{2,3})"
    + r"|(?P<url>\[http[^\]]*\])"
    + r"|(?P<li>^\s+\*.*$)"
    + r"|(?P<pre>(\{\{\{|\}\}\}))"
    + r"|(?P<img>(\[[^\]]*\]))"
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
        self.is_em = 0
        self.is_b = 0

    def _emph_repl(self, word):
        if len(word) == 3:
            self.is_b = not self.is_b
            return ['</b>', '<b>'][self.is_b]
        else:
            self.is_em = not self.is_em
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

    def _img_repl(self, match):
        value = match[1:-1]
        return '  <img src="%s"/>' % value

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
        res = []
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
        

def header(i, name, title):
    res = ["""<html>
<head>
   <meta content="text/html; charset=utf-8" http-equiv="content-type" />
   <link href="present.css" type="text/css" rel="stylesheet" />
   <title>%s | %s</title>
</head>
<body>
  <div class='content'>
  <div class='nav'>
  <a accesskey="h" class="up" href="1.html">home</a>
  
  """ % (name, title)]
    if i > 1:
        res.append("""<a accesskey="j" class="prev" href="%d.html">&laquo;</a>""" % (i - 1,))
    if title != "The End":
        res.append("""<a accesskey="k" class="next" href="%d.html">&raquo;</a>""" % (i+1,))

    res.append("<h1>%s</h1>" % title)
    res.append("""</div><div class="page">""")
    return "\n".join(res)

def footer():
    return """</div></div></body></html>"""

filename = sys.argv[1]
blocks = file(filename, "r").read().split("")
blocks.append("\nThe End\n\n")
presentation_name, blocks[0]= blocks[0].split("\n", 1)
i = 1;
for b in blocks:
    page = ""
    scrap, title, b = b.split("\n", 2)
    print "Title = " + title
    for part in b.split("----"):
        page += (" " + part)
        f = file(str(i) + ".html", "w")
        f.write(header(i, presentation_name, title))
        f.write(Formatter(page, title).get_html())
        f.write(footer())
        f.close()
        i += 1
