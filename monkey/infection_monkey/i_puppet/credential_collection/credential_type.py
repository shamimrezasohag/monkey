from enum import Enum


class CredentialType(Enum):
    USERNAME = 1
    PASSWORD = 2
    NT_HASH = 3
    LM_HASH = 4
