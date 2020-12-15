import matplotlib.pyplot as plt
import pandas as pd
import pyodbc as db


import set_name as employ_name
Employee_name=employ_name.name()
employee_search_name='%'+Employee_name+'%'

connection = db.connect('DRIVER={SQL Server};'
                        'SERVER=;'                     # Provide server
                        'DATABASE=;'                   # provide database 
                        'UID=;PWD=')                   # provide username and password

cursor = connection.cursor()


nsm_target_sales_df = pd.read_sql_query("""declare @fromdate varchar(6)=CONVERT(varchar(6), dateAdd(day,0,getdate()-1), 112)
declare @yeardate varchar(4)=CONVERT(varchar(4), dateAdd(day,0,getdate()), 112)

select NSMNAME,EMPSHORTNAME, SUM(target) as Target, SUM(sales) as Sales, ISNULL(SUM(Outstanding),0) as Outstanding from
(select  NSMID,NSMNAME,rsmtr,sum(Target) as target from RFieldForce
where yearmonth=@fromdate --and nsmname = 'Mr. Golam Haider' --and ccmsotr = 'ccd46'
group by NSMID,NSMNAME, rsmtr) as nsm
left join 
(select case when left(msotr,2) = 'CC' then LEFT(MSOTR,3) else rsmtr end as rsmtr,
sum(extinvmisc) as sales from OESalesDetails
where LEFT(Transdate,6)=@fromdate
and TRANSTYPE=1
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
order by Sales DESC
""", connection,params={employee_search_name})

monthly_target = nsm_target_sales_df['Target'].tolist()

monthly_sale = nsm_target_sales_df['Sales'].tolist()
print(monthly_target)
print(monthly_sale)
sales = int(monthly_sale[0])
target = int(monthly_target[0])

achievement = round((sales/target)*100,1)
# achievement = 85
if(achievement>100):
    data=[achievement-100, 100-(achievement-100)]
    colors = ['#128e18','#128e18']
    startangle=90
else:
    data = [achievement, 100-achievement]
    colors = ['#128e18', '#e5cf5b']
    startangle=90

if(achievement<=50):
    color1 = '#ff1a1a'
elif(achievement<=79):
    color1 = '#e5cf5b'
elif(achievement<=200):
    color1 = '#128e18'
# -----------------------------------------------------

fig1, ax = plt.subplots(figsize=(2.1,2.1),facecolor='#011936')
wedges, labels= ax.pie(data,radius=.06, colors=colors, startangle=startangle)
ax.text(0, -.006, str(round(achievement,1))+'%', ha='center', fontsize=22, fontweight='bold',color=color1)
#
centre_circle = plt.Circle((0, 0), 0.05, fc='#011936')

fig = plt.gcf()

fig.gca().add_artist(centre_circle)

# plt.title('Title of pie', fontsize=16, fontweight='bold', color='#ff6138')

ax.axis('equal')
plt.rcParams['savefig.facecolor'] = '#011936'
plt.tight_layout()
# plt.show()
plt.savefig('./images/achievement_hour.png', transparent=False)
print('work hour achieve circle generated')