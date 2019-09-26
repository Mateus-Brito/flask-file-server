import unittest
from parameterized import parameterized
from app.auth import passwordsAreIdentical

class test_DifferentPasswords(unittest.TestCase):
    @parameterized.expand([
        ["password", "Password"],
        ["password", "PASSWORD"],
        ["password", "passwor"],
        ["password", "assword"],
    ])
    
    def test_sequence(self, password, cpassword):
        result = passwordsAreIdentical(password, cpassword)
        self.assertFalse( result )