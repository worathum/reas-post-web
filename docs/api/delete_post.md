# delete post



## post_data
~~~json
{
    "action": "delete_post",
    "timeout": "5",
    
    "web": {
        "thaihometown": {
            "post_id": "33333",
            "log_id": "33333",
            "user": "amarin.ta@gmail.com",
            "pass": "encryped_by_openssljkldsjfldjfklljfdklsjfkldjs"
        },
        "ddproperty": {  
            "post_id": "444444",
            "log_id": "33333",
            "user": "amarin.ta@gmail.com",
            "pass": "encryped_by_openssljkldsjfldjfklljfdklsjfkldjs",
        }
    }
}
~~~

## Return response json
false message

1. Login failed due to incorrect userid/password
2. System connection timeout in 5 second
3. System maintenance"

~~~json
{
    "success": "true",
    "action": "delete_post",
    "time_start": "0:00:00.771743",
    "web": {
        "thaihometown": {
            "success": "true",      
            "log_id": "33333",
            "time_usage": "0:00:00.771743",
            "detail": ""
        },
        "ddproperty": {
            "success": "false",
            "log_id": "33333",
            "time_usage": "0:00:00.771743",
            "detail": ""
        }
    }
}
~~~
