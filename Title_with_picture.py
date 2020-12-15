from PIL import Image, ImageDraw, ImageFont
import os
import re

dirpath = os.path.dirname(os.path.realpath(__file__))

import pandas as pd
import pyodbc as db

def crore(number):
    number = number / 10000000
    number = round(number,1)
    number = format(number, ',')
    number = number + ' Cr'
    return number

import set_name as employ_name
Employee_name=employ_name.name()
employee_search_name='%'+Employee_name+'%'
# print(employee_search_name)

def Mr_Replace(customer_name):
    md_replaced_result = [sub.replace('Mr.', '') for sub in customer_name]
    return md_replaced_result

connection = db.connect('DRIVER={SQL Server};'
                        'SERVER=;'                     # Provide server
                        'DATABASE=;'                   # provide database 
                        'UID=;PWD=')                   # provide username and password

cursor = connection.cursor()

employee_name_desig_df = pd.read_sql_query("""select NSMNAME,NSMID from RFieldForce
where NSMNAME like ?
group by NSMNAME,NSMID""", connection,params={employee_search_name})


Asign_name = employee_name_desig_df['NSMNAME'].tolist()
designation = 'National Sales Manager'
id = employee_name_desig_df['NSMID'].tolist()
sister_concern = "Eskayef Pharmaceuticals Limited"
Company_location = "Transcom Limited"
employee_information = [Asign_name[0],designation,sister_concern,Company_location,id[0]]
print(employee_information)


# print(Mr_Replace(Asign_name))
# print(Mr_Replace(Asign_name)[0].lstrip())

final_employee_name=Mr_Replace(Asign_name)[0].lstrip()
print(final_employee_name)

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
print(monthly_sale)
#---------------------------------------------------------------------

img = Image.open("./images/portfolio.png")

brand1_name = ImageDraw.Draw(img)

font1 = ImageFont.truetype("./fonts/Lobster-Regular.ttf", 50, encoding="unic")
font2 = ImageFont.truetype("./fonts/Viga-Regular.ttf", 27, encoding="unic")
font3 = ImageFont.truetype("./fonts/Viga-Regular.ttf", 27, encoding="unic")
font4 = ImageFont.truetype("./fonts/Viga-Regular.ttf", 20, encoding="unic")
font5 = ImageFont.truetype("./fonts/Anton-Regular.ttf", 25, encoding="unic")
font6 = ImageFont.truetype("./fonts/Lobster-Regular.ttf", 29, encoding="unic")
font7 = ImageFont.truetype("./fonts/Viga-Regular.ttf", 23, encoding="unic")
font8 = ImageFont.truetype("./fonts/Viga-Regular.ttf", 31, encoding="unic")

brand1_name.text((272, 45), final_employee_name, (253,208,59), font=font1)
brand1_name.text((277, 125), employee_information[1], (255,255,255), font=font2)
brand1_name.text((277, 175),'ID : '+ employee_information[4], (255,255,255), font=font3)

brand1_name.text((277, 228), employee_information[2], (253,208,59), font=font8)

brand1_name.text((1077, 100), "Target:", (255,255,255), font=font4)
brand1_name.text((1077, 130), crore(monthly_target[0]), (253,208,59), font=font4)
#
brand1_name.text((1077, 180), "Sales:", (255,255,255), font=font4)
brand1_name.text((1077, 210), crore(monthly_sale[0]), (253,208,59), font=font4)
#
brand1_name.text((840, 41), "Status:", (253,208,59), font=font7)

# brand1_name.text((960, 62), A[3], (0,0,0), font=font4)
# brand1_name.text((960, 125), A[4], (0,0,0), font=font4)

# profile_pic = Image.open("./images/bashir.png")
#
# imageSize = Image.new('RGB', (1270,1500 ))
# imageSize.paste(profile_pic, (50, 50))

img.save('./images/titles_marged.png')
print('name and information are merged with the picture.')

