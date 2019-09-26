from flask_socketio import Namespace, join_room
from app.db_utils.user_queries import UserQueries
from app.custom_decorators.auth_handler import LiveSocketAuth

class TestHandler(Namespace):
    @staticmethod
    def on_authenticate(data):
        status, roles =  UserQueries.check_token(user_id=data["user_id"],
                        h_token=data["token"])
        if status:
            UserQueries.start_session(user_id,
                           store="test")
            join_room("test")
            # do operation and emit data
        else:
            disconnect(sid=request.sid)
    @staticmethod
    @LiveSocketAuth.check_login
    def on_test(data):
        print(data)
        
    @staticmethod
    def on_disconnect():
        user_id = request.args.get("user_id", None)
        UserQueries.end_session(user_id=user_id,
                        store="test")
        leave_room("test")