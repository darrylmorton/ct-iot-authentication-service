from utils.app_util import AppUtil


class TestAppUtil:
    async def test_get_app_version(self):
        actual_result = AppUtil.get_app_version()

        assert actual_result == "1.0.1"
