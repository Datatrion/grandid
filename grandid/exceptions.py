import logging
from typing import Dict

logger = logging.getLogger(__name__)


def get_error_class(data):
    errorObject = data.get("errorObject")
    error_class = _ERROR_CODE_TO_CLASS.get(errorObject.get("code"), GrandIDError)
    return error_class("{0}: {1}".format(errorObject.get("code"), errorObject.get("message")), errorObject)


def get_bankid_message_error(message, data):
    msg = data.get("message")
    error_class = _BANKID_MSG_CODE_TO_CLASS.get(msg.get("hintCode"), BankIDMessageError)
    return error_class("{0}: {1}".format(msg.get("status"), msg.get("hintCode")), msg)


class GrandIDError(Exception):
    """Parent exception class for all GrandID errors."""


class GrandIDWarning(Warning):
    """Warning class for GrandID."""


class IncorrectURLDataError(GrandIDError):
    """
    Incorrect URL data

    This happens when we could not find a base64 encoded url sent with FederatedLogin.
    """


class IncorrectSSNError(GrandIDError):
    """
    Incorrect SSN

    This happens when SSN does not have 12 digits or is not a valid SSN.
    """


class BankIDIncorrectDataError(GrandIDError):
    """
    Incorrect User Visible Data

    This happens when we could not find a base64 encoded User Visible Data sent with FederatedLogin.
    """


class IncorrectSignDataError(GrandIDError):
    """
    Missing User Visible Data

    This happens when BankID could not find User Visible Data to sign it.
    """


class BankIDError(GrandIDError):
    """
    BankID Error

    This happens when the connexion with BankID fails because of internal error, Maintenance or request timeout,…etc.
    In that case Grandid forward the error message from BankID to the client.
    """


class BankIDSignNotAllowedError(GrandIDError):
    """
    BankID sign not allowed

    This usually happens when you try to use BankID sign but you have requested a bankid service for authenticating only.
    """


class BankIDSignUserVisibleSizeError(GrandIDError):
    """
    Sign data too large

    This happens when too much data is being passed in either userVisibleData or userNonVisibleData, their respective
    limits are 40000 and 200000 characters after base64 encoding.
    """


class BankIDSignUserNonvisibleSizeError(GrandIDError):
    """
    Sign data too large

    This happens when too much data is being passed in either userVisibleData or userNonVisibleData, their respective
    limits are 40000 and 200000 characters after base64 encoding.
    """


class InvalidCertificatePolicyError(GrandIDError):
    """
    Invalid certificate policy

    This error happens if both mobileBankId and desktopBankId are set to false, which disallows all devices for the user
    to authenticate or sign the request. To solve this either remove both parameters or set at least one of these
    parameters to true.
    """


class InsufficientDataForMeaningfulAnswerError(GrandIDError):
    """
    Insufficient data

    If you have sent parameters thisDevice, deviceChoice as false also mobileBankId to false while sending no personal
    number, then you will get this message since there will be nothing to do!?
    """


class BankIDMessageError(GrandIDError):
    """
    When requesting an answer from BankID when using the gui=false parameter, the messages are directly forwarded from
    BankID to allow developers the same access to data as we do. Thus the responses are identical to the ones referenced
    in BankID documentation
    """

    msg: Dict = None

    def __init__(self, message: str, msg: Dict):
        super().__init__(message)
        self.msg = msg


class BankIDMessagePendingError(BankIDMessageError):
    pass


class BankIDMessageUserSignError(BankIDMessagePendingError):
    pass


class BankIDOutstandingTransactionError(BankIDMessagePendingError):
    pass


_ERROR_CODE_TO_CLASS = {
    "INCORRECT_URL_DATA": IncorrectURLDataError,
    "INCORRECT_SSN": IncorrectSSNError,
    "BANKID_INCORRECT_DATA": BankIDIncorrectDataError,
    "INCORRECT_SIGN_DATA": IncorrectSignDataError,
    "BANKID_ERROR": BankIDError,
    "BANKID_SIGN_NOT_ALLOWED": BankIDSignNotAllowedError,
    "BANKID_SIGN_USER_VISIBLE_SIZE": BankIDSignUserVisibleSizeError,
    "BANKID_SIGN_USER_NONVISIBLE_SIZE": BankIDSignUserNonvisibleSizeError,
    "INVALID_CERTIFICATE_POLICY": InvalidCertificatePolicyError,
    "INSUFFICIENT_DATA_FOR_MEANINGFUL_ANSWER": InsufficientDataForMeaningfulAnswerError,
    "BANKID_MSG": get_bankid_message_error,
}

_BANKID_MSG_CODE_TO_CLASS = {
    "outstandingTransaction": BankIDOutstandingTransactionError,
    "userSign": BankIDMessageUserSignError,
}
