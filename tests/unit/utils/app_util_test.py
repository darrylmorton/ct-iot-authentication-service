from unittest import skip

from utils.app_util import AppUtil


class TestAppUtil:
    def test_get_app_version(self):
        actual_result = AppUtil.get_app_version()

        assert actual_result == "2.0.0"

    @skip
    def test_set_openapi_info(self):
        pass

    @skip
    def test_validate_uuid4(self):
        pass

    @skip
    def test_create_token_expiry(self):
        pass
