# test login

## post_data
~~~json
{
    "action": "test_login",
    "timeout": "5",
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

## Return response json
false message

1. Login failed due to incorrect userid/password
2. System connection timeout in 5 second

~~~json
{
    "success": "true",
    "action": "test_login",
    "start_time": "0:00:00.771743",
    "end_time": "0:00:00.771743",
    "web": {
        "thaihometown": {
            "success": "true",
            "detail": "",
            "start_time": "0:00:00.771743",
            "end_time": "0:00:00.771743",
        },
        "otherweb": {
            "success": "false",
            "detail": "Login failed due to incorrect userid/password",
            "start_time": "0:00:00.771743",
            "end_time": "0:00:00.771743",
        }
    }
}
~~~
