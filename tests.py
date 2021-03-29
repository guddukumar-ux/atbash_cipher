import pytest

from atbash import AtbashCipher


@pytest.fixture
def validate_atbash_data():
    return [
        AtbashCipher("in.txt", "out.txt"),
        AtbashCipher("in1.txt", "out1.txt"),
        AtbashCipher("in2.txt", "out2.txt")
    ]


@pytest.fixture
def encrypt_atbash_data():
    return [
        'Hello world!', 'Christmas is the 25th of December'
    ]


def test_validate(validate_atbash_data):
    """Validate method test"""
    assert list(map(lambda x: x.validate_input(), validate_atbash_data)) == [True, False, False]


def test_encrypt(encrypt_atbash_data):
    """Encryption method check"""
    assert list(map(lambda x: AtbashCipher.encrypt(x), encrypt_atbash_data)) == ['Svool dliow!', 'Xsirhgnzh rh gsv 25gs lu Wvxvnyvi']
