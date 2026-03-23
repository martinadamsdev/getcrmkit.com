import pytest

from app.domain.auth.exceptions import AuthenticationError, WeakPasswordError
from app.domain.auth.value_objects import Email, Password, Token, TokenPair


class TestEmail:
    def test_valid_email(self):
        email = Email("user@example.com")
        assert email.value == "user@example.com"

    def test_normalizes_case(self):
        email = Email("User@Example.COM")
        assert email.value == "user@example.com"

    def test_strips_whitespace(self):
        email = Email("  user@example.com  ")
        assert email.value == "user@example.com"

    @pytest.mark.parametrize(
        "invalid",
        [
            "",
            "not-an-email",
            "@no-local.com",
            "no-domain@",
            "spaces in@email.com",
            "no@dots",
        ],
    )
    def test_invalid_email_raises(self, invalid):
        with pytest.raises(ValueError, match="Invalid email"):
            Email(invalid)

    def test_equality(self):
        assert Email("a@b.com") == Email("A@B.COM")

    def test_str(self):
        assert str(Email("user@example.com")) == "user@example.com"


class TestPassword:
    def test_hash_and_verify(self):
        pw = Password.from_plain("Secure123")
        assert pw.verify("Secure123") is True
        assert pw.verify("wrong") is False

    def test_hash_is_not_plaintext(self):
        pw = Password.from_plain("Secure123")
        assert pw.hashed != "Secure123"
        assert pw.hashed.startswith("$2b$")

    def test_from_hash(self):
        pw1 = Password.from_plain("Secure123")
        pw2 = Password.from_hash(pw1.hashed)
        assert pw2.verify("Secure123") is True

    def test_rejects_short_password(self):
        with pytest.raises(WeakPasswordError, match="at least 8"):
            Password.from_plain("Ab1")

    def test_rejects_all_numeric(self):
        with pytest.raises(WeakPasswordError, match="letter"):
            Password.from_plain("12345678")

    def test_rejects_all_alpha(self):
        with pytest.raises(WeakPasswordError, match="digit"):
            Password.from_plain("abcdefgh")


class TestToken:
    SECRET = "test-secret-key"

    def test_encode_decode_access(self):
        token = Token.create_access_token(
            user_id="user-123",
            secret=self.SECRET,
            algorithm="HS256",
            expire_minutes=60,
        )
        payload = Token.decode(token.value, secret=self.SECRET, algorithm="HS256")
        assert payload["sub"] == "user-123"
        assert payload["type"] == "access"
        assert "jti" in payload
        assert "exp" in payload

    def test_encode_decode_refresh(self):
        token = Token.create_refresh_token(
            user_id="user-123",
            secret=self.SECRET,
            algorithm="HS256",
            expire_days=30,
        )
        payload = Token.decode(token.value, secret=self.SECRET, algorithm="HS256")
        assert payload["sub"] == "user-123"
        assert payload["type"] == "refresh"

    def test_refresh_token_with_remember_me_flag(self):
        token = Token.create_refresh_token(
            user_id="user-123",
            secret=self.SECRET,
            algorithm="HS256",
            expire_days=30,
            remember_me=True,
        )
        payload = Token.decode(token.value, secret=self.SECRET, algorithm="HS256")
        assert payload["remember_me"] is True

    def test_expired_token_raises(self):
        token = Token.create_access_token(
            user_id="user-123",
            secret=self.SECRET,
            algorithm="HS256",
            expire_minutes=-1,
        )
        with pytest.raises(AuthenticationError, match="expired"):
            Token.decode(token.value, secret=self.SECRET, algorithm="HS256")

    def test_invalid_token_raises(self):
        with pytest.raises(AuthenticationError):
            Token.decode("invalid.token.value", secret=self.SECRET, algorithm="HS256")

    def test_jti_is_unique(self):
        t1 = Token.create_access_token("u1", self.SECRET, "HS256", 60)
        t2 = Token.create_access_token("u1", self.SECRET, "HS256", 60)
        p1 = Token.decode(t1.value, self.SECRET, "HS256")
        p2 = Token.decode(t2.value, self.SECRET, "HS256")
        assert p1["jti"] != p2["jti"]


class TestTokenPair:
    def test_creation(self):
        pair = TokenPair(
            access_token="access",
            refresh_token="refresh",
            expires_in=3600,
        )
        assert pair.access_token == "access"
        assert pair.refresh_token == "refresh"
        assert pair.token_type == "bearer"
        assert pair.expires_in == 3600
