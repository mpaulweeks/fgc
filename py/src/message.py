
import requests

from py.src.logger import (
    log,
    read_logs,
)
from py.src.settings import (
    ENVARS,
)
from py.src.time_util import (
    convert_dt_to_nyc,
)


def send_error_message(message):
    log('sending error email')
    text = "server: %s\n\n%s\n\nlogging:\n\n%s" % (
        ENVARS.server_name, message, read_logs()
    )
    return requests.post(
        "https://api.mailgun.net/v3/%s/messages" % ENVARS.mailgun_domain_name,
        auth=(
            "api",
            ENVARS.mailgun_api_key,
        ),
        data={
            "from": "FGCBOT <robot@%s>" % ENVARS.mailgun_domain_name,
            "to": [ENVARS.mailgun_recipient],
            "subject": "FGC STATUS %s" % convert_dt_to_nyc(),
            "text": text,
        },
    )
