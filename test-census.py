import pandas as pd
import censusdata
from tabulate import tabulate
sample = censusdata.search('acs5', 2015,'concept', 'language')


#print(sample[0])
#censusdata.printtable(censusdata.censustable('acs5',2015,'B06007PR'))

states = censusdata.geographies(censusdata.censusgeo([('state', '*')]), 'acs5', 2015)
counties = censusdata.geographies(censusdata.censusgeo([('state', '53'), ('county', '*')]), 'acs5', 2015)
#print(states['Washington'])
#print(counties)

#data = censusdata.download('acs5',2015,censusdata.censusgeo([('state','53'),('county', '071'),('block group','*')]),
#        ['B06007PR_020E','B06007PR_021E','B06007PR_023E','B06007PR_024E'])
data = censusdata.download('acs5',2015,censusdata.censusgeo([('state','53'),('county', '*'),('block group','*')]),
        ['B08301_001E', 'B08301_010E'])
print(tabulate(data, headers='keys', tablefmt='psql'))
column_names = ['total_transpo', 'total_public_transpo']
data.columns = column_names

data['percent_public_transpo'] = data.apply(
           lambda row: row['total_public_transpo']/row['total_transpo'], 
              axis = 1)

new_indices = []
county_names = []
for index in data.index.tolist():
    new_index = index.geo[0][1] + index.geo[1][1]
    new_indices.append(new_index)
    county_name = index.name.split(',')[0]
    county_names.append(county_name)
    
data.index = new_indices
data['county_name'] = county_names
data['fips'] = data.index

from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

        counties["features"][0]


import plotly.express as px
fig = px.choropleth(data, geojson=counties, locations='fips', color='percent_public_transpo',
      color_continuous_scale="Viridis",
      range_color=(0, 1),
      scope="usa",
      labels={'percent_public_transpo':'WA Public Transit Use by County'})

#import plotly.figure_factory as ff
#fig = ff.create_choropleth(fips=data.index, 
#                                   scope=['Washington'],
#                                   values=data.percent_public_transpo, 
#                                   title='WA Public Transit Use by County', 
#                                   legend_title='% Public Transit')
fig.layout.template = None
fig.show()

#print(data.columns)
#print(data.axes)
