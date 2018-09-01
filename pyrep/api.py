from .vrep import vrep as v
from .common import ReturnCommandError
from .joints import Joints
from .sensors import Sensors
from .simulation import Simulation

class VRepApi:
    def __init__(self, id):
        self._id = id
        self._def_op_mode = v.simx_opmode_oneshot_wait
        self.joint = Joints(id)  # type: Joints
        self.sensor = Sensors(id)  # type: Sensors
        self.simulation = Simulation(id)  # type: Simulation

    @staticmethod
    def connect(ip, port):
        id = v.simxStart(
            connectionAddress=ip,
            connectionPort=port,
            waitUntilConnected=True,
            doNotReconnectOnceDisconnected=True,
            timeOutInMs=5000,
            commThreadCycleInMs=5)
        if id == -1:
            raise Exception("Could not connect")
        else:
            return VRepApi(id)

    def close_connection(self):
        v.simxFinish(self._id)

    def __enter__(self):
        self.simulation.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.simulation.stop()
        self.close_connection()




