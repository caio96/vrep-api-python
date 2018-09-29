import numpy as np
from .vrep import vrep as v
from .vrep import vrepConst as vc
from .common import NotFoundComponentError, ReturnCommandError
from .common import Coordinates, EulerAngles

class ProximitySensor:

    def __init__(self, client_id, handle):
        self._id = client_id
        self._handle = handle

    def read(self, op_mode=None) -> (bool, int, Coordinates):
        """
        Reads the state of a proximity sensor.
        @return detection state and detected point
        @rtype (bool, int, Coordinates)
        """
        if op_mode is None:
            op_mode = vc.simx_opmode_streaming
        code, state, point, _, _ = v.simxReadProximitySensor(
            self._id, self._handle, op_mode)
        if code == vc.simx_return_ok:
            return state, Coordinates(point[0], point[1], point[2])
        elif code == vc.simx_return_novalue_flag:
            return None, None
        raise ReturnCommandError(code)


class VisionSensor:

    def __init__(self, client_id, handle):
        self._id = client_id
        self._handle = handle

    def read(self, op_mode=None):
        if op_mode is None:
            op_mode = vc.simx_opmode_streaming
        code, state, aux_packets = v.simxReadVisionSensor(
            self._id, self._handle, op_mode)
        if code == vc.simx_return_ok:
            return state, aux_packets
        elif code == vc.simx_return_novalue_flag:
            return None, None
        raise ReturnCommandError(code)

    def raw_image(self, is_grey_scale=False, op_mode=None):
        """
        Retrieves the image of a vision sensor.
        @return the image as a numpy array
        """
        if op_mode is None:
            op_mode = vc.simx_opmode_streaming
        code, resolution, image_flat = v.simxGetVisionSensorImage(
            self._id, self._handle, int(is_grey_scale), op_mode)
        if code == vc.simx_return_ok:
            image_flat = np.asarray(image_flat, dtype=np.uint8)
            if not is_grey_scale:
                resolution.append(3)
            image = image_flat.reshape(tuple(resolution))
            image = np.rot90(image, 2)
            return image
        elif code == vc.simx_return_novalue_flag:
            return None
        raise ReturnCommandError(code)

    def depth_buffer(self, op_mode=None):
        """
        Retrieves the depth buffer of a vision sensor.
        """
        if op_mode is None:
            op_mode = vc.simx_opmode_streaming
        code, resolution, buffer = v.simxGetVisionSensorDepthBuffer(
            self._id, self._handle, op_mode)
        if code == vc.simx_return_ok:
            return buffer
        elif code == vc.simx_return_novalue_flag:
            return None
        raise ReturnCommandError(code)


class ForceSensor:

    def __init__(self, client_id, handle):
        self._id = client_id
        self._handle = handle

    def read(self, op_mode=None) -> (bool, int, Coordinates, Coordinates):
        """
        Reads the force and torque applied to a force sensor
        (filtered values are read), and its current state ('unbroken' or 'broken').
        """
        if op_mode is None:
            op_mode = vc.simx_opmode_streaming
        code, state, force, torque = v.simxReadForceSensor(
            self._id, self._handle, op_mode)
        force_vector = Coordinates(force[0], force[1], force[2])
        torque_vector = Coordinates(torque[0], torque[1], torque[2])
        if code == vc.simx_return_ok:
            return state, force_vector, torque_vector
        elif code == vc.simx_return_novalue_flag:
            return None, None, None
        raise ReturnCommandError(code)


class GroundTruthSensor:

    def __init__(self, client_id, handle):
        self._id = client_id
        self._handle = handle

    def get_position(self, op_mode=None) -> Coordinates:
        """Retrieves the orientation.
        @rtype: Coordinates
        """
        if op_mode is None:
            op_mode = vc.simx_opmode_streaming
        code, pos = v.simxGetObjectPosition(self._id, self._handle, -1, op_mode)
        if code == vc.simx_return_ok:
            return Coordinates(pos[0], pos[1], pos[2])
        elif code == vc.simx_return_novalue_flag:
            return None
        raise ReturnCommandError(code)

    def get_orientation(self, op_mode=None) -> EulerAngles:
        """
        Retrieves the linear and angular velocity.
        @rtype EulerAngles
        """
        if op_mode is None:
            op_mode = vc.simx_opmode_streaming
        code, orient = v.simxGetObjectOrientation(self._id, self._handle, -1, op_mode)
        if code == vc.simx_return_ok:
            return EulerAngles(orient[0], orient[1], orient[2])
        elif code == vc.simx_return_novalue_flag:
            return None
        raise ReturnCommandError(code)

    def get_velocity(self, op_mode=None) -> (Coordinates, EulerAngles):
        """
        Retrieves the linear and angular velocity.
        @rtype (Coordinates, EulerAngles)
        """
        if op_mode is None:
            op_mode = vc.simx_opmode_streaming
        code, lin_vel, ang_vel = v.simxGetObjectVelocity(self._id, self._handle, op_mode)
        linear_velocity = Coordinates(lin_vel[0], lin_vel[1], lin_vel[2])
        angular_velocity = EulerAngles(ang_vel[0], ang_vel[1], ang_vel[2])
        if code == vc.simx_return_ok:
            return linear_velocity, angular_velocity
        elif code == vc.simx_return_novalue_flag:
            return None, None
        raise ReturnCommandError(code)


class LaserScanner2d:

    """
    Class for model '2d Laser Scanner.ttm'
    Add the following lines to the child script of the laser scanner:

    data=simPackFloats(points)
    simSetStringSignal("LaserScanner2dData", data)
    """

    def __init__(self, client_id, handle, signal_name=None):
        self._id = client_id
        self._handle = handle
        if signal_name is not None:
            self._signal_name = signal_name
        else:
            self._signal_name = "LaserScanner2dData"

    def read(self, op_mode=None):
        if op_mode is None:
            op_mode = vc.simx_opmode_streaming
        code, signal = v.simxGetStringSignal(self._id, self._signal_name, op_mode)
        if code == vc.simx_return_ok:
            readings = v.simxUnpackFloats(signal)
            points = []
            for i in range(0, len(readings), 3):
                points.append(Coordinates(readings[i], readings[i+1], readings[i+2]))
            return points
        elif code == vc.simx_return_novalue_flag:
            return None
        raise ReturnCommandError(code)


class Sensors:

    def __init__(self, client_id):
        self._id = client_id

    def proximity(self, name: str) -> ProximitySensor:
        handle = self._get_object_handle(name)
        return ProximitySensor(self._id, handle)

    def ground_truth(self, name: str) -> GroundTruthSensor:
        handle = self._get_object_handle(name)
        return GroundTruthSensor(self._id, handle)

    def vision(self, name: str) -> VisionSensor:
        handle = self._get_object_handle(name)
        return VisionSensor(self._id, handle)

    def force(self, name: str) -> ForceSensor:
        handle = self._get_object_handle(name)
        return ForceSensor(self._id, handle)

    def laser_scanner_2d(self, name: str, signal_name: str=None):
        handle = self._get_object_handle(name)
        return LaserScanner2d(self._id, handle, signal_name)

    def _get_object_handle(self, name):
        code, handle = v.simxGetObjectHandle(self._id, name, vc.simx_opmode_oneshot_wait)
        if code == v.simx_return_ok:
            return handle
        raise NotFoundComponentError(name, code)
