import unittest

from grandid.exceptions import BankIDOutstandingTransactionError
from grandid.exceptions import IncorrectSSNError


class GetErrorClassTests(unittest.TestCase):
    @property
    def _fut(self):
        from grandid.exceptions import get_error_class

        return get_error_class

    def test_get_error_class_transaction(self):
        data = {
            "grandidObject": {
                "autoStartToken": "[Filtered]",
                "code": "BANKID_MSG",
                "message": {"hintCode": "outstandingTransaction", "status": "pending"},
                "sessionId": "abc",
            }
        }
        result = self._fut(data)
        self.assertIsInstance(result, BankIDOutstandingTransactionError)

    def test_get_error_class_current_docs(self):
        data = {
            "errorObject": {
                "code": "INCORRECT_SSN",
                "message": "SSN bad",
            }
        }
        result = self._fut(data)
        self.assertIsInstance(result, IncorrectSSNError)


if __name__ == "__main__":
    unittest.main()
