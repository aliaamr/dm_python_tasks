#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Name : Alia Amr | Track : Data Management | Mail : aliaamr2110@gmail.com


# ### Step 0
# Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']`
# 
# Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
# 
# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, 
# 
# e.g. 
# 
# `'Bolivia (Plurinational State of)'` should be `'Bolivia'`, 
# 
# `'Switzerland17'` should be `'Switzerland'`.

# In[12]:


# Import pandas package 
import pandas as pd
# Import numy package
import numpy as np
# Now, we will work with IMDB dataset
data_extraction = pd.ExcelFile('/home/aliaamr/Documents/Material/data/Energy Indicators.xls')
energy = data_extraction.parse(skiprows=17,skip_footer=(38),usecols=[1,3,4,5],
                               names=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'])

# make sure missing data is reflected as np.NaN values.
columns = ['Energy Supply', 'Energy Supply per Capita', '% Renewable']
energy[columns] = energy[columns].replace('...',np.NaN)
# convert Energy Supply to gigajoules
energy.loc['Energy Supply'] = energy['Energy Supply']*(10**6)
# rename the following list of countries
energy['Country'] = energy['Country'].replace({'China, Hong Kong Special Administrative Region':'Hong Kong',
                                               'United Kingdom of Great Britain and Northern Ireland':'United Kingdom',
                                               'Republic of Korea':'South Korea','United States of America':'United States',
                                               'Iran (Islamic Republic of)':'Iran'})
# there are several countries with numbers and/or parenthesis in their name. Be sure to remove them
energy['Country'] = energy['Country'].str.replace(r" \(.*\)","")

print(energy.count())


# In[ ]:


print('-'*40)
print('Step 0 done successfully')
print('_'*40)


# ### Step 1
# <br>
# 
# Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# <br>

# In[13]:


GDP = pd.read_csv('/home/aliaamr/Documents/Material/data/world_bank.csv', header = 4)

GDP['Country Name'].replace({"Korea, Rep.":"South Korea", 
                             "Iran, Islamic Rep.":"Iran",
                             "Hong Kong SAR, China": "Hong Kong"}
                            , inplace=True)
print(GDP.count())


# In[ ]:


print('-'*40)
print('Step 1 done successfully')
print('_'*40)


# ### Step 2
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.

# In[14]:


ScimEn = pd.read_excel('/home/aliaamr/Documents/Material/data/scimagojr-3.xlsx')
print(ScimEn.count())


# In[ ]:


print('-'*40)
print('Step 2 done successfully')
print('_'*40)


# ### Step 3
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# 
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
# 
# *This step should yeild a DataFrame with 20 columns and 15 entries.*

# In[15]:


# ScimEn
# only the top 15 countries
ScimEn = ScimEn[:15]

# GDP
# only the last 10 years (2006-2015)
GDP = GDP[['Country Name','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']]
GDP.columns = ['Country','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']

energy_GDP = pd.merge(energy, GDP,how='inner', left_on='Country', right_on='Country')

# Merge ScimEn & energy
df1 = pd.merge(ScimEn, energy, how='inner', left_on='Country', right_on='Country')
# Merge (ScimEn & energy) & GDP
df2 = pd.merge(df1, GDP,how='inner', left_on='Country', right_on='Country')
# set index for the table
df2 = df2.set_index('Country')


# In[16]:


print(df2.shape)


# In[ ]:


print('-'*40)
print('Step 3 done successfully')
print('_'*40)


# ### Step 4
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# 
# *This step should yield a single number.*

# In[ ]:


171


# In[ ]:


print('-'*40)
print('Step 4 done successfully')
print('_'*40)


# ### Step 5
# 
# #### Answer the following questions in the context of only the top 15 countries by Scimagojr Rank 
# 
# 
# What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
# 
# *This step should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*

# In[5]:


# 15 countries 
# average GDP 
# descending order
data = df2
years = ['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']
avgGDP = data[years].mean(axis = 1).rename('avgGDP').sort_values(ascending= True)
print(avgGDP)


# In[ ]:


print('-'*40)
print('Step 5 done successfully')
print('_'*40)


# ### Step  6
# What is the mean `Energy Supply per Capita`?
# 
# *This step should return a single number.*

# In[6]:


# print(data.iloc[:,8])
meanESPC = data.iloc[:,8].mean()
print(meanESPC)


# In[ ]:


print('-'*40)
print('Step 6 done successfully')
print('_'*40)


# ### Step 7
# What country has the maximum % Renewable and what is the percentage?
# 
# *This step should return a tuple with the name of the country and the percentage.*

# In[7]:


# idxmax() – > returns the index of the row where column name “% Renewable” has maximum value.
maxRenewable = data.iloc[:,9].max()
country = data['% Renewable'].idxmax()

maxRenewableResult = (country, maxRenewable)
print(maxRenewableResult)


# In[ ]:


print('-'*40)
print('Step 7 done successfully')
print('_'*40)


# ### Step 8
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 
# *This step should return a tuple with the name of the country and the ratio.*

# In[8]:


citationsRatio = data["Self-citations"] / data["Citations"]

citationsRatioResult = (citationsRatio.idxmax(), citationsRatio.max())
print(citationsRatioResult)


# In[ ]:


print('-'*40)
print('Step 8 done successfully')
print('_'*40)


# ### Step 9
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
# 
# *This step should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*

# In[9]:


# the median for all countries in the top 15
medianRenewable = data["% Renewable"].median(axis=0)

# 1 if the country's % Renewable value is at or above the median
# 0 if the country's % Renewable value is below the median
data["HighRenew"] = data.apply(lambda c: 1 if c["% Renewable"] > medianRenewable else 0, axis=1)

#sorted in ascending order of rank
data.sort_values(by='Rank', inplace=True)

print(data["HighRenew"])


# In[ ]:


print('-'*40)
print('Step 9 done successfully')
print('_'*40)


# ### Step 10
# Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# 
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# 
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*

# In[10]:


ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}

data['Estimate Population'] = data['Energy Supply'] / data['Energy Supply per Capita']

continentGroups = pd.DataFrame(columns = ['size', 'sum', 'mean', 'std'])
# size, sum, mean, and std deviation for the estimated population of each country.
for group, df in data.groupby(ContinentDict):
    continentGroups.loc[group] = [len(df),
                         df['Estimate Population'].sum(),
                         df['Estimate Population'].mean(),
                         df['Estimate Population'].std()]
    
print(continentGroups)


# In[ ]:


print('-'*40)
print('Step 10 done successfully')
print('_'*40)

