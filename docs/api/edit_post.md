# edit post

## post_data
~~~json
{
    "action": "edit_post",
    "timeout": "5",
    "post_img_url_lists": [
        "http://imagestore.com/pic1.jpg",
        "http://imagestore.com/pic2.jpg",
        "http://imagestore.com/pic3.jpg",
        "http://imagestore.com/pic4.jpg",
        "http://imagestore.com/pic5.jpg"
    ],
    "price_baht": "5",
    "county": "เขต",
    "district": "แขวง",
    "geo_latitude": "13.786862",
    "geo_longitude": "100.757815",
    "post_title_th": "xxx",
    "post_description_th": "xxx",
    "post_title_en": "",
    "post_description_en": "",
    "web": {
        "thaihometown": {
            "post_id": "33333",
            "email_user": "amarin.ta@gmail.com",
            "email_pass": "encryped_by_openssljkldsjfldjfklljfdklsjfkldjs"
        },
        "ddproperty": {
            "post_id": "44444",
            "email_user": "amarin.ta@gmail.com",
            "email_pass": "encryped_by_openssljkldsjfldjfklljfdklsjfkldjs",
            "project_name": "ลุมพินี"
        }
    }
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
    "action": "edit_post",
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
