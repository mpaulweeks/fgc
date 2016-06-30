
from datetime import datetime

_log_file = open('temp/default.log', 'w')
_logs = []


def read_logs():
    global _logs
    return '\n'.join(_logs)


def set_log_file(file_name):
    global _log_file
    _log_file.close()
    _log_file = open("temp/%s.log" % file_name, 'w')
    log('set log file: %s' % file_name)


def log(message):
    global _log_file
    global _logs
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    message = '%s | %s' % (timestamp, str(message))
    print (message)
    print (message, file=_log_file)
    _logs.append(message)


def log_exception(exception):
    message = (
        "------- EXCEPTION -------"
        "\n%s\n"
        "-------------------------"
    ) % repr(exception)
    log(message)
