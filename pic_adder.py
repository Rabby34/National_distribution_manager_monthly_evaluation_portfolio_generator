import set_name
import Title_with_picture
import achievement_circle_generator
import day_wise_sales_cumulative
import top5_brand_changed
import top5_brand_contribution
import top_rsm_contibution
import outstanding
import aging_days

from PIL import Image, ImageDraw, ImageFont, ImageFilter

back = Image.open("./images/titles_marged.png")
# pro_pic = Image.open("./images/bashir.png")
achievement_hour_per = Image.open("./images/achievement_hour.png")
down_arrow = Image.open("./images/down_arrow.png")
up_arrow = Image.open("./images/up_arrow.png")
# yearly_contribution_donut=Image.open("./images/yearly_contribution.png")
# monthly_contribution_donut=Image.open("./images/monthly_contribution.png")
target = Image.open("./images/7th_kpi.png")
gross_sales = Image.open("./images/9th_kpi.png")
net_sales = Image.open("./images/1st_kpi.png")

market_return = Image.open("./images/2nd_kpi.png")
achievement = Image.open("./images/6th_kpi.png")
trend = Image.open("./images/3rd_kpi.png")

customer_coverage = Image.open("./images/4th_kpi.png")
item_coverage = Image.open("./images/5th_kpi.png")
trend_achievement = Image.open("./images/8th_kpi.png")

day_wise_sale = Image.open("./images/Cumulative_Day_Wise_Target_vs_Sales.png")
top5_brand = Image.open("./images/changed_top5_brand_info.png")
top5_brand_contribution = Image.open("./images/contribution_pic.png")
top9_rsm = Image.open("./images/top9_customer_info.png")
outstanding_pie = Image.open("./images/outstanding_donut.png")
aging_day = Image.open("./images/aging_outstanding.png")

import pandas as pd
import pyodbc as db

imageSize = Image.new('RGB', (1270,2870))#1270,2290#1270,2790
imageSize.paste(back, (0, 0))
# imageSize.paste(pro_pic, (45, 59))
imageSize.paste(achievement_hour_per, (825, 66))
imageSize.paste(target, (10, 357))
imageSize.paste(gross_sales, (432, 357))
imageSize.paste(net_sales, (853, 357))

imageSize.paste(market_return, (10, 537))
imageSize.paste(achievement, (432, 537))
imageSize.paste(trend, (853, 537))

imageSize.paste(customer_coverage, (10, 717))
imageSize.paste(item_coverage, (432, 717))
imageSize.paste(trend_achievement, (853, 717))

imageSize.paste(day_wise_sale, (10, 985))

imageSize.paste(top5_brand, (10, 1420))
imageSize.paste(top5_brand_contribution, (900, 1420))

imageSize.paste(top9_rsm, (25, 1890))
imageSize.paste(outstanding_pie, (-50, 2390))
imageSize.paste(aging_day, (760, 2430))
# imageSize.paste(yearly_contribution_donut, (35, 594))
# imageSize.paste(monthly_contribution_donut, (450, 594))


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
# achievement=94.1

if(achievement<=100):
    imageSize.paste(down_arrow, (1025, 140))
elif(achievement>100):
    imageSize.paste(up_arrow, (1025, 140))

imageSize.save("./images/marge_all.png")

print("all are merged together.")

import add_final_text