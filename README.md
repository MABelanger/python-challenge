## usage
```
$ python csv_parser.py
```

## The challenge test*.csv :
There are 2 small files containing some data.  Here is some information about the files:
- the data is stored in a CSV (Comma Separated Values) file format.
- the 'dialect' is the one used by Microsoft Excel
- the first line is a header describing the data/columns
- fields are separated by commas ","
- commas inside a data field surrounded by quotes (") are not separators, but part of the data
- quotes inside data fields are escaped using an extra double quote (ie. 19" becomes 19"")
- data fields may contain newline characters (meaning a single data field may span several lines) but is definitely surrounded by quotes in that case.
- See this link to have more information about the CSV format: http://en.wikipedia.org/wiki/Comma-separated_values#Basic_rules

To view the files you can load it in notepad or any other text editor.  If you wish to view the data, the file should load in Excel or OpenOffice (all valid CSV files will load in Excel and OpenOffice).

Your task:

- write a Python program that is a generic CSV parser that reads 'test.csv' and 'test2.csv' as is and transforms the data into Python variables (the parser must be generic in the sense that it should be able to process any valid CSV file).
- we want a variable called 'objects' that is a Python list
- the elements of 'objects' will be Python dictionaries (like a hash table, or mapping object / associative array) containing the data
- the dictionary keys will be the field names given in the header of the CSV (ie. 'id', 'year' etc.)
- print the list of objects sorted by year followed by make and then model (of course, to be able to sort you need to validate that these fields exist in the CSV to do this step; otherwise, just print the output, unsorted)

This should give you an idea of how we want the data stored:

#initialization
objects = []
... your parser code here
... sort list (if applicable)
#print the data
for obj in objects:
print obj['year']   # print some basic info here

Please *do not* use the Python 'csv' module.  You are welcome to search the net for hints, but please list the sources/URLs used.

BONUS Task: If there is a column containing a date in this format "Nov 15 2004  9:13:26:186AM", store that date into a python datetime.


Once completed, please zip and email your results to us.

Thanks, and good luck!
