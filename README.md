# A crawler for EST main realestate web page www.kv.ee

## The how-to:
    You must go and create the base query on the website itself.
        - pick 100 answers per page and the sorting option of your liking.
        - paste that query lik into the code (line 6)
        - define how many result pages you want to iterate over (line 77)

Once done, run the code with "python3 kvcrawl.py"
Type in the keyword you search for (e.g. lemmikoom) and await for the results.

### In case of error 403:
    Google for a different header format and replace the exisiting one. 
    kv.ee tends not to like automated searches that much so from time to time, 
    changing header section is neccessary.