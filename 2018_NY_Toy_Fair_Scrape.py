import requests
import re
import pandas as pd

def main():
    """
    Program scrapes every exhibitor from the 2018 NY Toy Fair using requests and regex on the HTML class name.
    Generates a CSV file with the exhibitors' name and clickable links to their Google and Amazon queries.
    Designed for retailers to discover toy distributors.
    """
    url = 'https://s23.a2zinc.net/clients/tia/toyfair2018/public/EventMap.aspx?shMode=E&ID=2931'

    page = requests.get(url).text

    data = []
    data.append(['Name', 'Google', 'Amazon'])

    identifier = "exhibitorName"
    for line in page.splitlines():
        if identifier in line:
            try:
                regex = 'href="(.+?)">(.+?)<'
                name = re.search(regex, line).group(2)
                if '&amp;' in name:
                    name = name.replace('&amp;', '&')
                google = '=HYPERLINK("https://www.google.com/search?q={}")'.format(name.replace(' ','+'))
                amazon = '=HYPERLINK("https://www.amazon.com/s/field-keywords={}")'.format(name.replace(' ','+'))
                data.append([name, google, amazon])
            except:
                pass

    df = pd.DataFrame(data)

    out_name = "2018_ToyFair.csv"
    df.to_csv(out_name)

if __name__ == '__main__':
    main()
