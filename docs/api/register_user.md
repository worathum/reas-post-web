# register user

## post_data
~~~json
{
    "action": "register_user",
    "timeout": "7",
    "web": {
        "thaihometown": {
            "email_user": "amarin.ta@gmail.com",
            "email_pass": "encryped_by_openssl_dklsjfkldjs",
            "name": "Amarin",
            "surname": "Boonkirt",
            "tel": "0891999450"
        },
        "otherweb": {
            "email_user": "amarin.ta@gmail.com",
            "email_pass": "encryped_by_openssl_dklsjfkldjs",
            "name": "Amarin",
            "surname": "Boonkirt",
            "tel": "0891999450"
        }
    }
}
~~~

## Return response json
~~~json
{
    "success": "true",
    "action": "register_user",
    "time_usage":"0:00:00.771743",
    "web": {
        "thaihometown": {
            "success": "true",
            "detail": "",
            "time_usage":"0:00:00.771743"
        },
        "otherweb": {
            "success": "false",
            "detail": "System not required to register",
            "time_usage":"0:00:00.771743",
        }
    }
}
~~~
