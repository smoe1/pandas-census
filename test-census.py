import pandas as pd
import censusdata
sample = censusdata.search('acs5', 2015,'concept', 'transportation')

print(len(sample)) 
