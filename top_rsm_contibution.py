import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pyodbc as db
from matplotlib.patches import Patch
from PIL import Image, ImageDraw, ImageFont
import sys

def crore(number):
    number = number / 10000000
    number = round(number,1)
    number = format(number, ',')
    number = number + ' Cr'
    return number

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

top6_customer_df = pd.read_sql_query("""declare @fromdate varchar(6)=CONVERT(varchar(6), dateAdd(day,0,getdate()), 112)
declare @yeardate varchar(4)=CONVERT(varchar(4), dateAdd(day,0,getdate()), 112)

select NSMNAME,EMPSHORTNAME,rsmname, SUM(target) as Target, SUM(sales) as Sales, ISNULL(SUM(Outstanding),0) as Outstanding from
(select  NSMID,NSMNAME,rsmname,rsmtr,sum(Target) as target from RFieldForce
where yearmonth=@fromdate and nsmname like ? --and ccmsotr = 'ccd46'
group by NSMID,NSMNAME, rsmtr,rsmname) as nsm
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
and short.EMPSHORTNAME is not null
group by NSMNAME,EMPSHORTNAME,rsmname
order by Sales DESC
""", connection,params={employee_search_name})

customer_name = top6_customer_df['rsmname'].values.tolist()
target_values = top6_customer_df['Target'].values.tolist()
bought_values = top6_customer_df['Sales'].values.tolist()
outstanding = top6_customer_df['Outstanding'].values.tolist()
print(customer_name)
print(target_values)
print(bought_values)
print(outstanding)

def Md_Replace(customer_name):
    md_replaced_result = [sub.replace('Md.', '') for sub in customer_name]
    return md_replaced_result

def Mr_Replace(customer_name):
    md_replaced_result = [sub.replace('Mr.', '') for sub in customer_name]
    return md_replaced_result

def Muhammad_Replace(customer_name):
    md_replaced_result = [sub.replace('Muhammad', '') for sub in customer_name]
    return md_replaced_result

new_name = Md_Replace(customer_name)
new_name2 = Mr_Replace(new_name)
new_name3 = Muhammad_Replace(new_name2)
print(new_name3)

length = len(new_name3)
print(length)
# total_amount=sum(bought_values)
# print(total_amount)
# percent_array=[]
#
# for x in bought_values:
#     percen=(x/total_amount)*100;
#     percent_array.append(percen)
# print(percent_array)
# sys.exit()

img = Image.open("./images//top9_rsm_v2.png")


top_customer1_sale = ImageDraw.Draw(img)
top_customer2_sale = ImageDraw.Draw(img)
top_customer3_sale = ImageDraw.Draw(img)
top_customer4_sale = ImageDraw.Draw(img)
top_customer5_sale = ImageDraw.Draw(img)
top_customer6_sale = ImageDraw.Draw(img)
top_customer7_sale = ImageDraw.Draw(img)
top_customer8_sale = ImageDraw.Draw(img)
top_customer9_sale = ImageDraw.Draw(img)

top_customer1_percentage = ImageDraw.Draw(img)
top_customer2_percentage = ImageDraw.Draw(img)
top_customer3_percentage = ImageDraw.Draw(img)
top_customer4_percentage = ImageDraw.Draw(img)
top_customer5_percentage = ImageDraw.Draw(img)
top_customer6_percentage = ImageDraw.Draw(img)
top_customer7_percentage = ImageDraw.Draw(img)
top_customer8_percentage = ImageDraw.Draw(img)
top_customer9_percentage = ImageDraw.Draw(img)

top_customer1_name = ImageDraw.Draw(img)
top_customer2_name = ImageDraw.Draw(img)
top_customer3_name = ImageDraw.Draw(img)
top_customer4_name = ImageDraw.Draw(img)
top_customer5_name = ImageDraw.Draw(img)
top_customer6_name = ImageDraw.Draw(img)
top_customer7_name = ImageDraw.Draw(img)
top_customer8_name = ImageDraw.Draw(img)
top_customer9_name = ImageDraw.Draw(img)

below_title5 = ImageDraw.Draw(img)

font = ImageFont.truetype("./fonts/Stencil_Regular.ttf", 10, encoding="unic")
font1 = ImageFont.truetype("./fonts/ROCK.ttf", 11, encoding="unic")
font2 = ImageFont.truetype("./fonts/ROCK.ttf", 13, encoding="unic")
font4 = ImageFont.truetype("./fonts/Bitstream_Vera_Sans_Roman.ttf", 12, encoding="unic")
font5 = ImageFont.truetype("./fonts/bitstream-vera-sans.bold.ttf", 18, encoding="unic")
font6 = ImageFont.truetype("./fonts/bitstream-vera-sans.bold.ttf", 20, encoding="unic")
font7 = ImageFont.truetype("./fonts/bitstream-vera-sans.bold.ttf", 21, encoding="unic")


if length>=6:
    #--------------------------------------------------------------------------------------

    top_customer1_name.text((160, 200), new_name3[0], (238, 57, 102), font=font5)
    top_customer1_name.text((160, 201), new_name3[0], (238, 57, 102), font=font5)

    top_customer2_name.text((345, 200), new_name3[1], (119, 72, 196), font=font5)
    top_customer2_name.text((345, 201), new_name3[1], (119, 72, 196), font=font5)

    top_customer3_name.text((520, 200), new_name3[2], (3,145,155), font=font5)
    top_customer3_name.text((520, 201), new_name3[2], (3,145,155), font=font5)
    #
    top_customer4_name.text((693, 200), new_name3[3], (231,115,6), font=font5)
    top_customer4_name.text((693, 201), new_name3[3], (231,115,6), font=font5)
    #
    top_customer5_name.text((860, 200), new_name3[4], (21,132,93), font=font5)
    top_customer5_name.text((860, 201), new_name3[4], (21,132,93), font=font5)
    #
    top_customer6_name.text((1015, 200), new_name3[5], (222,153,17), font=font5)
    top_customer6_name.text((1015, 201), new_name3[5], (222,153,17), font=font5)


    #-------------------------------sales------------------------------------------------

    top_customer1_name.text((210, 280),crore(bought_values[0]), (255,255,255), font=font6)
    # top_customer1_name.text((30, 259),'A: '+ crore(bought_values[0]), (0,0,0), font=font5)

    top_customer2_name.text((383, 280),crore(bought_values[1]), (255,255,255), font=font6)
    # top_customer2_name.text((162, 259),'A: '+ crore(bought_values[1]), (0,0,0), font=font5)

    top_customer3_name.text((556, 280),crore(bought_values[2]), (255,255,255), font=font6)
    # top_customer3_name.text((298, 259),'A: '+ crore(bought_values[2]), (0,0,0), font=font5)
    #
    top_customer4_name.text((729, 280),crore(bought_values[3]), (255,255,255), font=font6)
    # top_customer4_name.text((445, 259),'A: '+ crore(bought_values[3]), (0,0,0), font=font5)
    #
    top_customer5_name.text((902, 280),crore(bought_values[4]), (255,255,255), font=font6)
    # top_customer5_name.text((581, 259),'A: '+ crore(bought_values[4]), (0,0,0), font=font5)

    top_customer6_name.text((1075, 280),crore(bought_values[5]), (255,255,255), font=font6)
    # top_customer6_name.text((723, 259),'A: '+ crore(bought_values[5]), (0,0,0), font=font5)

    #---------------------------------target----------------------------------------------

    top_customer1_name.text((210, 247),crore(target_values[0]), (255,255,255), font=font6)
    # top_customer1_name.text((30, 239),'T: '+ crore(target_values[0]), (0,0,0), font=font5)

    top_customer2_name.text((383, 247),crore(target_values[1]), (255,255,255), font=font6)
    # top_customer2_name.text((162, 239), 'T: '+ crore(target_values[1]), (0,0,0), font=font5)

    top_customer3_name.text((556, 247),crore(target_values[2]), (255,255,255), font=font6)
    # top_customer3_name.text((298, 239), 'T: '+ crore(target_values[2]), (0,0,0), font=font5)
    #
    top_customer4_name.text((729, 247),crore(target_values[3]), (255,255,255), font=font6)
    # top_customer4_name.text((445, 239), 'T: '+ crore(target_values[3]), (0,0,0), font=font5)
    #
    top_customer5_name.text((902, 247),crore(target_values[4]), (255,255,255), font=font6)
    # top_customer5_name.text((581, 239), 'T: '+ crore(target_values[4]), (0,0,0), font=font5)
    #
    top_customer6_name.text((1075, 247),crore(target_values[5]), (255,255,255), font=font6)
    # top_customer6_name.text((723, 239), 'T: '+ crore(target_values[5]), (0,0,0), font=font5)

    #---------------------------------------outstanding----------------------------------------

    top_customer1_name.text((210, 346),crore(outstanding[0]), (255,255,255), font=font6)
    # top_customer1_name.text((30, 279),'O: '+ crore(outstanding[0]), (0,0,0), font=font5)

    top_customer2_name.text((383, 346),crore(outstanding[1]), (255,255,255), font=font6)
    # top_customer2_name.text((162, 279), 'O: '+ crore(outstanding[1]), (0,0,0), font=font5)

    top_customer3_name.text((556, 346),crore(outstanding[2]), (255,255,255), font=font6)
    # top_customer3_name.text((298, 279), 'O: '+ crore(outstanding[2]), (0,0,0), font=font5)
    #
    top_customer4_name.text((729, 346),crore(outstanding[3]), (255,255,255), font=font6)
    # top_customer4_name.text((445, 279), 'O: '+ crore(outstanding[3]), (0,0,0), font=font5)
    #
    top_customer5_name.text((902, 346),crore(outstanding[4]), (255,255,255), font=font6)
    # top_customer5_name.text((581, 279), 'O: '+ crore(outstanding[4]), (0,0,0), font=font5)
    #
    top_customer6_name.text((1075, 346),crore(outstanding[5]), (255,255,255), font=font6)
    # top_customer6_name.text((723, 279), 'O: '+ crore(outstanding[5]), (0,0,0), font=font5)

    #---------------------------------achievement----------------------------------------------

    top_customer1_name.text((210, 313),str(round((bought_values[0]/target_values[0])*100,1))+" %", (0,96,252), font=font6)
    # top_customer1_name.text((30, 299),'Ac: '+ str(round((bought_values[0]/target_values[0])*100,1))+" %", (0,0,0), font=font5)

    top_customer2_name.text((383, 313),str(round((bought_values[1]/target_values[1])*100,1))+" %", (0,96,252), font=font6)
    # top_customer2_name.text((162, 299), 'Ac: '+ str(round((bought_values[1]/target_values[1])*100,1))+" %", (0,0,0), font=font5)

    top_customer3_name.text((556, 313),str(round((bought_values[2]/target_values[2])*100,1))+" %", (0,96,252), font=font6)
    # top_customer3_name.text((298, 299), 'Ac: '+ str(round((bought_values[2]/target_values[2])*100,1))+" %", (0,0,0), font=font5)
    #
    top_customer4_name.text((729, 313),str(round((bought_values[3]/target_values[3])*100,1))+" %", (0,96,252), font=font6)
    # top_customer4_name.text((445, 299), 'Ac: '+ str(round((bought_values[3]/target_values[3])*100,1))+" %", (0,0,0), font=font5)
    #
    top_customer5_name.text((902, 313),str(round((bought_values[4]/target_values[4])*100,1))+" %", (0,96,252), font=font6)
    # top_customer5_name.text((581, 299), 'Ac: '+ str(round((bought_values[4]/target_values[4])*100,1))+" %", (0,0,0), font=font5)
    #
    top_customer6_name.text((1075, 313),str(round((bought_values[5]/target_values[5])*100,1))+" %", (0,96,252), font=font6)
    # top_customer6_name.text((723, 299), 'Ac: '+ str(round((bought_values[5]/target_values[5])*100,1))+" %", (0,0,0), font=font5)

    img.save('./images/top9_customer_info.png')

if length==5:
    #--------------------------------------------------------------------------------------

    top_customer1_name.text((160, 200), new_name3[0], (238, 57, 102), font=font5)
    top_customer1_name.text((160, 201), new_name3[0], (238, 57, 102), font=font5)

    top_customer2_name.text((345, 200), new_name3[1], (119, 72, 196), font=font5)
    top_customer2_name.text((345, 201), new_name3[1], (119, 72, 196), font=font5)

    top_customer3_name.text((520, 200), new_name3[2], (3,145,155), font=font5)
    top_customer3_name.text((520, 201), new_name3[2], (3,145,155), font=font5)
    #
    top_customer4_name.text((693, 200), new_name3[3], (231,115,6), font=font5)
    top_customer4_name.text((693, 201), new_name3[3], (231,115,6), font=font5)
    #
    top_customer5_name.text((860, 200), new_name3[4], (21,132,93), font=font5)
    top_customer5_name.text((860, 201), new_name3[4], (21,132,93), font=font5)


    #-------------------------------sales------------------------------------------------

    top_customer1_name.text((210, 280),crore(bought_values[0]), (255,255,255), font=font6)
    # top_customer1_name.text((30, 259),'A: '+ crore(bought_values[0]), (0,0,0), font=font5)

    top_customer2_name.text((383, 280),crore(bought_values[1]), (255,255,255), font=font6)
    # top_customer2_name.text((162, 259),'A: '+ crore(bought_values[1]), (0,0,0), font=font5)

    top_customer3_name.text((556, 280),crore(bought_values[2]), (255,255,255), font=font6)
    # top_customer3_name.text((298, 259),'A: '+ crore(bought_values[2]), (0,0,0), font=font5)
    #
    top_customer4_name.text((729, 280),crore(bought_values[3]), (255,255,255), font=font6)
    # top_customer4_name.text((445, 259),'A: '+ crore(bought_values[3]), (0,0,0), font=font5)
    #
    top_customer5_name.text((902, 280),crore(bought_values[4]), (255,255,255), font=font6)
    # top_customer5_name.text((581, 259),'A: '+ crore(bought_values[4]), (0,0,0), font=font5)

    #---------------------------------target----------------------------------------------

    top_customer1_name.text((210, 247),crore(target_values[0]), (255,255,255), font=font6)
    # top_customer1_name.text((30, 239),'T: '+ crore(target_values[0]), (0,0,0), font=font5)

    top_customer2_name.text((383, 247),crore(target_values[1]), (255,255,255), font=font6)
    # top_customer2_name.text((162, 239), 'T: '+ crore(target_values[1]), (0,0,0), font=font5)

    top_customer3_name.text((556, 247),crore(target_values[2]), (255,255,255), font=font6)
    # top_customer3_name.text((298, 239), 'T: '+ crore(target_values[2]), (0,0,0), font=font5)
    #
    top_customer4_name.text((729, 247),crore(target_values[3]), (255,255,255), font=font6)
    # top_customer4_name.text((445, 239), 'T: '+ crore(target_values[3]), (0,0,0), font=font5)
    #
    top_customer5_name.text((902, 247),crore(target_values[4]), (255,255,255), font=font6)
    # top_customer5_name.text((581, 239), 'T: '+ crore(target_values[4]), (0,0,0), font=font5)

    #---------------------------------------outstanding----------------------------------------

    top_customer1_name.text((210, 346),crore(outstanding[0]), (255,255,255), font=font6)
    # top_customer1_name.text((30, 279),'O: '+ crore(outstanding[0]), (0,0,0), font=font5)

    top_customer2_name.text((383, 346),crore(outstanding[1]), (255,255,255), font=font6)
    # top_customer2_name.text((162, 279), 'O: '+ crore(outstanding[1]), (0,0,0), font=font5)

    top_customer3_name.text((556, 346),crore(outstanding[2]), (255,255,255), font=font6)
    # top_customer3_name.text((298, 279), 'O: '+ crore(outstanding[2]), (0,0,0), font=font5)
    #
    top_customer4_name.text((729, 346),crore(outstanding[3]), (255,255,255), font=font6)
    # top_customer4_name.text((445, 279), 'O: '+ crore(outstanding[3]), (0,0,0), font=font5)
    #
    top_customer5_name.text((902, 346),crore(outstanding[4]), (255,255,255), font=font6)
    # top_customer5_name.text((581, 279), 'O: '+ crore(outstanding[4]), (0,0,0), font=font5)

    #---------------------------------achievement----------------------------------------------

    top_customer1_name.text((210, 313),str(round((bought_values[0]/target_values[0])*100,1))+" %", (0,96,252), font=font6)
    # top_customer1_name.text((30, 299),'Ac: '+ str(round((bought_values[0]/target_values[0])*100,1))+" %", (0,0,0), font=font5)

    top_customer2_name.text((383, 313),str(round((bought_values[1]/target_values[1])*100,1))+" %", (0,96,252), font=font6)
    # top_customer2_name.text((162, 299), 'Ac: '+ str(round((bought_values[1]/target_values[1])*100,1))+" %", (0,0,0), font=font5)

    top_customer3_name.text((556, 313),str(round((bought_values[2]/target_values[2])*100,1))+" %", (0,96,252), font=font6)
    # top_customer3_name.text((298, 299), 'Ac: '+ str(round((bought_values[2]/target_values[2])*100,1))+" %", (0,0,0), font=font5)
    #
    top_customer4_name.text((729, 313),str(round((bought_values[3]/target_values[3])*100,1))+" %", (0,96,252), font=font6)
    # top_customer4_name.text((445, 299), 'Ac: '+ str(round((bought_values[3]/target_values[3])*100,1))+" %", (0,0,0), font=font5)
    #
    top_customer5_name.text((902, 313),str(round((bought_values[4]/target_values[4])*100,1))+" %", (0,96,252), font=font6)
    # top_customer5_name.text((581, 299), 'Ac: '+ str(round((bought_values[4]/target_values[4])*100,1))+" %", (0,0,0), font=font5)

    img.save('./images/top9_customer_info.png')

if length==4:
    #--------------------------------------------------------------------------------------

    top_customer1_name.text((160, 200), new_name3[0], (238, 57, 102), font=font5)
    top_customer1_name.text((160, 201), new_name3[0], (238, 57, 102), font=font5)

    top_customer2_name.text((345, 200), new_name3[1], (119, 72, 196), font=font5)
    top_customer2_name.text((345, 201), new_name3[1], (119, 72, 196), font=font5)

    top_customer3_name.text((520, 200), new_name3[2], (3,145,155), font=font5)
    top_customer3_name.text((520, 201), new_name3[2], (3,145,155), font=font5)
    #
    top_customer4_name.text((693, 200), new_name3[3], (231,115,6), font=font5)
    top_customer4_name.text((693, 201), new_name3[3], (231,115,6), font=font5)


    #-------------------------------sales------------------------------------------------

    top_customer1_name.text((210, 280),crore(bought_values[0]), (255,255,255), font=font6)
    # top_customer1_name.text((30, 259),'A: '+ crore(bought_values[0]), (0,0,0), font=font5)

    top_customer2_name.text((383, 280),crore(bought_values[1]), (255,255,255), font=font6)
    # top_customer2_name.text((162, 259),'A: '+ crore(bought_values[1]), (0,0,0), font=font5)

    top_customer3_name.text((556, 280),crore(bought_values[2]), (255,255,255), font=font6)
    # top_customer3_name.text((298, 259),'A: '+ crore(bought_values[2]), (0,0,0), font=font5)
    #
    top_customer4_name.text((729, 280),crore(bought_values[3]), (255,255,255), font=font6)
    # top_customer4_name.text((445, 259),'A: '+ crore(bought_values[3]), (0,0,0), font=font5)

    #---------------------------------target----------------------------------------------

    top_customer1_name.text((210, 247),crore(target_values[0]), (255,255,255), font=font6)
    # top_customer1_name.text((30, 239),'T: '+ crore(target_values[0]), (0,0,0), font=font5)

    top_customer2_name.text((383, 247),crore(target_values[1]), (255,255,255), font=font6)
    # top_customer2_name.text((162, 239), 'T: '+ crore(target_values[1]), (0,0,0), font=font5)

    top_customer3_name.text((556, 247),crore(target_values[2]), (255,255,255), font=font6)
    # top_customer3_name.text((298, 239), 'T: '+ crore(target_values[2]), (0,0,0), font=font5)
    #
    top_customer4_name.text((729, 247),crore(target_values[3]), (255,255,255), font=font6)
    # top_customer4_name.text((445, 239), 'T: '+ crore(target_values[3]), (0,0,0), font=font5)

    #---------------------------------------outstanding----------------------------------------

    top_customer1_name.text((210, 346),crore(outstanding[0]), (255,255,255), font=font6)
    # top_customer1_name.text((30, 279),'O: '+ crore(outstanding[0]), (0,0,0), font=font5)

    top_customer2_name.text((383, 346),crore(outstanding[1]), (255,255,255), font=font6)
    # top_customer2_name.text((162, 279), 'O: '+ crore(outstanding[1]), (0,0,0), font=font5)

    top_customer3_name.text((556, 346),crore(outstanding[2]), (255,255,255), font=font6)
    # top_customer3_name.text((298, 279), 'O: '+ crore(outstanding[2]), (0,0,0), font=font5)
    #
    top_customer4_name.text((729, 346),crore(outstanding[3]), (255,255,255), font=font6)
    # top_customer4_name.text((445, 279), 'O: '+ crore(outstanding[3]), (0,0,0), font=font5)

    #---------------------------------achievement----------------------------------------------

    top_customer1_name.text((210, 313),str(round((bought_values[0]/target_values[0])*100,1))+" %", (0,96,252), font=font6)
    # top_customer1_name.text((30, 299),'Ac: '+ str(round((bought_values[0]/target_values[0])*100,1))+" %", (0,0,0), font=font5)

    top_customer2_name.text((383, 313),str(round((bought_values[1]/target_values[1])*100,1))+" %", (0,96,252), font=font6)
    # top_customer2_name.text((162, 299), 'Ac: '+ str(round((bought_values[1]/target_values[1])*100,1))+" %", (0,0,0), font=font5)

    top_customer3_name.text((556, 313),str(round((bought_values[2]/target_values[2])*100,1))+" %", (0,96,252), font=font6)
    # top_customer3_name.text((298, 299), 'Ac: '+ str(round((bought_values[2]/target_values[2])*100,1))+" %", (0,0,0), font=font5)
    #
    top_customer4_name.text((729, 313),str(round((bought_values[3]/target_values[3])*100,1))+" %", (0,96,252), font=font6)
    # top_customer4_name.text((445, 299), 'Ac: '+ str(round((bought_values[3]/target_values[3])*100,1))+" %", (0,0,0), font=font5)


    img.save('./images/top9_customer_info.png')

print('15. Top 6 valuable customer with values generated')