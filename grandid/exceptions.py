def get_error_class(response):
    data = response.json()
    errorObject = data.get("errorObject")
    error_class = _ERROR_CODE_TO_CLASS.get(errorObject.get("errorCode"), GrandIDError)
    return error_class("{0}: {1}".format(data.get("errorCode"), data.get("details")))


class GrandIDError(Exception):
    """Parent exception class for all GrandID errors."""

    def __init__(self, *args, **kwargs):
        super(GrandIDError, self).__init__(*args, **kwargs)
        self.rfa = None


class GrandIDWarning(Warning):
    """Warning class for GrandID."""

    pass


# TODO: Make explicit classes for different errors
_ERROR_CODE_TO_CLASS = {}
