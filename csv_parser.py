# -*- coding: utf-8 -*-
"""
    CSV parser to test.csv, test2.csv and other csv files separate by
    comma between double quotes
"""
__author__ = 'Michel-Alexandre Bélanger (michel.alexandre.belanger@gmail.com)'

# modules imports
import re
from datetime import datetime

# Constants
CARTOON = "cartoon"
CAR = "car"
DELEMITER = '\n'

def _get_csv_sting( file_name, type ):
    """
    This function remove all new lines to the file and replace it by space
    and return that string
    """
    if type:
        lines_lst = [line.strip() for line in open(file_name)]
        csv_str = ' '.join(lines_lst)
        return csv_str
    else :
        return open(file_name, 'r').read()

def _get_re_pat( type ):
    """
    Build a regex pattern from the type (CARTOON, CAR or None)
    """

    if not type:
        return re.compile('[\r\n]+')

    if type == CARTOON :
        prefix_re = '"[^"]*"'
    elif type == CAR :
        prefix_re = '\d*'

    month_re = ',"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
    day_re = ' *.\d'
    year_re = ' *\d{4}'
    hour_re = ' *\d*:\d{2}:\d{2}:\d{3}(?:AM|PM)",'
    
    # Merge all the criteria of the regex
    return re.compile(prefix_re + month_re + day_re + year_re + hour_re)

def _get_record_csv_lst( csv_str, type ):
    """
    if type exist split the record we use the date and the precedent field 
    the precedent field of cartoon is a string within the quote
    and the precedent field of car is the id example : 
    car :`378795,"Nov 15 2004  9:05:26:976AM",'
    cartoon :`"Winnie, The Pooh","Nov 15 2004  9:01:00:596AM",'
    
    If type do not exist the split of record is done by new line
    """
    reg_pat = _get_re_pat(type)

    # The the rest of the string of the record in a list
    s_rec_csv = re.split(reg_pat, csv_str)
    
    if not type:
        # If type is not specified, return only the record split by line
        return s_rec_csv

    # The date of the record in a list
    f_rec_csv = re.findall(reg_pat, csv_str)
    
    # Joint the date and the rest of the record in a list
    record_csv_lst = []
    for x, y in map(None, s_rec_csv[1:], f_rec_csv):
        record_csv_lst.append(y + x)
    return record_csv_lst

def _get_record_lst( record_csv_lst ):
    """
    Convert the csv into a record_lst to do so, we need to replace all 
    string separator '","' and ',"' and then '",' by delimiter. The
    list of data for each record is build by the delimiter.
    """
    record_lst = []
    # for each csv record, build a list of data and put it into a record list
    for record_csv in record_csv_lst: 
        record_csv = record_csv\
            .replace('","', DELEMITER)\
            .replace(',"', DELEMITER)\
            .replace('",', DELEMITER)

        # Build a list with the delimiter
        obj_data_lst = record_csv.split(DELEMITER)
        
        # Remove the quote only at the end of the string (data)
        obj_data_lst = [s.strip('" ') for s in obj_data_lst]

        record_lst.append(obj_data_lst)
    return record_lst
    
def __get_obj_dic( obj_data_lst, type ):

    """
    Convert the object list of data to the dictionnary that key depends on
    the type. If the number of the data don't correspond to the number
    key of the type, it raise an exception.  
    """
    def get_pydate( date_str ):
        """
        convert unix format date "Nov 15 2004  9:13:26:186AM" into 
        python datetime
        """
        return datetime.strptime(date_str, '%b %d %Y %I:%M:%S:%f%p')

    CARTOON_KEYS_LST = ["name", "entrydate", "age", "sex", "country",
                        "province", "city", "options", "permissions",
                        "comments","year","make","model"]
    
    CAR_KEYS_LST = ["id", "entrydate", "year", "make", "model", "colore",
                    "intcolorf", "leasingoptions", "financingoptions", 
                    "noteextrae"]

    if type == CARTOON :
        nb_data = len(CARTOON_KEYS_LST)
        keys_lst = CARTOON_KEYS_LST

    elif type == CAR :
        nb_data = len(CAR_KEYS_LST)
        keys_lst = CAR_KEYS_LST

    if type :
        # Check the type
        if len(obj_data_lst) != nb_data :
            # Raise an error if the nb_key don't 
            # correspond to the number of data
            raise Exception("The number of data in obj_data_lst is not = %d" 
                            %(nb_data))
        # Convert keys_lst list and obj_data_lst list to dictionnary
        obj_dic = dict(zip(keys_lst, obj_data_lst))
    else :
        # The position in the list is used as key
        obj_dic = dict(zip(range(len(obj_data_lst)), obj_data_lst))

    if "entrydate" in obj_dic:
        # Convert unix date into python date
        obj_dic['entrydate'] = get_pydate(obj_dic['entrydate'])

    return obj_dic

def _get_obj_dic_lst( record_lst, type ):
    """
    Loop over all record list and use __get_obj_dic to build the 
    obj_dic_lst, catch the exception and print it
    """
    obj_dic_lst = []
    # For each record list
    for obj_data_lst in record_lst:
        try:
            # Append the obj_dic to the list
            obj_dic_lst.append(__get_obj_dic(obj_data_lst, type))
        except Exception, e:
            # if len(obj_data_lst) != nb_data, print error
            print str(e)

    return obj_dic_lst

def _get_obj_dic_sorted_lst( obj_dic_lst ):
    """
    Sort all the objects
    """
    def mixed_order( x ):
        return ( x["year"], x["make"], x["model"] )

    return sorted(obj_dic_lst, key=mixed_order)

def get_obj_dic_sorted_lst( file_name, type ):
    """
    Call the step to transformation
    1) Remove the new line from the text
    2) Split the text into record list without delemiting the data
    3) For each record, split the record into data list
    4) For each record, convert the data list to the dictionnary
    5) Return a sorted list of dictionnary object if type exist
    """
    csv_str = _get_csv_sting (file_name, type)
    record_csv_lst = _get_record_csv_lst(csv_str, type)
    record_lst = _get_record_lst(record_csv_lst)
    obj_dic_lst = _get_obj_dic_lst( record_lst, type )

    if type :
        return _get_obj_dic_sorted_lst(obj_dic_lst)
    else :
        return obj_dic_lst

def print_obj_dic( obj_dic_sorted_lst ):
    """
    For each object sorted, print the year, make and model
    """
    for object in obj_dic_sorted_lst : 
        print object["year"], " ", object["make"], " ", object["model"]

if __name__ == "__main__":
    """
    Call test.csv, test2.csv and test3.csv
    """
    print_obj_dic(get_obj_dic_sorted_lst("test.csv", CAR))
    print_obj_dic(get_obj_dic_sorted_lst("test2.csv", CARTOON))
    print get_obj_dic_sorted_lst("test3.csv", None)
