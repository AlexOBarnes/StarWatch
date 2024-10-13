'''This module contains the API error class'''

class APIError(Exception):
    """Describes an error triggered by a failing API call."""

    def __init__(self, message: str, code: int = 500):
        """Creates a new APIError instance."""
        self.code = code
        self._message = message
        super().__init__(self.message)
        self.define_error()

    @property
    def message(self):
        '''Getter for message of APIError class'''
        return self._message

    @message.setter
    def message(self, new_message):
        '''Setter for the message property of the APIError class'''
        self._message = f"{self._message}: {new_message}"

    def define_error(self):
        '''Returns the associated error message to the status code'''
        error_messages = {
            400: "Bad Request: The server could not understand the request.",
            401: "Unauthorized: Authentication is required and has failed.",
            403: "Forbidden: You do not have permission to access this resource.",
            404: "Not Found: The requested resource could not be found.",
            405: "Method Not Allowed: The request method is not supported for this resource.",
            408: "Request Timeout: The server timed out waiting for the request.",
            429: "Too Many Requests: You have sent too many requests in a given amount of time.",
            500: "Internal Server Error: The server encountered an unexpected condition.",
            502: "Bad Gateway: The server received an invalid response from the upstream server.",
            503: "Service Unavailable: The server is currently unable to handle the request.",
            504: "Gateway Timeout: The server did not respond in a timely manner."}

        self._message = f"APIError: {error_messages.get(
            self.code, 'Unknown error code')} (HTTP {self.code})"
