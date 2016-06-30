
from py.test.datagen import (
    ensure_test_data,
)
from py.bin.server import (
    start_server,
)

if __name__ == "__main__":
    ensure_test_data()
    start_server()
