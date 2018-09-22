from .vrep import vrep as v
from .joints import Joints
from .sensors import Sensors
from .simulation import Simulation

class VRepApi:
    def __init__(self, client_id):
        self._id = client_id
        self.joint = Joints(client_id)  # type: Joints
        self.sensor = Sensors(client_id)  # type: Sensors
        self.simulation = Simulation(client_id)  # type: Simulation

    @staticmethod
    def connect(ip, port):
        client_id = v.simxStart(
            connectionAddress=ip,
            connectionPort=port,
            waitUntilConnected=True,
            doNotReconnectOnceDisconnected=True,
            timeOutInMs=5000,
            commThreadCycleInMs=5)
        if client_id == -1:
            raise Exception("Could not connect")
        else:
            return VRepApi(client_id)

    def close_connection(self):
        v.simxFinish(self._id)

    def __enter__(self):
        self.simulation.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.simulation.stop()
        self.close_connection()
