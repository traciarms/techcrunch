import csv
import unittest
from articles import TechCrunchScraper


class TestTechCrunchScraper(unittest.TestCase):
    """
    Our basic test class.  These tests mainly test the existence of
    the data or files, since the data we are scraping is dynamic the
    tests cannot test for data accuracy.
    """

    def test_init(self):
        """
        Testing init method for TechCrunchScraper.  Testing that the
        filename for the csv file and the header were created properly.
        """
        header = ['company name', 'company website']
        test_csv = 'test.csv'
        tcs = TechCrunchScraper(test_csv, header)
        self.assertEqual(tcs.out_filename, test_csv)
        self.assertEqual(tcs.csv_header, header)

    def test_get_soup(self):
        """
        Testing get soup method.  Testing that the soup returned is not
        None.
        :return:
        """
        url = 'http://techcrunch.com/'
        header = ['company name', 'company website']
        test_csv = 'test.csv'
        tcs = TechCrunchScraper(test_csv, header)

        soup = tcs.get_soup(url)
        self.assertIsNotNone(soup)

    def test_get_article_links(self):
        """
        Testing the get article links method.  Testing that the number
        of links returned is greater than 0.
        :return:
        """
        url = 'http://techcrunch.com/'
        header = ['company name', 'company website']
        test_csv = 'test.csv'
        tcs = TechCrunchScraper(test_csv, header)
        soup = tcs.get_soup(url)
        links = tcs.get_article_links(soup)

        self.assertGreater(len(links), 0)

    def test_scrape_article(self):
        """
        Testing the scrape article method.  Testing specifically that
        the header data is valid in the data returned.
        :return:
        """
        url = 'http://techcrunch.com/'
        header = ['company name', 'company website']
        test_csv = 'test.csv'
        tcs = TechCrunchScraper(test_csv, header)
        soup = tcs.get_soup(url)
        links = tcs.get_article_links(soup)
        link_soup = tcs.get_soup(links[0])
        data = tcs.scrape_article(link_soup, links[0])

        self.assertIn(header[0], data)
        self.assertIn(header[1], data)

    def test_write_to_csv(self):
        """
        Testing the write to csv method.  This method will test if the
        csv file exists.
        :return:
        """
        url = 'http://techcrunch.com/'
        header = ['company name', 'company website']
        test_csv = 'test.csv'
        tcs = TechCrunchScraper(test_csv, header)
        soup = tcs.get_soup(url)
        links = tcs.get_article_links(soup)
        link_soup = tcs.get_soup(links[0])
        data = tcs.scrape_article(link_soup, links[0])
        tcs.write_to_csv([data])

        with open(test_csv, 'r') as fp:
            file_out = csv.reader(fp)

        self.assertIsNotNone(file_out)

if __name__ == '__main__':
    unittest.main()
