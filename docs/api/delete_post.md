# delete post

## post_data
~~~json
{
    "action": "delete_post",
    "timeout": "5",
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
            "ds_id": "4",
            "post_id": "33333",
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
3. System maintenance

~~~json
{
    "success": "true",
    "action": "delete_post",
    "start_time": "0:00:00.771743",
    "end_time": "0:00:00.771743",
    "web": {
        "thaihometown": {
            "success": "true",   
            "post_id": "33333",
            "ds_id": "4",
            "log_id": "33333",
            "start_time": "0:00:00.771743",
            "end_time": "0:00:00.771743",
            "detail": ""
        },
        "ddproperty": {
            "success": "false",
            "post_id": "33333",
            "ds_id": "4",
            "log_id": "33333",
            "start_time": "0:00:00.771743",
            "end_time": "0:00:00.771743",
            "detail": ""
        }
    }
}
~~~
