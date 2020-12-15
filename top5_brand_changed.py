import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pyodbc as db
from matplotlib.patches import Patch
from PIL import Image, ImageDraw, ImageFont
import sys

import math

millnames = ['',' K',' M',' B',' T']

def millify(n):
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])

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

top5_brand_df = pd.read_sql_query("""select top 5 isnull(b.NSMNAME,a.nsmname),a.brand as brand,target,sale,(sale/target)*100 as achv from
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
order by achv desc

""", connection,params=(employee_search_name,employee_search_name))

Brand_name = top5_brand_df['brand'].values.tolist()
sale_values = top5_brand_df['sale'].values.tolist()
target_values = top5_brand_df['target'].values.tolist()
achv_values = top5_brand_df['achv'].values.tolist()

img = Image.open("./images/top5_brand.png")
top_brand1_sale = ImageDraw.Draw(img)
top_brand2_sale = ImageDraw.Draw(img)
top_brand3_sale = ImageDraw.Draw(img)
top_brand4_sale = ImageDraw.Draw(img)
top_brand5_sale = ImageDraw.Draw(img)

top_brand1_name = ImageDraw.Draw(img)
top_brand2_name = ImageDraw.Draw(img)
top_brand3_name = ImageDraw.Draw(img)
top_brand4_name = ImageDraw.Draw(img)
top_brand5_name = ImageDraw.Draw(img)

below_title5 = ImageDraw.Draw(img)

font = ImageFont.truetype("./fonts/Stencil_Regular.ttf", 10, encoding="unic")
font1 = ImageFont.truetype("./fonts/ROCK.ttf", 11, encoding="unic")
font2 = ImageFont.truetype("./fonts/ROCK.ttf", 13, encoding="unic")
font4 = ImageFont.truetype("./fonts/Bitstream_Vera_Sans_Roman.ttf", 12, encoding="unic")
font5 = ImageFont.truetype("./fonts/bitstream-vera-sans.bold.ttf", 16, encoding="unic")
font6 = ImageFont.truetype("./fonts/bitstream-vera-sans.bold.ttf", 17, encoding="unic")
font7 = ImageFont.truetype("./fonts/bitstream-vera-sans.bold.ttf", 25, encoding="unic")
font8 = ImageFont.truetype("./fonts/bitstream-vera-sans.bold.ttf", 18, encoding="unic")


#-----------------------------------target-----------------------------------------------------
top_brand1_sale.text((193, 338), str(round(target_values[0]/1000,1))+" K", (255,255,255), font=font8)
# top_brand1_sale.text((78, 291), str(round(target_values[0]/1000,1))+" K", (0,0,0), font=font5)

top_brand2_sale.text((334, 338), str(round(target_values[1]/1000,1))+" K", (255,255,255), font=font8)
# top_brand2_sale.text((234, 291), str(round(target_values[1]/1000,1))+" K", (0,0,0), font=font5)

top_brand3_sale.text((485, 338), str(round(target_values[2]/1000,1))+" K", (255,255,255), font=font8)
# top_brand3_sale.text((388, 291), str(round(target_values[2]/1000,1))+" K", (0,0,0), font=font5)

top_brand4_sale.text((621, 338), str(round(target_values[3]/1000,1))+" K", (255,255,255), font=font8)
# top_brand4_sale.text((539, 291), str(round(target_values[3]/1000,1))+" K", (0,0,0), font=font5)

top_brand5_sale.text((757, 338), str(round(target_values[4]/1000,1))+" K", (255,255,255), font=font8)
# top_brand5_sale.text((694, 291), str(round(target_values[4]/1000,1))+" K", (0,0,0), font=font5)

#-----------------------------------------------sales-----------------------------------------------------------
top_brand1_sale.text((193, 376), str(round(sale_values[0]/1000,1))+" K", (255,255,255), font=font8)
# top_brand1_sale.text((78, 191), str(round(achv_values[0],1))+" K", (0,0,0), font=font5)

top_brand2_sale.text((334, 376),str(round(sale_values[1]/1000,1))+" K", (255,255,255), font=font8)
# top_brand2_sale.text((234, 191), str(round(achv_values[1],1))+" %", (0,0,0), font=font5)

top_brand3_sale.text((485, 376), str(round(sale_values[2]/1000,1))+" K", (255,255,255), font=font8)
# top_brand3_sale.text((388, 191), str(round(achv_values[2],1))+" %", (0,0,0), font=font5)

top_brand4_sale.text((621, 376), str(round(sale_values[3]/1000,1))+" K", (255,255,255), font=font8)
# top_brand4_sale.text((539, 191), str(round(achv_values[3],1))+" %", (0,0,0), font=font5)

top_brand5_sale.text((757, 376), str(round(sale_values[4]/1000,1))+" K", (255,255,255), font=font8)
# top_brand5_sale.text((694, 191), str(round(achv_values[4],1))+" %", (0,0,0), font=font5)
#--------------------------------------------------------------------------------------------------------

top_brand1_sale.text((189, 178), str(round(achv_values[0],1))+" %", (0,0,0), font=font8)
# top_brand1_sale.text((78, 191), str(round(achv_values[0],1))+" %", (0,0,0), font=font5)

top_brand2_sale.text((332, 178), str(round(achv_values[1],1))+" %", (0,0,0), font=font8)
# top_brand2_sale.text((234, 191), str(round(achv_values[1],1))+" %", (0,0,0), font=font5)

top_brand3_sale.text((478, 178), str(round(achv_values[2],1))+" %", (0,0,0), font=font8)
# top_brand3_sale.text((388, 191), str(round(achv_values[2],1))+" %", (0,0,0), font=font5)

top_brand4_sale.text((621, 178), str(round(achv_values[3],1))+" %", (0,0,0), font=font8)
# top_brand4_sale.text((539, 191), str(round(achv_values[3],1))+" %", (0,0,0), font=font5)

top_brand5_sale.text((767, 178), str(round(achv_values[4],1))+" %", (0,0,0), font=font8)
# top_brand5_sale.text((694, 191), str(round(achv_values[4],1))+" %", (0,0,0), font=font5)

top_brand1_name.text((193, 275), Brand_name[0], (252,208,59), font=font8)
top_brand1_name.text((193, 276), Brand_name[0], (252,208,59), font=font8)

top_brand2_name.text((334, 275), Brand_name[1], (252,208,59), font=font8)#289, 235
top_brand2_name.text((334, 276), Brand_name[1], (252,208,59), font=font8)

top_brand3_name.text((485, 275), Brand_name[2], (252,208,59), font=font8)
top_brand3_name.text((485, 276), Brand_name[2], (252,208,59), font=font8)

top_brand4_name.text((632, 275), Brand_name[3], (252,208,59), font=font8)
top_brand4_name.text((632, 276), Brand_name[3], (252,208,59), font=font8)

top_brand5_name.text((757, 275), Brand_name[4], (252,208,59), font=font8)
top_brand5_name.text((757, 276), Brand_name[4], (252,208,59), font=font8)

# below_title5.text((320, 5), "Top 5 Brand by Achv.", (252,208,59), font=font7)
#below_title5.text((280, 31), "Top 5 Brand Sales", (7,24,24), font=font7)

img.save('./images/changed_top5_brand_info.png')

print('10. Top 5 branch sales with values generated')