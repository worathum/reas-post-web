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

addr_district = เขต
addr_sub_district = ตำบล แขวง
addr_road = ถนน
addr_near_by = สถานที่ใกล้เคียง
       
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

post_title_th = หัวข้อประกาศ (ไทย)
post_description_th= รายละเอียดเกี่ยวกับประกาศ (ไทย)

post_title_en = หัวข้อประกาศ (อังกฤษ)
post_description_en = รายละเอียดเกี่ยวกับประกาศ (อังกฤษ)

name = ชื่อตัวแทน
mobile = เบอร์มือถือตัวแทน
email = อีเมล์ตัวแทน
~~~

Only ddproperty
~~~
account_type = ex: normal, coperate

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
    "post_img_url_lists": [
        "http://imagestore.com/pic1.jpg",
        "http://imagestore.com/pic2.jpg",
        "http://imagestore.com/pic3.jpg",
        "http://imagestore.com/pic4.jpg",
        "http://imagestore.com/pic5.jpg"
    ],
    "price_baht": "3000",
    "geo_latitude": "13.786862",
    "geo_longitude": "100.757815",
    "post_title_th": "xxx",
    "post_description_th": "xxx",
    "post_title_en": "",
    "post_description_en": "",
    "web": {
        "thaihometown": {
            "email_user": "amarin.ta@gmail.com",
            "email_pass": "encryped_by_openssljkldsjfldjfklljfdklsjfkldjs"
        },
        "ddproperty": {
            "account_type" : "agent",
            "email_user": "amarin.ta@gmail.com",
            "email_pass": "encryped_by_openssljkldsjfldjfklljfdklsjfkldjs",            
        }
    }
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
        },
        "ddproperty": {
            "success": "false",
            "time_usage": "0:00:00.771743",
            "post_url": "",
            "post_id": "",
            "account_type" : "normal",
            "detail": ""
        }
    }
}
~~~
