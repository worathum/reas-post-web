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

  "action" : "register_user",
  "timeout" : "7",
	"web" : { 
        "thaihometown" : {
            "email_user" : "amarin.ta@gmail.com",
            "email_pass" : "0294kdjfkljeoiurtjffjdklfjkldsjfldjfklljfdklsjfkldjs",
            "name" : "Amarin",
            "surname" : "Boonkirt",
            "tel" : "0891999450"
        }    
    }
}

~~~
