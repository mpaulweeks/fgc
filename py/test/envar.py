
from py.test.tools import (
    BaseTestCase,
)
from py.src.settings.envar import (
    _ENVARS,
)


class EnvarTest(BaseTestCase):

    def test_is_web_server(self):
        sut = _ENVARS({})
        self.assertTrue(sut.is_web_server())
        sut = _ENVARS({"instance_type": "dev"})
        self.assertTrue(sut.is_web_server())
        sut = _ENVARS({"instance_type": "web"})
        self.assertTrue(sut.is_web_server())
        sut = _ENVARS({"instance_type": "api"})
        self.assertFalse(sut.is_web_server())
        sut = _ENVARS({"instance_type": "scraper"})
        self.assertFalse(sut.is_web_server())

    def test_is_api_server(self):
        sut = _ENVARS({})
        self.assertFalse(sut.is_api_server())
        sut = _ENVARS({"instance_type": "dev"})
        self.assertFalse(sut.is_api_server())
        sut = _ENVARS({"instance_type": "web"})
        self.assertFalse(sut.is_api_server())
        sut = _ENVARS({"instance_type": "api"})
        self.assertTrue(sut.is_api_server())
        sut = _ENVARS({"instance_type": "scraper"})
        self.assertFalse(sut.is_api_server())
