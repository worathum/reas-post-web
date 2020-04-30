secret_key = 'baquooSiriewoM8yae6iemiu1urohshohRo1pahyoo5eigoChei4ieph2wieNgujechooxaen8eSh8eiquael0ke6reo4moh9holohfeyooPhi8leifotoohuthequah'

list_module = ['ddproperty', 'thaihometown', 'renthub']

list_action = ['register_user', 'test_login', 'create_post', 'edit_post', 'boost_post', 'delete_post']

captcha_secret = '28b19f8fa1d583a46e2cec418f8b0172'

logging_config = { 
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': { 
        'standard': { 
            'format': '%(process)d %(asctime)s %(name)s [%(levelname)s] %(filename)s(%(funcName)s) :: %(message)s',
            'datefmt': '%d-%b-%y %H:%M:%S'
        },
    },
    'handlers': { 
        # 'default': { 
        #     'level': 'DEBUG',
        #     'formatter': 'standard',
        #     'class': 'logging.StreamHandler',
        #     'stream': 'ext://sys.stdout',  # Default is stderr
        # },
        'logfile': { 
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/app.log',
            'mode': 'a',
            'maxBytes': 1048576,
            'backupCount': 10
        },
    },
    'loggers': { 
        '': {  # root logger
            'handlers': ['logfile'],
            'level': 'DEBUG',
            'propagate': False
        }
    } 
}