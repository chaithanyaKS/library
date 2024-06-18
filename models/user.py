import hashlib
import secrets
from typing import Any, List, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(String(256))
    name: Mapped[str] = mapped_column(String(30))
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)

    _min_password_length = 8
    _max_password_length = 128
    _iteration_count = 6_00_000
    _prefix = "pbkdf2_sha256"

    @classmethod
    def _get_salt(cls):
        return secrets.token_hex(16)

    def set_password(self, password: str):
        self._validate_password(password)
        salt = self._get_salt()
        self.password = self._hash_password(password, salt)

    @classmethod
    def _validate_password(cls, password: str):
        """
        Validate the raw password. Used by :meth:`update_password` and
        :meth:`create_user`.

        :param password:
            The raw password e.g. ``'hello123'``.
        :raises ValueError:
            If the password fails any of the criteria.

        """
        if not password:
            raise ValueError("A password must be provided.")

        if len(password) < cls._min_password_length:
            raise ValueError("The password is too short.")

        if len(password) > cls._max_password_length:
            raise ValueError("The password is too long.")

        if password.startswith(cls._prefix):
            raise ValueError("Do not pass a hashed password.")

    @classmethod
    def _hash_password(
        cls, password: str, salt: str = "", iterations: Optional[int] = None
    ) -> str:
        """
        Hashes the password, ready for storage, and for comparing during
        login.

        :raises ValueError:
            If an excessively long password is provided.

        """
        if len(password) > cls._max_password_length:
            raise ValueError("The password is too long.")

        if not salt:
            salt = cls._get_salt()

        if iterations is None:
            iterations = cls._iteration_count

        hashed = hashlib.pbkdf2_hmac(
            "sha256",
            bytes(password, encoding="utf-8"),
            bytes(salt, encoding="utf-8"),
            iterations,
        ).hex()
        return f"pbkdf2_sha256${iterations}${salt}${hashed}"

    @classmethod
    def _split_stored_password(cls, password: str) -> List[str]:
        elements = password.split("$")
        if len(elements) != 4:
            raise ValueError("Unable to split hashed password")
        return elements

    @classmethod
    def check_password(cls, hashed_password, password) -> bool:
        prefix, iterations, salt, current_password = cls._split_stored_password(
            hashed_password
        )
        h_password = cls._hash_password(password, salt, int(iterations))

        return h_password == hashed_password

    def __setattr__(self, name: str, value: Any):
        """
        Make sure that if the password is set, it's stored in a hashed form.
        """
        if name == "password" and not value.startswith("pbkdf2_sha256"):
            value = self.__class__._hash_password(value)

        super().__setattr__(name, value)
