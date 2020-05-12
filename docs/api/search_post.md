Input Data

{
    "action": "search_post",
    "timeout": "5",
    "post_title_th": "ขาย Watermark Riverside 2 ห้องนอน 68 ตรม ตกแต่งสวย ราคาพิเศษ"
    "web": [
        {
            "ds_name": "thaihometown",
            "ds_id": "4",
            "post_id": "33333",
            "log_id": "33333",             
            "user": "amarin.ta@gmail.com",
            "pass": "5k4kk3253434"
        },
        {
            "ds_name": "ddproperty",
            "ds_id": "5",
            "post_id": "4444",
            "log_id": "44444",             
            "user": "amarin.ta@gmail.com",
            "pass": "5k4kk3253434",            
        }
    ]
}


Return Value
{
    "success": "true",
    "action": "search_post",
    "start_time": "0:00:00.771743",
    "end_time": "0:00:00.771743",
    "web": {
        "thaihometown": {
            "success": "true",            
            "start_time": "0:00:00.771743",
            "end_time": "0:00:00.771743",
            "ds_id": "4",
            "post_url": "http://xxxxx/post/232323",
            "post_id": "33333",
            "account_type" : null,
        },
        "ddproperty": {
            "success": "false",
            "start_time": "0:00:00.771743",
            "end_time": "0:00:00.771743",
            "ds_id": "5",
            "post_url": "",
            "post_id": "",
            "detail": ""
        }
    }
}
