
import subprocess
from py.src.logger import log
from py.src.settings import (
    ENVARS,
)


def load_crontab():
    crontab_path = "install/crontab/crontab-%s" % ENVARS.instance_type
    process_out = subprocess.check_output(
        ["crontab", crontab_path],
    )
    log("crontab out: %s" % process_out)


if __name__ == "__main__":
    load_crontab()
