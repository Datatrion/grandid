import base64
import logging

import requests
import six

from grandid.exceptions import get_error_class

logger = logging.getLogger(__name__)


class GrandIDClient(object):
    """
    :param apikey:
    :type apikey: str
    :param authenticateservicekey:
    :type authenticateservicekey: str
    :param test_server: Use the test server for authenticating and signing.
    :type test_server: bool
    :param request_timeout: Timeout for requests.
    :type request_timeout: int
    """

    def __init__(
            self, apikey: str, authenticateservicekey: str, test_server: bool = False, request_timeout: int = None
    ):
        self.apikey = apikey
        self.authenticateservicekey = authenticateservicekey
        self._request_timeout = request_timeout

        logger.debug("apikey %s", self.apikey)
        logger.debug("authenticateservicekey %s", self.authenticateservicekey)

        if test_server:
            self.api_url = "https://client-test.grandid.com/json1.1"
        else:
            self.api_url = "https://client.grandid.com/json1.1"

        self.client = requests.Session()
        self.client.headers = {"Content-Type": "application/json"}

        self._federatedlogin_endpoint = f"{self.api_url}/FederatedLogin"
        self._getsession_endpoint = f"{self.api_url}/GetSession"
        self._logout_endpoint = f"{self.api_url}/Logout"

    def _post(self, endpoint, json, *args, **kwargs):
        """Internal helper method for adding keys and timeout to requests."""
        params = {"apiKey": self.apikey, "authenticateServiceKey": self.authenticateservicekey}
        logger.debug("params %s", params)
        logger.debug("json %s", json)
        return self.client.post(endpoint, *args, timeout=self._request_timeout, params=params, json=json, **kwargs)

    def _get(self, endpoint, params, *args, **kwargs):
        """Internal helper method for adding keys and timeout to requests."""
        params.update({"apiKey": self.apikey, "authenticateServiceKey": self.authenticateservicekey})
        logger.debug("params %s", params)
        return self.client.get(endpoint, *args, timeout=self._request_timeout, params=params, **kwargs)

    def _federated_login(self, **data):
        logger.debug("data %s", data)
        response = self._post(self._federatedlogin_endpoint, json=data)

        if response.status_code == 200:
            return response.json()
        else:
            raise get_error_class(response)

    def _get_session(self, sessionId: str):
        response = self._get(self._federatedlogin_endpoint, params={"sessionId": sessionId})

        if response.status_code == 200:
            return response.json()
        else:
            raise get_error_class(response)

    def authenticate(self, **kwargs):
        raise NotImplementedError()

    def sign(self, user_visible_data, **kwargs):
        raise NotImplementedError()

    def collect(self, sessionId: str):
        self._get_session(sessionId)

    def logout(self, sessionId: str):
        response = self._get(self._federatedlogin_endpoint, params={"sessionId": sessionId})

        if response.status_code == 200:
            return response.json()
        else:
            raise get_error_class(response)

    def _encode_user_data(self, user_data):
        if isinstance(user_data, six.text_type):
            return base64.b64encode(user_data.encode("utf-8")).decode("ascii")
        else:
            return base64.b64encode(user_data).decode("ascii")


class BankIDClient(GrandIDClient):
    def authenticate(
            self,
            callbackUrl: str = None,
            personalNumber: str = None,
            mobileBankId: bool = False,
            desktopBankId: bool = False,
            thisDevice: bool = False,
            deviceChoice: bool = False,
            askForSSN: bool = False,
            gui: bool = True,
            qr: bool = False,
            customerURL: str = None,
            appRedirect: str = None,
            allowFingerprintSign: bool = False,
    ):
        return self._federated_login(
            callbackUrl=callbackUrl,
            personalNumber=personalNumber,
            mobileBankId=mobileBankId,
            desktopBankId=desktopBankId,
            thisDevice=thisDevice,
            deviceChoice=deviceChoice,
            askForSSN=askForSSN,
            gui=gui,
            qr=qr,
            customerURL=customerURL,
            appRedirect=appRedirect,
            allowFingerprintSign=allowFingerprintSign,
        )

    def sign(
            self,
            userVisibleData: str,
            callbackUrl: str = None,
            personalNumber: str = None,
            userNonVisibleData: str = None,
            mobileBankId: bool = False,
            desktopBankId: bool = False,
            thisDevice: bool = False,
            deviceChoice: bool = False,
            askForSSN: bool = False,
            gui: bool = True,
            qr: bool = False,
            customerURL: str = None,
            appRedirect: str = None,
            allowFingerprintSign: bool = False,
    ):
        userVisibleData = self._encode_user_data(userVisibleData)
        if userNonVisibleData:
            userNonVisibleData = self._encode_user_data(userNonVisibleData)
        return self._federated_login(
            callbackUrl=callbackUrl,
            personalNumber=personalNumber,
            userVisibleData=userVisibleData,
            userNonVisibleData=userNonVisibleData,
            mobileBankId=mobileBankId,
            desktopBankId=desktopBankId,
            thisDevice=thisDevice,
            deviceChoice=deviceChoice,
            askForSSN=askForSSN,
            gui=gui,
            qr=qr,
            customerURL=customerURL,
            appRedirect=appRedirect,
            allowFingerprintSign=allowFingerprintSign,
        )

    def logout(self, sessionId: str, cancelBankID: bool = False):
        response = self._get(
            self._federatedlogin_endpoint, params={"sessionId": sessionId, "cancelBankID": str(cancelBankID).lower()}
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise get_error_class(response)


class NetIDAccsessClient(GrandIDClient):
    def authenticate(
            self,
            callbackUrl: str = None,
            personalNumber: str = None,
            thisDevice: bool = False,
            appRedirect: str = None,
            gui: bool = True,
    ):
        return self._federated_login(
            callbackUrl=callbackUrl,
            personalNumber=personalNumber,
            thisDevice=thisDevice,
            appRedirect=appRedirect,
            gui=gui,
        )

    def sign(
            self,
            userVisibleData: str,
            callbackUrl: str = None,
            userNonVisibleData: str = None,
            personalNumber: str = None,
            thisDevice: bool = False,
            appRedirect: str = None,
            gui: bool = True,
    ):
        userVisibleData = self._encode_user_data(userVisibleData)
        if userNonVisibleData:
            userNonVisibleData = self._encode_user_data(userNonVisibleData)
        return self._federated_login(
            callbackUrl=callbackUrl,
            userVisibleData=userVisibleData,
            userNonVisibleData=userNonVisibleData,
            personalNumber=personalNumber,
            thisDevice=thisDevice,
            appRedirect=appRedirect,
            gui=gui,
        )


class NetiDEnterpriseClient(GrandIDClient):
    def authenticate(self):
        return self._federated_login()

    def sign(self, user_visible_data, **kwargs):
        raise NotImplementedError("Net iD Enterprise does not support signing")
