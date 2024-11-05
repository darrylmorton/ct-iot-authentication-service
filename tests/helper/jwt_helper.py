import datetime

from tests.config import JWT_EXPIRY_SECONDS


class JwtHelper:
    @staticmethod
    def create_token_expiry(_seconds=JWT_EXPIRY_SECONDS) -> datetime:
        return datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(
            seconds=_seconds
        )
