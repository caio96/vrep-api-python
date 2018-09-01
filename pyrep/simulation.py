from .vrep import vrep as v
from .vrep import vrepConst as vc
from .common import ReturnCommandError

class Simulation:

    def __init__(self, id):
        self._id = id
        self._def_op_mode = v.simx_opmode_oneshot_wait

    def start(self):
        code = v.simxStartSimulation(self._id, self._def_op_mode)
        if code != vc.simx_return_ok:
            raise ReturnCommandError(code)

    def resume(self):
        code = v.simxPauseSimulation(self._id, self._def_op_mode)
        if code != vc.simx_return_ok:
            raise ReturnCommandError(code)

    def pause(self):
        code = v.simxPauseSimulation(self._id, self._def_op_mode)
        if code != vc.simx_return_ok:
            raise ReturnCommandError(code)

    def stop(self):
        code = v.simxStopSimulation(self._id, self._def_op_mode)
        if code != vc.simx_return_ok:
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
        else:
            raise ReturnCommandError(code)

    def last_cmd_time(self):
        time = v.simxGetLastCmdTime(self._id)
        return time