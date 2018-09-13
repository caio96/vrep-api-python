from .vrep import vrep as v
from .vrep import vrepConst as vc
from .common import ReturnCommandError

class Simulation:

    def __init__(self, client_id):
        self._id = client_id

    def start(self):
        code = v.simxStartSimulation(self._id, vc.simx_opmode_oneshot_wait)
        if code != vc.simx_return_ok and code != vc.simx_return_novalue_flag:
            raise ReturnCommandError(code)

    def resume(self):
        code = v.simxPauseSimulation(self._id, vc.simx_opmode_oneshot_wait)
        if code != vc.simx_return_ok and code != vc.simx_return_novalue_flag:
            raise ReturnCommandError(code)

    def pause(self):
        code = v.simxPauseSimulation(self._id, vc.simx_opmode_oneshot_wait)
        if code != vc.simx_return_ok and code != vc.simx_return_novalue_flag:
            raise ReturnCommandError(code)

    def stop(self):
        code = v.simxStopSimulation(self._id, vc.simx_opmode_oneshot_wait)
        if code != vc.simx_return_ok and code != vc.simx_return_novalue_flag:
            raise ReturnCommandError(code)

    def resume_communication(self):
        code = v.simxPauseCommunication(self._id, False)
        if code != vc.simx_return_ok:
            raise ReturnCommandError(code)

    def pause_communication(self):
        code = v.simxPauseCommunication(self._id, True)
        if code != vc.simx_return_ok:
            raise ReturnCommandError(code)

    def ping_time(self):
        code, time = v.simxGetPingTime(self._id)
        if code == vc.simx_return_ok:
            return time
        raise ReturnCommandError(code)

    def last_cmd_time(self):
        time = v.simxGetLastCmdTime(self._id)
        return time
