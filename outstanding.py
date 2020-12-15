import pandas as pd
import pyodbc as db
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
from datetime import datetime
import os
import sys

conn = db.connect('DRIVER={SQL Server};'
                        'SERVER=;'                     # Provide server
                        'DATABASE=;'                   # provide database 
                        'UID=;PWD=')                   # provide username and password

def numberInCrore(number):
    number = number / 10000000
    number = round(number,2)
    number = format(number, ',')
    number = number + ' Cr'
    return number

import set_name as employ_name
Employee_name=employ_name.name()
employee_search_name='%'+Employee_name+'%'

outstanding_df = pd.read_sql_query(""" declare @fromdate varchar(6)=CONVERT(varchar(6), dateAdd(day,0,getdate()-1), 112)
declare @yeardate varchar(4)=CONVERT(varchar(4), dateAdd(day,0,getdate()), 112)
select NSMNAME,EMPSHORTNAME,terms, ISNULL(SUM(Outstanding),0) as Outstanding from
(select  NSMID,NSMNAME,rsmtr from RFieldForce
where yearmonth=@fromdate and nsmname like ? --and ccmsotr = 'ccd46'
group by NSMID,NSMNAME, rsmtr) as nsm
left join
(select
case when terms='Cash' then 'Cash' else 'Credit' end as terms,
case when left(msotr,2) = 'CC' then LEFT(MSOTR,3) else rsmtr end as RSMTR,
SUM(OUT_NET) as Outstanding from ARCOUT.dbo.CUST_OUT where LEFT(INVDATE,4)=@yeardate
group by case when left(msotr,2) = 'CC' then LEFT(MSOTR,3) else rsmtr end
, case when terms='Cash' then 'Cash' else 'Credit' end) as cout
on nsm.rsmtr=cout.rsmtr
left join
(select EMPID,EMPSHORTNAME from RFieldForce_SHORT
) as short
on short.EMPID=nsm.NSMID
and NSMNAME like ?
and short.EMPSHORTNAME is not null
group by NSMNAME,EMPSHORTNAME,terms
order by terms""", conn,params=(employee_search_name,employee_search_name))

all_label=outstanding_df['terms'].to_list()
print(all_label)
all_values=outstanding_df['Outstanding'].to_list()
print(all_values)

# sys.exit()
cash = int(all_values[0])
credit = int(all_values[1])

data = [cash, credit]
total = cash + credit
total = 'Total \n' + numberInCrore(total)

colors = ['#A42955', '#db7515']
fig, ax = plt.subplots(figsize=(8, 4),facecolor='#011936', subplot_kw=dict(aspect="equal"))

recipe = ["Cash   \n "+str(numberInCrore(cash)),
          "  Credit\n"+str(numberInCrore(credit))]


wedges, texts ,autopct= ax.pie(data, wedgeprops=dict(width=0.4), startangle=90,colors=colors, autopct='%.1f%%', textprops={
        'color':"white"},pctdistance=.8)

plt.setp(autopct, fontsize=12, fontweight='bold')

ax.text(0, -.1, total, ha='center', fontsize=13, fontweight='bold',color='white')

bbox_props = dict(boxstyle="square,pad=0.3", fc='y', ec="k", lw=0.72)
kw = dict(arrowprops=dict(arrowstyle="-",color='white'),
          bbox=bbox_props, zorder=0, va="center",fontsize=13,fontweight='bold')

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax.annotate(recipe[i], xy=(x, y), xytext=(1.5*np.sign(x), 1.3*y),
                horizontalalignment=horizontalalignment, **kw)
# plt.title('Total Outstanding', fontsize=16, fontweight='bold', color='black')
plt.rcParams['savefig.facecolor'] = '#011936'
plt.tight_layout()
# plt.show()
plt.savefig('./images/outstanding_donut.png', transparent=False)
print('outstanding circle generated')