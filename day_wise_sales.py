import os

dirpath = os.path.dirname(os.path.realpath(__file__))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyodbc as db

def crore(number):
    number = number / 10000000
    number = round(number,2)
    number = format(number, ',')
    number = number + ' Cr'
    return number

connection = db.connect('DRIVER={SQL Server};'
                        'SERVER=;'                     # Provide server
                        'DATABASE=;'                   # provide database 
                        'UID=;PWD=')                   # provide username and password

cursor = connection.cursor()

# import set_name as employ_name
# Employee_name=employ_name.name()

Employee_name = "Mr. Golam Haider"
employee_search_name='%'+Employee_name+'%'

daily_sales_df = pd.read_sql_query("""select right(TRANSDATE,2) as days,sum(total) as sale from
(select distinct MSOTR, SUM(extinvmisc) as total,TRANSDATE from OESALESDETAILS
where LEFT(TRANSDATE,6)=CONVERT(varchar(6), dateAdd(day,0,getdate()), 112)
--and TRANSTYPE=1
group by transdate,MSOTR) as a
left join
(select distinct msotr,NSMID,NSMNAME from rfieldforce
where yearmonth=CONVERT(varchar(6), dateAdd(day,0,getdate()), 112)) as b
on a.MSOTR = b.msotr
where NSMNAME like ?
group by right(TRANSDATE,2)
order by right(TRANSDATE,2) asc""", connection,params={employee_search_name})


Every_day = daily_sales_df['days'].tolist()
print(Every_day)
y_pos = np.arange(len(Every_day))
print(y_pos)
every_day_sale = daily_sales_df['sale'].tolist()
print(every_day_sale)
for i in range(0, len(every_day_sale)):
    every_day_sale[i] = float(every_day_sale[i])
print(every_day_sale)
x = np.arange(len(Every_day))

fig, ax = plt.subplots(figsize=(12.5, 4),facecolor='#011936')

# width = 0.35  # the width of the bars

rects2 = ax.bar(y_pos, every_day_sale, label='Sales',color='#0A58DE')
# line = ax.plot(Target, color='green', label='Target')


plt.yticks([])
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.set_xticks(x)
# ax.legend(fontsize=6,loc='upper right')
ax.set_xticklabels(Every_day,color='black')
ax.tick_params(axis='y', colors='white', labelsize=14)
ax.tick_params(axis='x', colors='white', labelsize=14)
ax.set_facecolor("#011936")


# plt.text(x[0], Target[0]+1000, format(Target[0], ',')+'K',fontsize=9,color='green', fontweight='bold')

def autolabel(bars):
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height,
                crore(height),
                    ha='center', va='bottom',color='white', fontsize=12, rotation=0, fontweight='bold')

autolabel(rects2)
plt.rcParams['savefig.facecolor'] = '#011936'
fig.tight_layout()
# plt.show()
plt.savefig("./images/Day_Wise_sale.png")
print('7. Day Wise Target vs Sales Generated')
#plt.close()