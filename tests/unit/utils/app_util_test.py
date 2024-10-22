from unittest import skip

from utils.app_util import AppUtil


class TestAppUtil:
    async def test_get_app_version(self):
        actual_result = AppUtil.get_app_version()

        assert actual_result == "1.0.0"

    @skip
    async def test_set_openapi_info(self):
        pass

    @skip
    async def test_validate_uuid4(self):
        pass
