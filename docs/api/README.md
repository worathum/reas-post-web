# API docs
## main post arguement
- access_token ใช้เพื่อ secure api
- post_data จะ encode มาด้วย base64_encode($post_data_json)

~~~json
{
    "access_token" : "jeoijroiejroweijrlkasdfjlkjeoijfiojdsj",
    "post_data" : "base64data"
}
~~~
## post_data
- post_data จะเป็น json
- email_pass จะ encrypt มาด้วย openssl ซึ่งทางฝั่ง api จะต้อง decrypt ด้วย key ก่อนนำไปใช้
~~~json
{
    "action": "<action_name>",
    "timeout": "<timeout_with_second",
    "global_argument1": "xxx",
    "global_argument2": "xxx",    
    "web": {
        "thaihometown": {
            "email_user": "amarin.ta@gmail.com",
            "email_pass": "encryped_by_openssljkldsjfldjfklljfdklsjfkldjs"
        },
        "ddproperty": {
            "email_user": "amarin.ta@gmail.com",
            "email_pass": "encryped_by_openssljkldsjfldjfklljfdklsjfkldjs",
        }
    }
}
~~~
