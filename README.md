# A crawler for EST main realestate web page www.kv.ee

## The initial set-up:
    - Go to the directory you wish to clone the repo

        % git clone https://github.com/eertamm/web-crawlers.git
        % cd web-crawlers

    - Create a python virtual environment because modules like 'requirements' and 'beautifulsoup4' tend to conflict with root settings

        % python3 -m venv <your venv name>

    - Launch your virutal environment

        % source <your venv name>/bin/activate

    - Install dependencies

        % pip3 install -r requirements.txt


## The how-to:
    
        - go and create the base query on the website www.kv.ee itself and copy it to your clipboard.

    Once done, launch the crawler

        % python3 kvcrawl.py
    
        - Paste the query link.
        - Type in the number of pages you wish to crawl through.    
        - Type in the keyword you search for (e.g. lemmikloom / rõdu / mänguväljak etc) and await for the results.
            the search uses regex so it searches for a pattern *keyword*
