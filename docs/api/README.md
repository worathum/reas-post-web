# API docs
## main post arguement

POST http://homepostapi.webup.site:8080/reaspostweb/apirequest
- access_token ใช้เพื่อ secure api
- post_data จะ encode มาด้วย base64_encode($post_data_json)

python time arguement UTC+0 -0

~~~json
{
    "access_token" : "YeiraupoimeR0aelaebohz8ieb0ShieMahTah0fie7iekae7ke6eichaif5oxah9",
    "post_data" : "base64data"
}
~~~
## post_data
- post_data จะเป็น json
~~~json
{
    "action": "<action_name>",
    "timeout": "<timeout_with_second",
    "global_argument1": "xxx",
    "global_argument2": "xxx",    
    "web": [
        {
            "ds_name": "thaihometown",
            "ds_id": "4",
            "user": "amarin.ta@gmail.com",
            "pass": "5k4kk3253434"
        },
        {
            "ds_name": "thaihometown",
            "ds_id": "4",
            "account_type" : "corperate",
            "user": "amarin.ta@gmail.com",
            "pass": "5k4kk3253434",            
        }
    ]
}
~~~

## return 

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
            "log_id": "33333",
        },
        "ddproperty": {
            "success": "false",
            "start_time": "0:00:00.771743",
            "end_time": "0:00:00.771743",
            "detail": "",
            "log_id": "33333",
        }
    }
}
~~~



