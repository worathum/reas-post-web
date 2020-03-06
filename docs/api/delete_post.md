# delete post



## post_data
~~~json
{
    "action": "delete_post",
    "timeout": "5",
    
    "web": {
        "thaihometown": {
            "post_id": "33333",
            "email_user": "amarin.ta@gmail.com",
            "email_pass": "encryped_by_openssljkldsjfldjfklljfdklsjfkldjs"
        },
        "ddproperty": {  
            "post_id": "444444",
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
3. System maintenance"

~~~json
{
    "success": "true",
    "action": "delete_post",
    "time_usage": "0:00:00.771743",
    "web": {
        "thaihometown": {
            "success": "true",            
            "time_usage": "0:00:00.771743",
            "detail": ""
        },
        "ddproperty": {
            "success": "false",
            "time_usage": "0:00:00.771743",
            "detail": ""
        }
    }
}
~~~
