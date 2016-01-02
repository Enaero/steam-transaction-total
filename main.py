import locale
from html.parser import HTMLParser
from argparse import ArgumentParser


class SteamHistoryParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.total = 0
        self.credit = 0
        self.add_data = False
        self.credit_found = False

    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            parser = self.__class__()
            for attrib in attrs:
                if attrib[0] == 'data-tooltip-content':
                    parser.feed(attrib[1])
        if tag == 'td' and ('class', "wht_total ") in attrs:
            self.add_data = True
        if self.credit_found and tag == 'div':
            self.add_data = True
    
    def handle_endtag(self, tag):
        if tag == 'td':
            self.add_data = False
        if self.credit_found and tag == 'div':
            self.add_data = False
            self.credit_found = False
    
    def handle_data(self, data):
        if self.add_data:
            data = ''.join(c for c in data if c.isdigit() or c == '.')
            
            if self.credit_found:
                self.credit += float(data)
            if data:
                self.total += float(data)
            else:
                self.credit_found = True


if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, '')

    argp = ArgumentParser(description='Sum up your Steam transactions.')
    argp.add_argument('path', metavar='path', type=str, nargs=1,
                      help='The path to the HTML file of the generated DOM')
    args = argp.parse_args()
    name = args.path[0]
    
    parser = SteamHistoryParser()
    with open(name, 'rt', encoding='utf-8') as fp:
        text = fp.read()
        parser.feed(text)

    spent = locale.currency(parser.total)
    gained = locale.currency(parser.credit)
    print('You have spent a total of', spent, 'and gained',
          gained, 'Steam dollars.')
