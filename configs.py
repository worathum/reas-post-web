secret_key = 'YeiraupoimeR0aelaebohz8ieb0ShieMahTah0fie7iekae7ke6eichaif5oxah9'

list_module = ['ddproperty', 'thaihometown', 'renthub']

list_action = ['register_user', 'test_login', 'create_post', 'edit_post', 'boost_post', 'delete_post']


logging_config = { 
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': { 
        'standard': { 
            'format': '%(process)d %(asctime)s [%(levelname)s] %(name)s :: %(message)s',
            'datefmt': '%d-%b-%y %H:%M:%S'
        },
    },
    'handlers': { 
        'default': { 
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
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
            'handlers': ['default','logfile'],
            'level': 'DEBUG',
            'propagate': False
        }
    } 
}