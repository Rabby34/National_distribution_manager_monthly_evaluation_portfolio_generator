import matplotlib.pyplot as plt
import pandas as pd
import pyodbc as db
import numpy as np
from matplotlib.patches import Patch
from PIL import Image, ImageDraw, ImageFont
import sys

def convert(number):
    number = number / 1000
    number = int(number)
    number = format(number, ',')
    number = number + 'K'
    return number

connection = db.connect('DRIVER={SQL Server};'
                        'SERVER=;'                     # Provide server
                        'DATABASE=;'                   # provide database 
                        'UID=;PWD=')                   # provide username and password

cursor = connection.cursor()

import set_name as employ_name
Employee_name=employ_name.name()
employee_search_name='%'+Employee_name+'%'


ever_sale_df = pd.read_sql_query("""select right(TRANSDATE,2) as days,sum(total)/10000000 as sale from
(select distinct MSOTR, SUM(extinvmisc) as total,TRANSDATE from OESALESDETAILS
where LEFT(TRANSDATE,6)=CONVERT(varchar(6), dateAdd(day,0,getdate()), 112)
and TRANSTYPE=1
group by transdate,MSOTR) as a
left join
(select distinct msotr,NSMID,NSMNAME from rfieldforce
where yearmonth=CONVERT(varchar(6), dateAdd(day,0,getdate()), 112)) as b
on a.MSOTR = b.msotr
where NSMNAME like ?
group by right(TRANSDATE,2)
order by right(TRANSDATE,2) asc""", connection,params={employee_search_name})

all_days_in_month=ever_sale_df['days'].tolist()
day_to_day_sale = ever_sale_df['sale'].tolist()
print(all_days_in_month)
print(day_to_day_sale)


from datetime import date

today = date.today()

current_day = today.strftime("%d")
current_day_in_int=int(current_day)
# print(current_day_in_int)

# sys.exit()
final_days_array=[]
final_sales_array=[]

for t_va in range(0, current_day_in_int):
    #print(t_va)
    final_days_array.append(all_days_in_month[t_va])
    final_sales_array.append(day_to_day_sale[t_va])


print(final_days_array)
print(final_sales_array)
# print(final_return_array)

EveryD_Target2_df = pd.read_sql_query("""declare @fromdate varchar(6)=CONVERT(varchar(6), dateAdd(day,0,getdate()-1), 112)
declare @yeardate varchar(4)=CONVERT(varchar(4), dateAdd(day,0,getdate()), 112)

select NSMNAME,EMPSHORTNAME, SUM(target)/10000000 as Target, SUM(sales) as Sales, ISNULL(SUM(Outstanding),0) as Outstanding from
(select  NSMID,NSMNAME,rsmtr,sum(Target) as target from RFieldForce
where yearmonth=@fromdate --and nsmname = 'Mr. Golam Haider' --and ccmsotr = 'ccd46'
group by NSMID,NSMNAME, rsmtr) as nsm
left join
(select case when left(msotr,2) = 'CC' then LEFT(MSOTR,3) else rsmtr end as rsmtr,
sum(extinvmisc) as sales from OESalesDetails
where LEFT(Transdate,6)=@fromdate
--and TRANSTYPE<>1
--and case when left(msotr,2) = 'CC' then LEFT(MSOTR,3) else rsmtr end in ('CD', 'CR', 'CS', 'CT', 'DM', 'NM', 'NM')
group by case when left(msotr,2) = 'CC' then LEFT(MSOTR,3) else rsmtr end) as sales
on nsm.rsmtr=sales.rsmtr
left join
(select case when left(msotr,2) = 'CC' then LEFT(MSOTR,3) else rsmtr end as RSMTR,
SUM(OUT_NET) as Outstanding from ARCOUT.dbo.CUST_OUT where LEFT(INVDATE,4)=@yeardate
group by case when left(msotr,2) = 'CC' then LEFT(MSOTR,3) else rsmtr end) as cout
on sales.rsmtr=cout.rsmtr
left join
(select EMPID,EMPSHORTNAME from RFieldForce_SHORT
) as short
on short.EMPID=nsm.NSMID
where target<>'0'
and NSMNAME like ?
and short.EMPSHORTNAME is not null
group by NSMNAME,EMPSHORTNAME
order by Sales DESC""", connection,params={employee_search_name})
totarget = EveryD_Target2_df['Target'].tolist()
# print(y_pos)
import calendar
import datetime

now = datetime.datetime.now()
total_days = calendar.monthrange(now.year, now.month)[1]
print(total_days)

target_for_target = totarget[ 0]/total_days
print(target_for_target)
# print(totarget)
# sys.exit()
y_pos = np.arange(len(final_days_array))

n = 1

labell_to_plot = []
for z in y_pos:
    labell_to_plot.append(n)
    n = n + 1


print(labell_to_plot)
#labell.append(20)

#sys.exit()
# ----------------code for cumulitive sales------------

new_target = target_for_target
labell_to_plot
z = len(labell_to_plot)
# print(len(labell))
fin_target = 0
cumulative_target_that_needs_to_plot = []
for t_value in range(0, total_days + 1):
    # print(t_value)
    fin_target = new_target * t_value
    # print(fin_target)
    cumulative_target_that_needs_to_plot.append(fin_target)
    fin_target = 0
print(cumulative_target_that_needs_to_plot) #-------------------target data

values = final_sales_array
length = len(values)

new_array = [0]
final = 0
for val in values:
    # print(val)
    get_in = values.index(val)
    # print(get_in)
    if get_in == 0:
        new_array.append(val)
    else:
        for i in range(0, get_in + 1):
            final = final + values[i]
        new_array.append(final)
        final = 0

# print(every_day_sale)
print(new_array)#--------------------------sales data

new_array_of_return = [0]
final_value_of_ret = 0

# print(new_array_of_return)

x = range(len(cumulative_target_that_needs_to_plot))
xx = range(len(new_array))

list_index_for_target = len(cumulative_target_that_needs_to_plot) - 1
# print(list_index_for_target)

list_index_for_sale = len(new_array) - 1
# print(list_index_for_sale)
fig, ax = plt.subplots(figsize=(12.5, 4),facecolor='#011936')
plt.fill_between(x, cumulative_target_that_needs_to_plot, color="#0A58DE", alpha=1)
plt.plot(xx, new_array, color="white", linewidth=3, linestyle="-")


# plt.text(list_index_for_sale-1, cumulative_target_that_needs_to_plot[list_index_for_sale]+6, format(round(cumulative_target_that_needs_to_plot[list_index_for_sale],1),',') + ' Cr',
#          color='black', fontsize=15, fontweight='bold')
plt.scatter(list_index_for_sale, cumulative_target_that_needs_to_plot[list_index_for_sale], s=60, facecolors='white', edgecolors='white')
plt.text(list_index_for_sale+.2, new_array[list_index_for_sale]+1, format(round(new_array[list_index_for_sale],1),',') + ' Cr',
         color='white', fontsize=15, fontweight='bold')
plt.scatter(list_index_for_sale, new_array[list_index_for_sale], s=60, facecolors='white', edgecolors='white')

plt.text(list_index_for_target-1, cumulative_target_that_needs_to_plot[list_index_for_target]+1, format(round(cumulative_target_that_needs_to_plot[list_index_for_target],1),',') + ' Cr',
         color='white', fontsize=15, fontweight='bold')
plt.scatter(list_index_for_target, cumulative_target_that_needs_to_plot[list_index_for_target], s=60, facecolors='white', edgecolors='white')

ax.yaxis.set_visible(False)
ax.set_facecolor("#011936")
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.tick_params(axis='x', colors='white')
plt.rcParams['savefig.facecolor'] = '#011936'
plt.tight_layout()
plt.savefig("./images/Cumulative_Day_Wise_Target_vs_Sales.png")
# plt.show()
# plt.close()
print('7. Cumulative day wise target sales')