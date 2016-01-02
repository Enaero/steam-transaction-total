import locale
from html.parser import HTMLParser
from argparse import ArgumentParser


class SteamHistoryParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.total = 0
        self.add_data = False

    def strip_nonmoney(self, data):
        return ''.join(c for c in data if c.isdigit() or c in ['.', '-'])

    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            parser = self.__class__()
            for attrib in attrs:
                if attrib[0] == 'data-tooltip-content':
                    parser.feed(attrib[1])
        if tag == 'td' and ('class', "wht_total ") in attrs:
            self.add_data = True
    
    def handle_endtag(self, tag):
        self.add_data = False

    def handle_data(self, data):
        if self.add_data:
            data = self.strip_nonmoney(data)
            if data:
                self.total += float(data)


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
    print('You have spent a total of', spent, 'on Steam.')
