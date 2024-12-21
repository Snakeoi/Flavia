from dataclasses import dataclass


@dataclass
class _Cfg:
    prompt: str


@dataclass
class _RegexCfg:
    pattern: str
    prompt: str
    
    
@dataclass
class _LengthCfg:
    min: int
    max: int
    prompt: str
    

class Email:
    required = _Cfg('Password is required.')
    email = _Cfg('Must be valid email address.')
    length = _LengthCfg(1, 64, "Email is to long")


class Username:
    required = _Cfg('Username is required.')
    length = _LengthCfg(3, 32, "Username must be between 3 and 32 characters.")
    regex = _RegexCfg(
        r"^[^\d!@#$%^&*()_+=\[\]{}|\\:;\"<>,.?/`~]+$",
        "User names can only contain letters, spaces, hyphens, and apostrophes."
    )


class Password:
    required = _Cfg('Password is required.')
    length = _LengthCfg(8, 64, "Password must be between 8 and 64 characters.")
    regex = _RegexCfg(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).+$',
        'Password must have at least one uppercase and one lowercase one number and special character.'
    )


class PasswordRepeat:
    required = _Cfg('Repeated password is required.')
    equal_to = _Cfg('Passwords must be equal.')


class Pin:
    regex = _RegexCfg(
        r'^\d\d\d\d\d\d$',
        'Not valid PIN'
    )
