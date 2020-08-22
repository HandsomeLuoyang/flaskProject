from functools import wraps
from flask_login import current_user
from flask import abort
import traceback


def admin_required(f):
    """
    权限认证装饰器
    :return:
    """
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            print(current_user.pow.pow_id)
            if not current_user or current_user.pow.pow_id != 1:
                abort(403)
            return f(*args, **kwargs)
        except BaseException as e:
            traceback.print_exc()
            abort(403)
    return decorator
