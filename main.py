import os
import requests
from bs4 import BeautifulSoup
import re
import webbrowser
from datetime import date

class recent_scraper():
    """add target URL"""
    urls = ["https://arxiv.org/list/gr-qc/new",
            "https://arxiv.org/list/hep-th/new",
            "https://arxiv.org/list/quant-ph/new",
            ]

    """input keywords (search method is "or" search)"""
    keywords = ["entanglement",
                "Holography",
                "Ads/CFT",
                ]

    """dir of saving html"""
    filename = '{}'.format(date.today()) + '.html'
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    save_dir = BASE_DIR
    full_file_name = os.path.join(save_dir, filename)

    template_html = 'temp.html'

    def scraping(self):
        """Main"""
        abstlist = {}
        reviselist = {}
        for url in self.urls:
            response = requests.get(url)
            print(response.status_code)

            bs = BeautifulSoup(response.content, "lxml")

            lists = bs.find_all("dd")
            for keyword in self.keywords:
                for index, source in enumerate(lists):
                    abst = source.find(string=re.compile(keyword, re.IGNORECASE))
                    if abst != None:
                        title = source.find(class_="list-title")
                        title.find("span", class_="descriptor").extract()
                        titletext = title.text
                        authors = source.find(class_="list-authors")
                        authors.find("span").extract()
                        authorstext = authors.text
                        abstract = source.find("p", class_="mathjax")
                        if abstract:
                            abstlist[titletext] = [authorstext, abstract.text]
                        else:
                            reviselist[titletext] = [authorstext]
                        lists.pop(index)
        return (abstlist, reviselist)

    def record(self):
        """html output"""
        temp = open(self.template_html)
        template = temp.read()
        temp.close()
        o = open(self.full_file_name,'w')
        o.write(template)

        (abstlist, reviselist) = self.scraping()

        """new paper"""
        for key in abstlist:
            o.write("<li class={}><h1>{}<br>".format("card",key))
            o.write("<span class={}>{}</span></h1>".format("subtitle", abstlist[key][0]))
            o.write("<p class={}>{}</p></li>".format("body", abstlist[key][1]))
        o.write("</ul>")
        o.write("</div>")

        """revise paper"""
        o.write("<div>")
        o.write("<ul>")
        for key in reviselist:
            o.write("<li class={}><h1>{}<br>".format("card",key))
            o.write("<span class={}>{}</span></h1></li>".format("subtitle", reviselist[key][0]))
        o.write("</ul>")
        o.write("</div>")
        o.write("</body>")
        o.write("</html>")
        o.close()

        webbrowser.open_new_tab(self.full_file_name)
