# register user

name_title = mr mrs miss

## post_data
~~~json
{
    "action": "register_user",
    "timeout": "7",
    "web": [
        {
            "ds_name": "thaihometown",
            "ds_id": "4",
            "user": "amarin.ta@gmail.com",
            "pass": "5k4kk3253434",
            "company_name": "amarin inc",
            "name_title": "mr",
            "name_th": "อัมรินทร์",
            "surname_th": "บุญเกิด",
            "name_en": "Amarin",
            "surname_en": "Boonkirt",
            "tel": "0891999450",
            "line": "amarin.ta",
            "addr_province" : "nonthaburi"            
        },
        {
            "ds_name": "thaihometown",
            "ds_id": "5",
            "account_type" : "corperate",
            "user": "amarin.ta@gmail.com",
            "pass": "5k4kk3253434",
            "company_name": "amarin inc",
            "name_title": "mr",
            "name_th": "อัมรินทร์",
            "surname_th": "บุญเกิด",
            "name_en": "Amarin",
            "surname_en": "Boonkirt",
            "email": "amarin.ta@gmail.com",
            "tel": "0891999450",
            "line": "amarin.ta",
            "addr_province" : "nonthaburi"
        }
    ]
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
            "start_time": "0:00:00.771743",
            "end_time": "0:00:00.771743",
        }
    }
}
~~~
