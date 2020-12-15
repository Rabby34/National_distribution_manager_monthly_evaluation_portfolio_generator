from PIL import Image, ImageDraw, ImageFont
import os

img = Image.open("./images/marge_all.png")

brand1_name = ImageDraw.Draw(img)

font1 = ImageFont.truetype("./fonts/Lobster-Regular.ttf", 55, encoding="unic")
font2 = ImageFont.truetype("./fonts/Viga-Regular.ttf", 27, encoding="unic")
font3 = ImageFont.truetype("./fonts/Viga-Regular.ttf", 27, encoding="unic")
font4 = ImageFont.truetype("./fonts/Viga-Regular.ttf", 20, encoding="unic")
font5 = ImageFont.truetype("./fonts/Anton-Regular.ttf", 25, encoding="unic")
font6 = ImageFont.truetype("./fonts/Lobster-Regular.ttf", 29, encoding="unic")
font7 = ImageFont.truetype("./fonts/Viga-Regular.ttf", 23, encoding="unic")
font8 = ImageFont.truetype("./fonts/Viga-Regular.ttf", 31, encoding="unic")
font8 = ImageFont.truetype("./fonts/Century_Gothic_normal.ttf", 55, encoding="unic")
font9 = ImageFont.truetype("./fonts/Viga-Regular.ttf", 21, encoding="unic")

brand1_name.text((500,924), 'Day Wise Sales - MTD', (253,208,59), font=font2)
brand1_name.text((380,1407), 'Top 5 Brand by Achv', (253,208,59), font=font2)
brand1_name.text((1000,1437), 'Top 5 Brand \nContribution', (253,208,59), font=font2)

brand1_name.text((545,1897), 'All RSM Contribution', (253,208,59), font=font2)
brand1_name.text((237,2355), "Total Outstanding", (253,208,59), font=font2)
brand1_name.text((910,2355), "Aging Outstanding", (253,208,59), font=font2)

brand1_name.text((772,2730), "30 Days", (253,208,59), font=font9)
brand1_name.text((865,2730), "45 Days", (253,208,59), font=font9)
brand1_name.text((958,2730), "60 Days", (253,208,59), font=font9)
brand1_name.text((1051,2730), "90 Days", (253,208,59), font=font9)
brand1_name.text((1144,2730), "90+ Days", (253,208,59), font=font9)
brand1_name.text((10,2790), "If there is any inconvenience, You are requested to communicate with "
                            "our ERP BI Service:", (255,255,255), font=font9)
brand1_name.text((10,2820), "(Mobile: 01713389972, 01713380502)", (191,191,0), font=font9)


import datetime
mydate = datetime.datetime.now()
month_name=mydate.strftime("%B")
print(month_name)

brand1_name.text((1105, 924),month_name, (249,215,59), font=font2)

import numpy as np
import pandas as pd
import pyodbc as db

connection = db.connect('DRIVER={SQL Server};'
                        'SERVER=;'                     # Provide server
                        'DATABASE=;'                   # provide database 
                        'UID=;PWD=')                   # provide username and password

cursor = connection.cursor()
import set_name as employ_name
Employee_name=employ_name.name()
employee_search_name='%'+Employee_name+'%'

nsm_target_netsales_df = pd.read_sql_query("""declare @fromdate varchar(6)=CONVERT(varchar(6), dateAdd(day,0,getdate()-1), 112)
declare @yeardate varchar(4)=CONVERT(varchar(4), dateAdd(day,0,getdate()), 112)

select NSMNAME,EMPSHORTNAME, SUM(target) as Target, SUM(sales) as Sales, ISNULL(SUM(Outstanding),0) as Outstanding from
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


nsm_target = nsm_target_netsales_df['Target'].tolist()
nsm_netsales = nsm_target_netsales_df['Sales'].tolist()

print("NSM TARGET = ",nsm_target[0])
print("NSM NET SALES = ",nsm_netsales[0])

nsm_gross_sales_df = pd.read_sql_query("""declare @fromdate varchar(6)=CONVERT(varchar(6), dateAdd(day,0,getdate()-1), 112)
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
order by Sales DESC""", connection,params={employee_search_name})

nsm_grosssales = nsm_gross_sales_df['Sales'].tolist()
# print(str(round((nsm_grosssales[0]/10000000),1))+' Cr')
print("NSM GROSS SALES = ",nsm_grosssales[0])

achievement_of_nsm = str(round((nsm_grosssales[0]/nsm_target[0])*100,1))+' %'

print("Achievement = ",achievement_of_nsm)

from datetime import date, timedelta
from calendar import monthrange

today = date.today()
days_number = today.day
month_number = today.month
year_number = today.year
total_days=monthrange(year_number,month_number)[1]

# print(days_number)
# print(total_days)

trend = (nsm_grosssales[0]/days_number)*total_days

final_trend = str(round((trend/10000000),1))+" Cr"
print("Trend = ",final_trend)

trend_achievement = (nsm_grosssales[0]/trend)*100

final_trend_achievement=str(round(trend_achievement,1))+" %"
print("Trend Achievement= "+final_trend_achievement)


nsm_return_df = pd.read_sql_query("""declare @fromdate varchar(6)=CONVERT(varchar(6), dateAdd(day,0,getdate()-1), 112)
declare @yeardate varchar(4)=CONVERT(varchar(4), dateAdd(day,0,getdate()), 112)

select NSMNAME,EMPSHORTNAME, SUM(target) as Target, SUM(sales)*(-1) as Sales, ISNULL(SUM(Outstanding),0) as Outstanding from
(select  NSMID,NSMNAME,rsmtr,sum(Target) as target from RFieldForce
where yearmonth=@fromdate --and nsmname = 'Mr. Golam Haider' --and ccmsotr = 'ccd46'
group by NSMID,NSMNAME, rsmtr) as nsm
left join
(select case when left(msotr,2) = 'CC' then LEFT(MSOTR,3) else rsmtr end as rsmtr,
sum(extinvmisc) as sales from OESalesDetails
where LEFT(Transdate,6)=@fromdate
and TRANSTYPE<>1
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

nsm_return = nsm_return_df['Sales'].tolist()

print("NSM RETURN", nsm_return)

nsm_customer_coverage_df = pd.read_sql_query("""Select NSMNAME,count(full_customer) as customer from
(SELECT distinct CONCAT(IDCUST, ' ', AUDTORG) as full_customer,MSOTR
FROM CustomerInformation
where swactv=1) as a
left join
(select distinct msotr,NSMID,NSMNAME from rfieldforce
where yearmonth=CONVERT(varchar(6), dateAdd(day,0,getdate()), 112)) as b
on a.MSOTR = b.msotr
where NSMNAME like ?
group by NSMNAME""", connection,params={employee_search_name})

nsm_customer_coverage = nsm_customer_coverage_df['customer'].tolist()

print("NSM CUSTOMER COVERAGE = ",nsm_customer_coverage)

all_active_item_df = pd.read_sql_query("""select count(ITEMNO) as active from PRINFOSKF
where STATUS=1""", connection)

all_active_item = all_active_item_df['active'].tolist()

print("ACTIVE ITEM = ",all_active_item)

nsm_covered_item_df = pd.read_sql_query("""Select NSMNAME,count(distinct ITEM) as item from
(select ITEM,MSOTR from OESalesDetails) as a
left join
(select distinct msotr,NSMID,NSMNAME from rfieldforce
where yearmonth=CONVERT(varchar(6), dateAdd(day,0,getdate()), 112)) as b
on a.MSOTR = b.msotr
where NSMNAME like ?
group by NSMNAME""", connection,params={employee_search_name})

nsm_covered_item = nsm_covered_item_df['item'].tolist()

print("NSM COVERED ITEM = ",nsm_covered_item)
brand1_name.text((40,420), str(round((nsm_target[0]/10000000),1))+' Cr', (255,255,255), font=font8)
brand1_name.text((463,420), str(round((nsm_grosssales[0]/10000000),2))+' Cr', (255,255,255), font=font8)
brand1_name.text((880,420), str(round((nsm_netsales[0]/10000000),2))+' Cr', (255,255,255), font=font8)

brand1_name.text((38,600), str(round((nsm_return[0]/nsm_grosssales[0])*100,1))+' %', (255,255,255), font=font8)
brand1_name.text((463,600), achievement_of_nsm, (255,255,255), font=font8)
brand1_name.text((880,600), final_trend, (255,255,255), font=font8)

brand1_name.text((38,780), str(round(nsm_customer_coverage[0]/1000,1))+" K", (255,255,255), font=font8)
brand1_name.text((463,780), str(round((nsm_covered_item[0]/all_active_item[0])*100,1))+" %", (255,255,255), font=font8)
brand1_name.text((880,780), final_trend_achievement, (255,255,255), font=font8)


img.save('./images/final_photo.png')
print('name and information are merged with the picture.')