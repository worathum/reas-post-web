# boost post

1. ถ้าไม่ส่ง post_id มา จะหมายถึงให้ทำการ boost post ทั้งหมด แต่ถ้าส่งมา post_id หมายถึงทำอันเดียว
2. เว็บไหนที่ไม่มีปุ่ม boost post ให้ใช้วิธี edit description แทน โดยไปใส่ tags พิเศษที่จะเปลี่ยนไปเรื่อยๆ เช่น ###07:03:2563 12:87###

## post_data
~~~json
{
    "action": "boost_post",
    "timeout": "7",
    "web": [
        {
            "ds_name": "thaihometown",
            "ds_id": "4",
            "post_id": "33333",
            "log_id": "33333",            
            "user": "amarin.ta@gmail.com",
            "pass": "5k4kk3253434"
        },
        {
            "ds_name": "ddproperty",
            "ds_id": "5",
            "post_id": "4444",
            "log_id": "33333",            
            "account_type" : "corperate",
            "user": "amarin.ta@gmail.com",
            "pass": "5k4kk3253434",            
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
    "action": "boost_post",
    "start_time": "0:00:00.771743",
    "end_time": "0:00:00.771743",
    "web": {
        "thaihometown": {
            "success": "true",            
            "start_time": "0:00:00.771743",
            "end_time": "0:00:00.771743",
            "detail": "",
            "ds_id": "4",
            "log_id": "33333",
            "post_id": "33333",
        },
        "ddproperty": {
            "success": "false",
            "start_time": "0:00:00.771743",
            "end_time": "0:00:00.771743",
            "ds_id": "5",
            "detail": "",
            "log_id": "33333",
            "post_id": "4444",
        }
    }
}
~~~
