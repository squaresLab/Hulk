#
# TODO use metaprogramming to reduce the amount of boilerplate
#
from typing import Any, Dict, Tuple

import flask

__ALL__ = [
    'HulkException',
    'ServerError',
    'OperatorNameAlreadyExists',
    'LanguageNotFound',
    'BadConfigFile',
    'IllegalConfig'
]


class HulkException(Exception):
    """
    Base class for all exceptions produced by Hulk.
    """
    def __init__(self, message: str) -> None:
        self.__message = message
        super().__init__(message)

    @property
    def message(self):
        """
        A short description of the error.
        """
        return self.__message


class ClientServerError(HulkException):
    """
    Base class for all exceptions that may be thrown from the server to the
    client. Provides the necessary machinery to write/read errors to/from
    JSON descriptions.
    """
    @staticmethod
    def from_dict(d: dict) -> 'HulkException':
        assert 'error' in d
        d = d['error']

        assert 'kind' in d

        # TODO use metaprogramming to avoid having to maintain this list
        cls = ({
            'OperatorNameAlreadyExists': OperatorNameAlreadyExists,
            'LanguageNotFound': LanguageNotFound,
            'BadConfigFile': BadConfigFile,
            'IllegalConfig': IllegalConfig
        })[d]

        return cls.from_data(d.get('data', {}))

    def __init__(self, status_code: int, message: str) -> None:
        self.__status_code = status_code
        super().__init__(message)

    @property
    def status_code(self) -> int:
        """
        The status code that was produced by the server when this error was
        reported to the client.
        """
        return self.__status_code

    def to_response(self, data: Dict[str, Any] = None) -> Tuple[Any, int]:
        """
        Transforms this exception into a HTTP response containing a
        machine-readable description of the exception.
        """
        jsn = {
            'kind': self.__class__.__name__,
            'message': self.message
        }
        if data:
            jsn['data'] = data
        jsn = {'error': jsn}
        return jsn, self.__status_code


class OperatorNameAlreadyExists(ClientServerError):
    """
    Used to indicate that a given operator name is already in use by another
    operator.
    """
    @staticmethod
    def from_data(data: dict) -> 'OperatorNameAlreadyExists':
        assert 'name' in data
        return OperatorNameAlreadyExists(data['name'])

    def __init__(self,
                 name: str,
                 *,
                 status_code: int = 409
                 ) -> None:
        self.__name = name
        msg = "operator name is already in use: {}".format(name)
        super().__init__(msg, status_code)

    @property
    def name(self) -> str:
        """
        The name of the requested operator.
        """
        return self.__name

    def to_response(self) -> Tuple[Any, int]:
        return super().to_response(data={'name': self.name})


class LanguageNotFound(ClientServerError):
    """
    Used to indicate that there exists no language registered under a given
    name.
    """
    @staticmethod
    def from_data(data: dict) -> 'LanguageNotFound':
        assert 'name' in data
        return LanguageNotFound(data['name'])

    def __init__(self,
                 name: str,
                 *,
                 status_code: int = 404
                 ) -> None:
        self.__name = name
        msg = "no language registered with name: {}".format(name)
        super().__init__(status_code, msg)

    @property
    def name(self) -> str:
        """
        The name of the requested language.
        """
        return self.__name

    def to_response(self) -> Tuple[Any, int]:
        return super().to_response(data={'name': self.name})


class OperatorNotFound(ClientServerError):
    """
    Used to indicate that no operator has been registered under a given name.
    """
    @staticmethod
    def from_data(data: dict) -> 'OperatorNotFound':
        assert 'name' in data
        return OperatorNotFound(data['name'])

    def __init__(self,
                 name: str,
                 *,
                 status_code: int = 404
                 ) -> None:
        self.__name = name
        msg = "no operator registered with name: {}".format(name)
        super().__init__(status_code, msg)

    @property
    def name(self) -> str:
        """
        The name of the requested language.
        """
        return self.__name

    def to_response(self) -> Tuple[Any, int]:
        return super().to_response(data={'name': self.name})


class SnapshotNotFound(ClientServerError):
    """
    Used to indicate that no snapshot was found with the given name on the
    attached BugZoo server.
    """
    @staticmethod
    def from_data(data: dict) -> 'SnapshotNotFound':
        assert 'name' in data
        return SnapshotNotFound(data['name'])

    def __init__(self,
                 name: str,
                 *,
                 status_code: int = 404
                 ) -> None:
        self.__name = name
        msg = "no BugZoo snapshot registered with name: {}".format(name)
        super().__init__(status_code, msg)

    @property
    def name(self) -> str:
        """
        The name of the requested snapshot.
        """
        return self.__name

    def to_response(self) -> Tuple[Any, int]:
        return super().to_response(data={'name': self.name})


class FileNotFound(ClientServerError):
    """
    Used to indicate that the requested file was not found.
    """
    @staticmethod
    def from_data(data: dict) -> 'FileNotFound':
        assert 'name' in data
        return FileNotFound(data['name'])

    def __init__(self,
                 name: str,
                 *,
                 status_code: int = 404
                 ) -> None:
        self.__name = name
        msg = "file not found: {}".format(name)
        super().__init__(status_code, msg)

    @property
    def name(self) -> str:
        """
        The name of the missing file.
        """
        return self.__name

    def to_response(self) -> Tuple[Any, int]:
        return super().to_response(data={'name': self.name})


class BadConfigFile(HulkException):
    """
    Used to indicate that a given configuration file is ill-formed.
    """
    def __init__(self, reason: str) -> None:
        super().__init__(reason)


class IllegalConfig(HulkException):
    """
    Used to indicate that a given configuration is syntatically correct but
    that it describes an illegal configuration.
    """
    def __init__(self, reason: str) -> None:
        super().__init__(reason)
