class Codes(object):
    SUCCESS = 'success'
    BAD_REQUEST = 'bad_request'
    UNAUTHORIZED = 'unauthorized'
    FORBIDDEN = 'forbidden'
    NOT_FOUND = 'not_found'
    CONFLICT = 'conflict'
    SERVER_ERROR = 'server_error'

    LOG_IN = 'log_in' #

    CREATE_USER = 'create_user' #
    UPDATE_USER = 'update_user' #
    GET_USER_DATA = 'get_user_data' #

    CREATE_GROUP = 'create_group' #
    UPDATE_GROUP = 'update_group' #
    GET_GROUP_DATA = 'get_group_data' #
    LEAVE_GROUP = 'leave_group' #
    KICK_GROUP_USER = 'kick_group_user' #

    INVITE = 'invite' #
    ACCEPT_INVITE = 'accept_invite' #
    REJECT_INVITE = 'reject_invite' #
    REVOKE_INVITE = 'revoke_invite' #

    CREATE_DIRECTORY = 'create_directory' #
    UPDATE_DIRECTORY = 'update_directory' #
    DELETE_DIRECTORY = 'delete_directory' #

    CREATE_FILE = 'create_file' #
    UPDATE_FILE = 'update_file' #
    DELETE_FILE = 'delete_file' #
    GET_FILE = 'get_file' #

    ADD_EDITOR = 'add_editor' #
    REMOVE_EDITOR = 'remove_editor' #
    GET_EDITORS = 'get_editors' #
    IS_FILE_EDITOR = 'is_file_editor' #

    GET_ADMIN_DATA = 'get_admin_data' #

    PING = 'ping' #