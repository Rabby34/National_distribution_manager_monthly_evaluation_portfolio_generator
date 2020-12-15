import pandas as pd
import pyodbc as db
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
from datetime import datetime
import os

connection = db.connect('DRIVER={SQL Server};'
                        'SERVER=;'                     # Provide server
                        'DATABASE=;'                   # provide database 
                        'UID=;PWD=')                   # provide username and password

def numberInCrore(number):
    number = number / 10000000
    number = round(number,2)
    number = format(number, ',')
    number = number + 'Cr'
    return number

import set_name as employ_name
Employee_name=employ_name.name()
employee_search_name='%'+Employee_name+'%'

CloseTo_mature_df = pd.read_sql_query("""declare @fromdate varchar(6)=CONVERT(varchar(6), dateAdd(day,0,getdate()-1), 112)
declare @yeardate varchar(4)=CONVERT(varchar(4), dateAdd(day,0,getdate()), 112)
select NSMNAME,EMPSHORTNAME,aging, ISNULL(SUM(Outstanding),0) as Outstanding from
(select  NSMID,NSMNAME,rsmtr from RFieldForce
where yearmonth=@fromdate and nsmname like ? --and ccmsotr = 'ccd46'
group by NSMID,NSMNAME, rsmtr) as nsm
left join
(select  CASE
    WHEN DATEDIFF(day,convert(datetime, convert(varchar(10), INVDATE), 112),Getdate() )<=30 THEN '30 Days'
    WHEN DATEDIFF(day,convert(datetime, convert(varchar(10), INVDATE), 112),Getdate() )>30 
 and DATEDIFF(day,convert(datetime, convert(varchar(10), INVDATE), 112),Getdate() )<=45 THEN '45 Days'
   WHEN DATEDIFF(day,convert(datetime, convert(varchar(10), INVDATE), 112),Getdate() )>45 
 and DATEDIFF(day,convert(datetime, convert(varchar(10), INVDATE), 112),Getdate() )<=60 THEN '60 Days'
   WHEN DATEDIFF(day,convert(datetime, convert(varchar(10), INVDATE), 112),Getdate() )>60 
 and DATEDIFF(day,convert(datetime, convert(varchar(10), INVDATE), 112),Getdate() )<=90 THEN '90 Days'
   WHEN DATEDIFF(day,convert(datetime, convert(varchar(10), INVDATE), 112),Getdate() )>90 THEN '90+ Days'
    ELSE 'Over 90'
END 

as aging,
case when left(msotr,2) = 'CC' then LEFT(MSOTR,3) else rsmtr end as RSMTR,
SUM(OUT_NET) as Outstanding from ARCOUT.dbo.CUST_OUT where LEFT(INVDATE,4)=@yeardate
group by case when left(msotr,2) = 'CC' then LEFT(MSOTR,3) else rsmtr end
, CASE
    WHEN DATEDIFF(day,convert(datetime, convert(varchar(10), INVDATE), 112),Getdate() )<=30 THEN '30 Days'
    WHEN DATEDIFF(day,convert(datetime, convert(varchar(10), INVDATE), 112),Getdate() )>30 
 and DATEDIFF(day,convert(datetime, convert(varchar(10), INVDATE), 112),Getdate() )<=45 THEN '45 Days'
   WHEN DATEDIFF(day,convert(datetime, convert(varchar(10), INVDATE), 112),Getdate() )>45 
 and DATEDIFF(day,convert(datetime, convert(varchar(10), INVDATE), 112),Getdate() )<=60 THEN '60 Days'
   WHEN DATEDIFF(day,convert(datetime, convert(varchar(10), INVDATE), 112),Getdate() )>60 
 and DATEDIFF(day,convert(datetime, convert(varchar(10), INVDATE), 112),Getdate() )<=90 THEN '90 Days'
   WHEN DATEDIFF(day,convert(datetime, convert(varchar(10), INVDATE), 112),Getdate() )>90 THEN '90+ Days'
    ELSE 'Over 90'
END) as cout
on nsm.rsmtr=cout.rsmtr
left join
(select EMPID,EMPSHORTNAME from RFieldForce_SHORT
) as short
on short.EMPID=nsm.NSMID
and NSMNAME like ?
and short.EMPSHORTNAME is not null
group by NSMNAME,EMPSHORTNAME,aging
order by aging asc
""",connection,params=(employee_search_name,employee_search_name))

# print(CloseTo_mature_df.head())

AgingDays = CloseTo_mature_df['aging']
width = 0.6
y_pos = np.arange(len(AgingDays))
performance = CloseTo_mature_df['Outstanding']

tovalue = sum(performance)
maf_kor = max(performance)
fig, ax = plt.subplots(figsize=(5, 3),facecolor='#011936')
bars = plt.bar(y_pos, performance, width, align='center', alpha=1,color=['#db9690','#db9690','#c86057','#c86057','#b2443a'])

def autolabel(bars):
    for bar in bars:
        height = int(bar.get_height())
        ax.text(bar.get_x() + bar.get_width() / 2., height+6000000,
                str(numberInCrore(height)),
                ha='center', va='bottom',color='white', fontsize=12, rotation=0, fontweight='bold')
        ax.text(bar.get_x() + bar.get_width() / 2., height+2000000,
                '(' + str(round(((height / tovalue) * 100), 1)) + "%)",
                ha='center', va='bottom',color='#0060fc', fontsize=10, rotation=0, fontweight='bold')
        ax.text(bar.get_x() + bar.get_width() / 2., height + 2000000,
                '(' + str(round(((height / tovalue) * 100), 1)) + "%)",
                ha='center', va='bottom', color='#0060fc', fontsize=10, rotation=0, fontweight='bold')

autolabel(bars)

#
# def autolabel2(bars):
#     for bar in bars:
#         height = int(bar.get_height())
#         ax.text(bar.get_x() + bar.get_width() / 2., .5 * height,
#                 str(round(((height / tovalue) * 100), 1)) + "%",
#                 ha='center', va='bottom', fontsize=10, fontweight='bold',color='white')
#
#
# autolabel2(bars)

# plt.xticks(y_pos, AgingDays, fontsize=12)
# plt.yticks(np.arange(0, maf_kor + (.6 * maf_kor), maf_kor / 5), fontsize=12)
# plt.xlabel('Aging Days', color='black', fontsize=14, fontweight='bold')
# plt.yticks(np.arange(0, round(ran) + (.6 * round(ran))), fontsize='12')
# plt.ylabel('Amount', color='black', fontsize=14, fontweight='bold')
plt.axis('off')

# ax.yaxis.set_visible(False)
# ax.set_facecolor("#a1efea")
# ax.spines['right'].set_visible(False)
# ax.spines['left'].set_visible(False)
# ax.spines['top'].set_visible(False)
# ax.spines['bottom'].set_visible(True)
# plt.title('Total Ageing', color='#3e0a75', fontweight='bold', fontsize=12)
plt.tight_layout()
plt.rcParams['savefig.facecolor'] = '#011936'
plt.savefig('./images/aging_outstanding.png')
# plt.show()
print(' aging Generated')