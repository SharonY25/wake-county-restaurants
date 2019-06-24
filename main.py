import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.options.display.max_colwidth = 200


restaurant = pd.read_csv('data/wake-county/Restaurants_in_Wake_County.csv')
violation = pd.read_csv('data/wake-county/Food_Inspection_Violations.csv')
inspection = pd.read_csv('data/wake-county/Food_Inspections.csv')

# print(restaurant.head())
# print(violation.head())
# print(inspection.head())


# print(restaurant.describe())
# print(violation.describe())
# print(inspection.describe())

violation_counts = violation.groupby('VIOLATIONCODE').count().sort_values(['OBJECTID'], ascending=False)
violation_counts_20 = violation_counts[0:20]
ax = sn.barplot(y=violation_counts_20.index, x=violation_counts_20['OBJECTID'])
ax.set(xlabel='number of violations', ylabel='violation code')
#print(inspection[inspection['SCORE']>0][inspection['SCORE']<75])
#print(inspection[inspection['SCORE']==0])
#sn.distplot(inspection[inspection['SCORE']>0]['SCORE'])
plt.show()
