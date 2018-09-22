import numpy as np
from .vrep import vrep as v
from .vrep import vrepConst as vc
from .common import NotFoundComponentError, ReturnCommandError
from .common import Coordinates, EulerAngles

class ProximitySensor:

    def __init__(self, client_id, handle):
        self._id = client_id
        self._handle = handle

    def read(self) -> (bool, Coordinates):
        """
        Reads the state of a proximity sensor.
        @return detection state and detected point
        @rtype (bool, Coordinates)
        """
        code, state, point, _, _ = v.simxReadProximitySensor(
            self._id, self._handle, vc.simx_opmode_streaming)
        if code == vc.simx_return_ok or code == vc.simx_return_novalue_flag:
            return state, Coordinates(point[0], point[1], point[2])
        raise ReturnCommandError(code)


class VisionSensor:

    def __init__(self, client_id, handle):
        self._id = client_id
        self._handle = handle

    def read(self):
        code, state, aux_packets = v.simxReadVisionSensor(
            self._id, self._handle, vc.simx_opmode_streaming)
        if code == vc.simx_return_ok or code == vc.simx_return_novalue_flag:
            return state, aux_packets
        raise ReturnCommandError(code)

    def raw_image(self, is_grey_scale=False):
        """
        Retrieves the image of a vision sensor.
        @return the image as a numpy array
        """
        code, resolution, image_flat = v.simxGetVisionSensorImage(
            self._id, self._handle, int(is_grey_scale), vc.simx_opmode_streaming)
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

    def depth_buffer(self):
        """
        Retrieves the depth buffer of a vision sensor.
        """
        code, resolution, buffer = v.simxGetVisionSensorDepthBuffer(
            self._id, self._handle, vc.simx_opmode_streaming)
        if code == vc.simx_return_ok or code == vc.simx_return_novalue_flag:
            return buffer
        raise ReturnCommandError(code)


class ForceSensor:

    def __init__(self, client_id, handle):
        self._id = client_id
        self._handle = handle

    def read(self) -> (bool, Coordinates, Coordinates):
        """
        Reads the force and torque applied to a force sensor
        (filtered values are read), and its current state ('unbroken' or 'broken').
        """
        code, state, force, torque = v.simxReadForceSensor(
            self._id, self._handle, vc.simx_opmode_streaming)
        force_vector = Coordinates(force[0], force[1], force[2])
        torque_vector = Coordinates(torque[0], torque[1], torque[2])
        if code == vc.simx_return_ok or code == vc.simx_return_novalue_flag:
            return state, force_vector, torque_vector
        raise ReturnCommandError(code)


class GroundTruthSensor:

    def __init__(self, client_id, handle):
        self._id = client_id
        self._handle = handle

    def get_position(self) -> Coordinates:
        """Retrieves the orientation.
        @rtype: Coordinates
        """
        code, pos = v.simxGetObjectPosition(self._id, self._handle, -1, vc.simx_opmode_streaming)
        if code == vc.simx_return_ok or code == vc.simx_return_novalue_flag:
            return Coordinates(pos[0], pos[1], pos[2])
        raise ReturnCommandError(code)

    def get_orientation(self) -> EulerAngles:
        """
        Retrieves the linear and angular velocity.
        @rtype EulerAngles
        """
        code, orient = v.simxGetObjectOrientation(self._id, self._handle, -1, vc.simx_opmode_streaming)
        if code == vc.simx_return_ok or code == vc.simx_return_novalue_flag:
            return EulerAngles(orient[0], orient[1], orient[2])
        raise ReturnCommandError(code)

    def get_velocity(self) -> (Coordinates, EulerAngles):
        """
        Retrieves the linear and angular velocity.
        @rtype (Coordinates, EulerAngles)
        """
        code, lin_vel, ang_vel = v.simxGetObjectVelocity(self._id, self._handle, vc.simx_opmode_streaming)
        linear_velocity = Coordinates(lin_vel[0], lin_vel[1], lin_vel[2])
        angular_velocity = EulerAngles(ang_vel[0], ang_vel[1], ang_vel[2])
        if code == vc.simx_return_ok or code == vc.simx_return_novalue_flag:
            return linear_velocity, angular_velocity
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

    def _get_object_handle(self, name):
        code, handle = v.simxGetObjectHandle(self._id, name, vc.simx_opmode_oneshot_wait)
        if code == v.simx_return_ok:
            return handle
        raise NotFoundComponentError(name, code)
