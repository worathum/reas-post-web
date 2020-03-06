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
false message

1. System required to manual register and confirm email at https://www.ddproperty.com/agent-register?package=TRIAL
2. System required to direct contact to create account
3. System not required to register
4. System connection timeout in 7 second

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
