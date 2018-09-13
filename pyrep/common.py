import math
from .vrep import vrep as v

class Coordinates:

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def distance(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __str__(self):
        return "(x={0}, y={1}, z={2})"\
               .format(str(self.x), str(self.y), str(self.z))

    def __repr__(self):
        return self.__str__()


class EulerAngles:

    def __init__(self, alpha=0, beta=0, gamma=0):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def __str__(self):
        return "(alpha={0}, beta={1}, gamma={2})"\
               .format(str(self.alpha), str(self.beta), str(self.gamma))

    def __repr__(self):
        return self.__str__()


class NotFoundComponentError(Exception):
    def __init__(self, name, code):
        super(NotFoundComponentError, self).__init__(
            "Component with name \"" + name + "\" was not found. Error code:" + str(code))


class MatchObjTypeError(Exception):

    def __init__(self, name):
        super(MatchObjTypeError, self).__init__(
            "Component with name: \"" + name + "\" does not fit the parameters.")


class ReturnCommandError(Exception):

    def __init__(self, code):
        msg = ""
        if code == v.simx_return_novalue_flag:
            msg = "There is no command reply in the input buffer. This should not always be considered as an error, depending on the selected operation mode"
        elif code == v.simx_return_timeout_flag:
            msg = "The function timed out (probably the network is down or too slow)"
        elif code == v.simx_return_illegal_opmode_flag:
            msg = "The specified operation mode is not supported for the given function"
        elif code == v.simx_return_remote_error_flag:
            msg = "The function caused an error on the server side (e.g. an invalid handle was specified)"
        elif code == v.simx_return_split_progress_flag:
            msg = "The communication thread is still processing previous split command of the same type"
        elif code == v.simx_return_local_error_flag:
            msg = "The function caused an error on the client side"
        elif code == v.simx_return_initialize_error_flag:
            msg = "simxStart was not yet called"
        elif code == v.simx_return_ok:
            msg = "The function executed fine, why is this an exception?"
        else:
            msg = "Undefined return code: " + str(code)
        super(ReturnCommandError, self).__init__(msg)
