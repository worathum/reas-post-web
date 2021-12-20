
class action_form(object):

    def __init__(self):
        self.webname = ""

    def form(self):
        postdata = {}
        time_usage = ""
        time_start = ""
        time_end = ""
        success = ""
        detail = ""
        device_id = ""
        mem_id = ""
        mem_status = ""
        post_url = ""
        post_id = ""
        post_view = ""

        data = {
        'test_login': [
            {
            "websitename": self.webname,
            "usage_time": str(time_usage),
            "start_time": str(time_start),
            "end_time": str(time_end),
            "success": success,
            "detail": detail,
            'device_id': device_id,
            'mem_id': mem_id,
            'mem_status': mem_status,
            "ds_id": postdata['ds_id']
            }
        ],
        'register_post': [
            {
                "websitename": self.webname,
                "success": success,
                "usage_time": str(time_usage),
                "start_time": str(time_start),
                "end_time": str(time_end),
                'ds_id': postdata['ds_id'],
                "detail": detail,
            }
        ],
        'create_post':[
            {
                "success": success,
                "websitename": self.webname,
                "usage_time": str(time_usage),
                "start_time": str(time_start),
                "end_time": str(time_end),
                "post_url": post_url,
                "post_id": post_id,
                "account_type": "null",
                "detail": detail,
            }
        ],
        'edit_post':[
            {
                    "success": success,
                    "websitename": self.webname,
                    "usage_time": str(time_usage),
                    "start_time": str(time_start),
                    "end_time": str(time_end),
                    "post_url": post_url,
                    "post_id": post_id,
                    "account_type": "null",
                    "detail": detail,
            }
        ],
        'delete_post':[
            {
                    "success": success,
                    "usage_time": time_end - time_start,
                    "start_time": time_start,
                    "end_time": time_end,
                    "detail": detail,
                    "log_id": postdata['log_id'],
                    "ds_id": postdata['ds_id'],
                    "post_id": postdata['post_id'],
                    "websitename": self.webname,
            }
        ],
        'boost_post':[
            {
                    "success": success,
                    "usage_time": time_usage,
                    "start_time": time_start,
                    "end_time": time_end,
                    "detail": detail,
                    "log_id": postdata['log_id'],
                    "ds_id": postdata['ds_id'],
                    "post_id": postdata['post_id'],
                    "websitename": self.webname,
                    "post_view": ''
            }
        ],
        'search_post':[
            {
                    "success": success,
                    "usage_time": str(time_usage),
                    "start_time": str(time_start),
                    "end_time": str(time_end),
                    "detail": detail,
                    "websitename": self.webname,
                    "account_type": None,
                    "ds_id": postdata['ds_id'],
                    "log_id": postdata['log_id'],
                    "post_id": post_id,
                    "post_created": '',
                    "post_modified": "",
                    "post_view": post_view,
                    "post_url": post_url
            }
        ]
        }
        return data
