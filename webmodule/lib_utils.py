import functools
from datetime import datetime
from typing import Dict


def timeit_to_dict(join_dict: bool = True):
    def _timeit(func):
        @functools.wraps(func)
        def _inner_timeit(*args, **kwargs) -> dict:
            start_time = datetime.utcnow()
            result = func(*args, **kwargs)
            end_time = datetime.utcnow()

            time_stats = {
                "start_time": start_time,
                "end_time": end_time,
                "usage_time": end_time - start_time,
            }

            if isinstance(result, dict) and join_dict:
                result.update(time_stats)
                return result
            else:
                time_stats["result"] = result
                return time_stats

        return _inner_timeit

    return _timeit


def serialize_dict(func):
    @functools.wraps(func)
    def serializer(*args, **kwargs) -> Dict[str, str]:
        dict_obj = func(*args, **kwargs)

        return dict_serializer(dict_obj)

    return serializer


def dict_serializer(dict_obj: dict) -> Dict[str, str]:
    if not isinstance(dict_obj, dict):
        raise TypeError("Not a Dict-like Object")

    dict_return = {}
    for key, value in dict_obj.items():
        if type(value) is bool:
            value = "true" if value else "false"
        elif isinstance(value, dict):
            value = dict_serializer(value)
        elif value is None:
            pass  # passthrough for NoneType
        else:
            value = str(value)
        dict_return.update({str(key): value})

    return dict_return
