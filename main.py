from html.parser import HTMLParser


class SteamHistoryParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.total = 0
        self.credit_total = 0
        self.add_data = False
        self.credit = False

    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            parser = self.__class__()
            for attrib in attrs:
                if attrib[0] == 'data-tooltip-content':
                    parser.feed(attrib[1])
        if tag == 'td' and ('class', "wht_total ") in attrs:
            self.add_data = True
        if self.credit and tag == 'div':
            self.add_data = True
    
    def handle_endtag(self, tag):
        if tag == 'td':
            self.add_data = False
        if self.credit and tag == 'div':
            self.add_data = False
            self.credit = False
    
    def handle_data(self, data):
        if self.add_data:
            data = ''.join(c for c in data if c.isdigit() or c == '.')
            
            if self.credit:
                self.credit_total += float(data)
            if data:
                self.total += float(data)
            else:
                self.credit = True


name = r'steamhist.html'
with open(name, 'rt', encoding='utf-8') as fp:
    text = fp.read()
    parser = SteamHistoryParser()
    parser.feed(text)
    print(parser.total, parser.credit_total)
