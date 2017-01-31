import csv
import re

import bs4
import requests


class TechCrunchScraper:
    """
    This is the main class used to scrape posts from the TechCrunch website.
    It will execute several methods. The process includes:
    1. Get all links for articles
    2. For each post, scrape its content to look for business that is the
    main subject of the post
    3. Write the data gathered from the post to a .csv file
    """

    def __init__(self, filename, header):
        """
        Initialize the Scraper with the out filename and the csv header, or
        format of the csv file.
        :param filename:
        :param header:
        """
        self.out_filename = filename
        self.csv_header = header
        self.request_header = {'User-agent': 'Mozilla/5.0 (Windows NT '
                                             '6.2; WOW64) AppleWebKit/'
                                             '537.36 (KHTML, like '
                                             'Gecko) Chrome/37.0.2062.'
                                             '120 Safari/537.36'}

    def get_soup(self, url):
        """
        Make a GET request to a URL and return the soup.
        :param url:
        :returns: requests' response -> soup.
        """
        response = requests.get(url, headers=self.request_header)
        soup = bs4.BeautifulSoup(response.content, "html.parser")

        return soup

    @staticmethod
    def get_article_links(soup):
        """
        Get the article links for this page.  There are a few different
        article link attributes, so I will first grab all the <li> tags on
        the page and then filter out for the article links that I want.
        :param soup:
        :return: a list of links to the articles on this page.
        """
        links = []
        li_s = soup.find_all('li')

        for li in li_s:

            if li.get('data-permalink'):
                links.append((li.get('data-permalink')))
            else:
                link = li.find_next('a')
                if link:
                    if li.find_next('a').get('data-omni-sm') and \
                       re.search(r'gbl_river_headline',
                                 li.find_next('a').get('data-omni-sm')) and \
                       re.search(r'techcrunch\.com',
                                 link.get('href'), re.IGNORECASE):
                        links.append((li.find_next('a').get('href')))

        return links

    @staticmethod
    def scrape_article(soup, url):
        """
        This method will scrape the contents of the article, specifically
        looking for the Organization name that is the main topic of the article.
        It returns the data for the business and the article.
        :param soup:
        :param url:
        :return: business and article data
        """
        data = {}
        article_title = soup.find('h1',
                                  attrs={
                                      'class': 'alpha tweet-title'}).get_text()
        data['article title'] = article_title
        data['article url'] = url

        crunch_base = soup.find('ul', attrs={'class': 'crunchbase-accordion'})

        # if the crunch base info is present
        if crunch_base:
            cbs = crunch_base.find_all('li')

            # find all the crunch base entries
            for cb in cbs:
                a = cb.find_next('a')
                href = cb.get('data-crunchbase-url')

                if href:

                    # if the entity in the crunchbase is an organization
                    # get the info
                    if re.search(r'organization', href):
                        data['company name'] = a.get_text().strip()
                        key = ''
                        key_node = crunch_base

                        # look for the website info
                        while key != 'Website' and key_node is not None:
                            if key_node:
                                key_node = \
                                    key_node.find_next('strong',
                                                       attrs={'class': 'key'})
                            if key_node:
                                key = key_node.get_text()

                        if key_node:
                            website = \
                                key_node.find_next('span',
                                                   attrs={'class': 'value'}).\
                                    find_next('a').get_text()

                            data['company website'] = website
                        break

        # if we could not determine the company name or website enter
        # n/a in the data
        if 'company name' not in data:
            data['company name'] = 'n/a'
        if 'company website' not in data:
            data['company website'] = 'n/a'

        return data

    def write_to_csv(self, data):
        """
        This method takes the data returned from the article and writes it out
        to a csv file.
        :param data:
        :return: None
        """
        f_data = []

        for row in data:
            row_data = []

            for header in self.csv_header:
                row_data.append(row[header])

            f_data.append(row_data)

        with open(self.out_filename, 'w') as fp:
            a = csv.writer(fp)
            a.writerow(self.csv_header)
            a.writerows(f_data)

    def run(self, url):
        """
        This method will first get a list of article links at the given url.
        It will then get the soup for each link in the list and then call
        the scraper with the given soup and link.

        ** Note ** I decided not to visit subsequent pages to get their links.
        However, if this was needed, after the links are gathered for each page
        (and scraped) I would then check for pagination and then iterate over
        the subsequent pages - gather links on each page and scrape the
        subsequent articles.
        :param url:
        :return: None
        """
        soup = self.get_soup(url)
        links = self.get_article_links(soup)

        data_set = []
        for link in links:
            soup = self.get_soup(link)
            data = self.scrape_article(soup, link)
            data_set.append(data)

        self.write_to_csv(data_set)


if __name__ == '__main__':
    csv_header = ["company name",
                  "company website",
                  "article title",
                  "article url"]
    csv_out = 'articles.csv'

    s = TechCrunchScraper(csv_out, csv_header)
    s.run('https://techcrunch.com/')
