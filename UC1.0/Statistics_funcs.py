from math import floor, ceil, sqrt

def clense_data(lst):
    while None in lst: lst.remove(None)
    return lst

def mean(lst):
    lst = clense_data(lst)
    return sum(lst) / len(lst)

def median(lst):
    lst = clense_data(lst)
    lst.sort()
    mid = len(lst) // 2
    med =  (lst[mid] + lst[~mid]) / 2 #/ ~mid = -(mid+1)
    
    return med

def mode(lst):
    lst = clense_data(lst)
    lst.sort() 
  
    L1=[]

    i = 0
    while i < len(lst) :
        L1.append(lst.count(lst[i]))
        i += 1

    d1 = dict(zip(lst, L1))
    
    modes = [k for (k,v) in d1.items() if v == max(L1) ]
    
    if modes == lst:
        return "No Mode"
    
    return modes

def range(lst):
    lst = clense_data(lst)
    return max(lst) - min(lst)

def sum_of_squares(lst):
    lst = clense_data(lst)
    m = mean(lst)
    return sum([(x-m)**2 for x in lst])

def iqr(lst):
    lst = clense_data(lst)
    mid = len(lst)/ 2
    Q1 = median(lst[0:floor(mid)])
    Q3 = median(lst[ceil(mid):])
    
    return Q3 - Q1

def variance(lst, sample = True):
    lst = clense_data(lst)
    if sample:
        den = len(lst) - 1
    else: #Population
        den = len(lst)
        
    return sum_of_squares(lst)/ den

def std_dev(lst, sample = True):
    lst = clense_data(lst)
    return sqrt(variance(lst, sample))

# sum function for sum of the given data




