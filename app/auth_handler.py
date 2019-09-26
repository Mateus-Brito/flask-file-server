from app.user_queries import UserQueries

class LiveSocketAuth(object):
    @staticmethod
    def check_login(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            """
            :param args:
            :param kwargs:
            :return:
            """
            user_id = request.args.get("user_id", None)
            if user_id is None:
                disconnect(sid=request.sid)
            else:
                status = UserQueries.check_session(user_id=user_id,
                                                   store="test")
                if not status:
                    disconnect(request.sid)

            return f(*args, **kwargs)

        return decorated_function