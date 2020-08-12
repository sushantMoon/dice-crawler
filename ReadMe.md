# Objective 
Scrap Job postings from Dice.com for educational purposes. ;)

# Requirements

1. chromedriver : [Download](https://chromedriver.chromium.org/downloads) the driver corresponding to your chrome version.
2. Python Module : Selenium

# Working

```
python crawl.py --job 'data scientist' --location 44000
```

For help,
```
python crawl.py --h
```

# Flow

1. Visit Dice.com.
2. Input the search query for provided `job` and `location`.
3. Scrap the results (links to the job postings in the search result) from the first page.
4. Iterate over the links, go to each job posting landing page and scrap the job requirement detailed paragraph and save it to the `detailed_html` file.
