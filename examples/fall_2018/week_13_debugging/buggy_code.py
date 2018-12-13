# buggy Python script

# cannot write tests of script code
president_elections = {
   'bush': [1988],
   'clinton': [1992, 1996],
   'bush': [2000, 2004],
   'obama': [2008, 2012],
   'trump': [2016]
}

# sort by year
'''
by_year = []
for pres, years in president_elections.items():
    for year in years:
        by_year.append((year, pres))

print(by_year)
'''

# test module-level code
def by_year_fn(years_data):
    results_by_year = []
    for pres, years in president_elections.items():
        for year in years:
            results_by_year.append((year, pres))
    return results_by_year

# print(by_year_fn(president_elections))



    