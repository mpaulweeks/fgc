
from py.test.tools import (
    BaseTestCase,
)
from py.src.s3_store import (
    download_global_cache,
)
from py.src.error import (
    TestingException,
)
from py.src.settings import (
    ensure_not_testing,
)


class BaseTestCaseTest(BaseTestCase):

    def test_ensure_not_testing(self):
        with self.assertRaises(TestingException):
            ensure_not_testing()

    def test_s3_mocked_out(self):
        with self.assertRaises(TestingException):
            download_global_cache()
