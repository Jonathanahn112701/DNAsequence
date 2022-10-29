# Author: Jonathan Ahn jxa5570@psu.edu
from sys import argv
import csv
import time

def db_getstrs():
  ''' 
  Opens first argument which is a data base file and returns its header in order to find the corresponding STRs. 
  '''
  with open(argv[1]) as dbfile:
    reader = csv.DictReader(dbfile)
    db_header = reader.fieldnames
  return db_header[1:]

def get_dbdict():
  '''
  this function opens the first agrument which is the crime database file and will use the db_getstrs() function in order to get the STRs and will iterate through each row of the file's csv file in order to create a dictionary with a key as the crime ID and the key value to be a tuple of each crime ID's STR count. This dictionary will be the return value
  '''
  with open(argv[1], newline ='') as dbfile:
    csvdbfile = csv.DictReader(dbfile, dialect ='excel')
    STRs = db_getstrs()
    dict1 = {}
    for row in csvdbfile:
      list1 = []
      for STR in STRs:
        list1.append(int(row[STR]))
      tulist = tuple(list1)
      dict1[row['CrimeID']] = tulist
    return dict1

def get_susdict():
  '''
  this function will open argument 2 which will be the suspect file then get the strs that are needed to find for this suspect then will iterate through the csv file and will find the maximum reoccurences of each STR (by using the str_count function) into a tuple which will be the key value of a dictionary that will be returned, and it's key will be the suspect's name (example: 'A').
  '''
  with open(argv[2], newline = '') as susfile:
    csvfile = csv.DictReader(susfile, dialect = 'excel')
    dict1 = {}
    strs = db_getstrs()
    for row in csvfile:
      sequence = row['Sequence']
      list1 = []
      for STR in strs:
        strcounter = str_count(sequence, STR)
        list1.append(strcounter)
      tulist = tuple(list1)
      dict1[row['Suspect']] = tulist
    return dict1
  
def str_count(sequence, STR):
  '''
  given a sequence and a STR it will find the most reoccurence of the STR within the sequence. It does so by establishing i to be the first occurence of the STR (if it is not in the sequence it will return 0) then looping through until i is greater than the length of the sequence. Throughout this loop it checks if the str is equivalent to the str right after it and if this string is the STR it will increase the count. However, whenever the STR is not found right after the next STR it will make the count 1 again. After this it will check if the count is greater than the maxcount therefore finding the maximum count from all of the reoccuring STR. This function returns the maximum count. 
  '''
  i = sequence.find(STR)
  if i == -1:
    return 0
  elif sequence.count(STR) == 1:
    return 1
  else:
    count = 1
    maxcount = 1
    while i <= len(sequence):
      if sequence[i:i+len(STR)] == sequence[i+len(STR):i+(2*len(STR))]:
        if sequence[i:i+len(STR)] == STR:
          count += 1 
          i += len(STR)
        else:
          count = 1
          i += 1
      else:
        count = 1
        i += 1
      if count > maxcount:
        maxcount = count
    return maxcount

def invert_dict1(d):
  '''
  given a dictionary, this function will return the inverse dictionary by swapping the dictionary's key with its value. Also, if this value is already in the new dictionary it will append to that list in order to avoid removal of duplications. 
  '''
  inverse = {}
  for key in d:
    val = d[key]
    if val not in inverse:
      inverse[val] = [key]
    else:
      inverse[val].append(key)
  return inverse

def invert_dict2(d):
  '''
  this function is very similar to invert_dict1 but the difference is it will not look for duplicates within the new dictionary therefore making the new value a string and not a list. 
  '''
  inverse = {}
  for key in d:
    val = d[key]
    inverse[val] = key

  return inverse

def run():
  '''
  opens the third argument which will be the file name that will be written into. It will also find the inverse of get_dbdict and get_susdict so it will be easier to compare STR counts. Next, it will iterate through the STR's of the new suspect dictionary (that is inverted) and will check if each suspect's STR count has a match with the database if it does it will assign a new dictionary with the suspect name and crime id. Finally, these dictionaries will be appended to a list which will be written into the new file.
  '''
  headers = ['Suspect', 'Crimes']
  with open(argv[3], 'w', newline='') as newfile:
    csvnew = csv.DictWriter(newfile, headers)
    csvnew.writeheader()
    dbdict = invert_dict1(get_dbdict())
    susdict = invert_dict2(get_susdict())
    rows = []
    for STR in susdict:
      dict1 = {}
      if STR in dbdict:
        CID = dbdict[STR]
        Sus = susdict[STR]
        CID1 = ",".join(CID)
        dict1['Suspect'] = Sus
        dict1['Crimes'] = CID1
      else:
        Sus = susdict[STR]
        dict1['Suspect'] = Sus
        dict1['Crimes'] = ''
      rows.append(dict1)
    csvnew.writerows(rows)
  
  return

if __name__ == "__main__":
  start = time.perf_counter()
  run()
  end = time.perf_counter()
  print(f"Time used: {end-start} seconds")
