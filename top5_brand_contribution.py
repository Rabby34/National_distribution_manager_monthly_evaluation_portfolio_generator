import matplotlib.pyplot as plt
import pandas as pd
import pyodbc as db
from matplotlib.patches import Patch
from PIL import Image, ImageDraw, ImageFont
import sys
from PIL import Image, ImageDraw, ImageFont

def convert(number):
    number = number / 1000
    number = int(number)
    number = format(number, ',')
    number = number + 'K'
    return number

import set_name as employ_name
Employee_name=employ_name.name()
employee_search_name='%'+Employee_name+'%'

connection = db.connect('DRIVER={SQL Server};'
                        'SERVER=;'                     # Provide server
                        'DATABASE=;'                   # provide database 
                        'UID=;PWD=')                   # provide username and password

cursor = connection.cursor()

total_sales_df = pd.read_sql_query("""Declare @Currentmonth NVARCHAR(MAX);
SET @Currentmonth = convert(varchar(6), GETDATE(),112);
select Sum(EXTINVMISC) as  MTDSales from OESalesDetails
where LEFT(TRANSDATE,6) = @Currentmonth
and transtype=1""", connection)

active_sales = total_sales_df['MTDSales'].values.tolist()

sales_act=active_sales[0]

print(sales_act)

top_sales_df = pd.read_sql_query("""select top 5 isnull(b.NSMNAME,a.nsmname),a.brand as brand,target,sale,(sale/target)*100 as achv from
(select nsmname,brand,sum(Value) as Target from
(select * from [ARCSECONDARY].[dbo].[RfieldForceProductTRG] where yearmonth=convert(varchar(6), GETDATE(),112) 
and nsmname like ?) as BTarget
left join
(select * from prinfoskf) as Item
on BTarget.ITEMNO=item.itemno
group by nsmname,brand) as a
left join
(
select nsmname,brand,sum(extinvmisc) as sale from
(select ITEM,msotr,msogrp,extinvmisc,left(transdate,6) as Yearmonth from oesalesdetails where left(transdate,6)=convert(varchar(6), GETDATE(),112) and transtype=1) as sale
left join
(select * from RFieldForce) as FF
on sale.msotr=ff.msotr
and sale.msogrp=ff.msogroup
and sale.yearmonth=ff.yearmonth
left join
(select * from prinfoskf) as Item
on item.itemno=sale.item
where nsmname like ?
group by nsmname,brand) as b
on a.brand=b.brand
where target<>0
order by achv desc""", connection,params=(employee_search_name,employee_search_name))

top_sale = top_sales_df['sale'].values.tolist()

sales_top=sum(top_sale)

print(sales_top)


percentage_value = round((sales_top/sales_act)*100,1)

# percentage_value = 32.2

print(percentage_value)

img = Image.open("./images/top5_brand_contribution.png")
print_value = str(percentage_value) + "%"

brand1_name = ImageDraw.Draw(img)

font = ImageFont.truetype("./fonts/Stencil_Regular.ttf", 10, encoding="unic")
font1 = ImageFont.truetype("./fonts/ROCK.ttf", 11, encoding="unic")
font2 = ImageFont.truetype("./fonts/ROCK.ttf", 13, encoding="unic")
font4 = ImageFont.truetype("./fonts/Bitstream_Vera_Sans_Roman.ttf", 12, encoding="unic")
font5 = ImageFont.truetype("./fonts/bitstream-vera-sans.bold.ttf", 12, encoding="unic")
font6 = ImageFont.truetype("./fonts/bitstream-vera-sans.bold.ttf", 20, encoding="unic")
font7 = ImageFont.truetype("./fonts/bitstream-vera-sans.bold.ttf", 30, encoding="unic")

brand1_name.text((138, 210), print_value, (255,255,255), font=font7)

# brand1_name.text((80, 10), "Top 5 Brand", (7,21,21), font=font7)
# brand1_name.text((90, 40), "Contribution", (7,21,21), font=font6)

# below_title5.text((175, 26), "Top 5 Brand Return", (0,0,0), font=font7)

# box.text((30, 320), '''If there is any inconvenience,\nyou are requested to communicate with the ERP BI Service:\n(Mobile: 01713-389972, 01713-380499)'''
#          ,(164,78,24), font=font5)

img.save('./images/contribution_pic.png')


