# test login

## post_data
~~~json
{
    "action": "test_login",
    "timeout": "5",
    "web": {
        "thaihometown": {
            "email_user": "amarin.ta@gmail.com",
            "email_pass": "encryped_by_openssljkldsjfldjfklljfdklsjfkldjs"
        },
        "otherweb": {
            "email_user": "amarin.ta@gmail.com",
            "email_pass": "encryped_by_openssljkldsjfldjfklljfdklsjfkldjs"
        }
    }
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
    "time_usage":"0:00:00.771743",
    "web": {
        "thaihometown": {
            "success": "true",
            "detail": "",
            "time_usage":"0:00:00.771743"
        },
        "otherweb": {
            "success": "false",
            "detail": "Login failed due to incorrect userid/password",
            "time_usage":"0:00:00.771743",
        }
    }
}
~~~
