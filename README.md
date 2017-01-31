# techcrunch.com Scraper

A simple command line app to go to techcrunch.com and read articles and
determine which company (if any) is the main subject of the article.

## Description

The program will examine the articles on the front page of techcrunch.com
and determine the company that is the main subject of the article.

## Details

The technique I used for determining the company was to visit the article
link and then read the crunch base area of the page searching for an organization.
If there is not an organziation listed in the crunch base area, n/a is added
(for company name and website) to the .csv for that particular article.  If
there is more than one organization listed in the crunch base area, I take the
first organization as the main subject.

### Deliverables

* A GitHub repo called techcrunch containing:
  * This `README.md` file
  * a file called `articles.py`
  * a file called `test.py`

### Execute

* To execute the script:
  * python3 articles.py
* To run tests:
  * python3 test.py

## csv_branch

You can then navigate to the csv_branch and again run the program with
the same command as above.  The output will be in the new requested format.

This only required a one line change to the csv_header variable in the main
method of the script.


## Notes

I made the design decision to not scrape further pages since it would just
be gathering other lists; such as pagination or other sections of the page.
I felt that this ability was demonstrated with the gathering of the initial
list.

I also considered allowing the user to input their desired header (for output
file format) - which could easily be accomplished with a raw_input() statement,
at the beginning of the main method.  However, I decided  to leave this setup
inside script for ease of running the program.

The way I designed it, if this type of change is required
it would just require changing the csv_header variable to the desired format
for the csv file.
