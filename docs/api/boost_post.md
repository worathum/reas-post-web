# boost post

1. ถ้าไม่ส่ง post_id มา จะหมายถึงให้ทำการ boost post ทั้งหมด แต่ถ้าส่งมา post_id หมายถึงทำอันเดียว
2. เว็บไหนที่ไม่มีปุ่ม boost post ให้ใช้วิธี edit description แทน โดยไปใส่ tags พิเศษที่จะเปลี่ยนไปเรื่อยๆ เช่น ###07:03:2563 12:87###

## post_data
~~~json
{
    "action": "boost_post",
    "timeout": "5",
    
    "web": {
        "thaihometown": {
            "post_id": "33333",
            "log_id": "33333",
            "email_user": "amarin.ta@gmail.com",
            "email_pass": "encryped_by_openssljkldsjfldjfklljfdklsjfkldjs"
        },
        "ddproperty": {       
            "post_id": "33333",
            "log_id": "33333",
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
    "action": "boost_post",
    "time_usage": "0:00:00.771743",
    "web": {
        "thaihometown": {
            "success": "true",            
            "time_usage": "0:00:00.771743",
            "detail": "",
            "log_id": "33333",
        },
        "ddproperty": {
            "success": "false",
            "time_usage": "0:00:00.771743",
            "detail": "",
            "log_id": "33333",
        }
    }
}
~~~
