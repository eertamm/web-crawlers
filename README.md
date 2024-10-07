# A crawler for EST main realestate web page www.kv.ee

## The initial set-up:
    - Go to the directory you wish to clone the repo
        % git clone https://github.com/eertamm/web-crawlers.git
        % cd web-crawlers
    - Create a python virtual environment because modules like 'requirements' and 'beautifulsoup4' tend to conflict with root settings
        % python 3 -m venv <your venv name here>
    -Launch your virutal environment
        % source crawlers/bin/activate
    - Install dependencies
        % pip3 install -r requirements.txt


## The how-to:
    You must go and create the base query on the website itself.
        - pick 100 answers per page and the sorting option of your liking.
        - paste that query lik into the code (line 6)
        - define how many result pages you want to iterate over (line 77)

Once done, launch the crawler
    % python3 kvcrawl.py
Type in the keyword you search for (e.g. koduloom) and await for the results.

### In case of error 403:
    Google for a different header format and replace the exisiting one. 
    kv.ee tends not to like automated searches that much so from time to time, 
    changing header section is neccessary.