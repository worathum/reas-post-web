# create post

arguement ที่ยังสงสัย
~~~

~~~

Common arguement
~~~    
action = create_post
timeout = process ทั้งหมดจะต้องเสร็จภายในวินาที่กำหนด ถ้ามีบางเว็บทำไม่เสร็จจะตัดเป็น false 
    ทั่วไปเราจะกำหนดไว้ที่ 5 วินาที กรณี retry เราอาจจะปรับเป็น 7 วินาทีก็ได้เลือกเอาตามความเหมาะสม
listing_type = ประเภทประกาศ / ต้องการ 
    ex: ขาย ให้เช่า
project_name = รายละเอียดที่ตั้ง    ex: ลุมพินี  
property_type_select = ประเภทของอสังหา
    ex:
        คอนโด
        บ้านเดี่ยว
        ทาวน์เฮ้าส์
        ที่ดิน
        อพาร์ทเมนท์
        กิจการ
        สำนักงาน
        พื้นที่ขายของ
        ตึกแถว-อาคารพาณิชย์
        โกดัง-โรงงาน
building = ชื่ออาคาร
floor_level = อยู่ชั้นที่
floor_area
bath_room = จำนวนห้องนอน
bed_room = จำนวนห้องนอน
floor_total = ชั้นทั้งหมด
prominent_point = จุดเด่น
view_type = วิว
    ex:
        แม่น้ำ
        สวน
        เมือง
        สระว่ายน้ำ
        ภูเขา
        ทะเล
addr_province = จังหวัด
addr_district = เขต
addr_sub_district = ตำบล แขวง
addr_road = ถนน
addr_soi = ซอย
addr_near_by = สถานที่ใกล้เคียง

# บ้าน - ที่ดิน (ที่ไม่ใช่คอนโดจะมีค่านี้)
floorarea_sqm = พื้นที่ใช้สอย
land_size_rai = ขนาดที่ดินเป็นไร่
land_size_ngan = ขนาดที่ดินเป็นงาน
land_size_wa = ขนาดที่ดินเป็นวา
       
post_img_url_lists = ลิสต์ของ image url ที่เราจะอัพโหลดเข้าไปในโพส โครงสร้างเป็น json array
    ex:
        [
            "http://imagestore.com/pic1.jpg",
            "http://imagestore.com/pic2.jpg"        
        ]
floorarea_sqm = พื้นที่ (ตารางเมตร) ex: 48
price_baht = ราคา ex: 300000
geo_latitude = ค่าละติจูด ex: 29098209328
geo_longitude = ค่าลองติจูด ex: 29098209328

property_id = รหัสทรัพย์ alias
post_title_th = หัวข้อประกาศ (ไทย)
short_post_title_th = หัวข้อประกาศสั้น (ไทย)
post_description_th= รายละเอียดเกี่ยวกับประกาศ (ไทย)

post_title_en = หัวข้อประกาศ (อังกฤษ)
short_post_title_en = หัวข้อประกาศสั้น (อังกฤษ)
post_description_en = รายละเอียดเกี่ยวกับประกาศ (อังกฤษ)

name = ชื่อตัวแทน
mobile = เบอร์มือถือตัวแทน
email = อีเมล์ตัวแทน
line = ไอดีไลน์
~~~

Only ddproperty
~~~
account_type = ex: normal, corperate

SPECIAL PROCESS:

if not define account_type: 
    account_type = normal
    if content have word "รายละเอียดตัวแทน":
        account_type = coperate
if account_type == coperate
    fill form
        name = ชื่อตัวแทน
        mobile = เบอร์มือถือตัวแทน
        email = อีเมล์ตัวแทน    
return account_type = normal, coperate
~~~

## post_data
~~~json
{
    "action": "create_post",
    "timeout": "5",
    "listing_type": "ขาย",    
    "property_type": "คอนโด",
    "post_img_url_lists": [
        "http://imagestore.com/pic1.jpg",
        "http://imagestore.com/pic2.jpg",        
    ],
    "price_baht": "3000",
    
    "addr_province": "จังหวัด",
    "addr_district": "เขต",
    "addr_sub_district": "ตำบล แขวง",
    "addr_road": "ถนน",
    "addr_near_by": "สถานที่ใกล้เคียง",
    "floorarea_sqm"
    "geo_latitude": "13.786862",
    "geo_longitude": "100.757815",
    
    "property_id" : "",
    "post_title_th": "xxx",
    "post_description_th": "xxx",
    "post_title_en": "",
    "post_description_en": "",

    "web": [
        {
            "ds_name": "thaihometown",
            "ds_id": "4",            
            "account_type" : null,
            "user": "amarin.ta@gmail.com",
            "pass": "4923892394i0923i",
            "project_name": "ลุมพินี",
           
        },
        {
            "ds_name": "thaihometown",
            "ds_id": "4",
            "account_type" : "corperate",
            "user": "amarin.ta@gmail.com",
            "pass": "34k34k;l3k4l3;"
            "project_name": "ลุมพินี",
        }
    ]
}
~~~

## Return response json
false message

1. Login failed due to incorrect userid/password
2. System connection timeout in 5 second
3. System not allowed to post cause "please wait 2 hour / system maintenance"

~~~json
{
    "success": "true",
    "action": "create_post",
    "time_usage": "0:00:00.771743",
    "web": {
        "thaihometown": {
            "success": "true",            
            "time_usage": "0:00:00.771743",
            "post_url": "http://xxxxx/post/232323",
            "post_id": "33333",
            "account_type" : null,
        },
        "ddproperty": {
            "success": "false",
            "time_usage": "0:00:00.771743",
            "post_url": "",
            "post_id": "",
            "account_type" : "corperate / normal",            
            "detail": ""
        }
    }
}
~~~
