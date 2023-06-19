# This program gives you the tag changes made according to the date, place, and tag
## It stores all the response from different places into a single response as well
## 1. Install all the requirements as follow
``` pip install -r requirements.txt ```

## 2. Give your own query parameters like date and geometry of places
## 3. Give your own osmcha token_id in the terminal 
## 4. you can pass arguments like start_date, end_date, places, tags, save_file and token in the terminal as following:  
```python OSM-tag-changes.py --start_date yyyy-mm-dd --end_date yyyy-mm-dd --places bhaktapur,lalitpur,kathmandu --tags highway=primary --token token_id --save_file changes.csv```

## 5. start_date and end_date should be in the format yyyy-mm-dd 
##    places should be comma seperated values where you can use any combination of the places. 
##    tags should in a key,value pair 
##    you should pass your own osmcha token_id in the terminal
##    If you give a name for save_file then it will save the file with that name else it will save    the file as changes{end_date}.csv 
