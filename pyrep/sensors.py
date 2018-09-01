from .vrep import vrep as v
from .vrep import vrepConst as vc
from .common import NotFoundComponentError, ReturnCommandError
from .common import Coordinates, EulerAngles

class ProximitySensor:

    def __init__(self, id, handle):
        self._id = id
        self._handle = handle
        self._def_op_mode = v.simx_opmode_oneshot_wait

    def read(self) -> (bool, Coordinates):
        """
        Reads the state of a proximity sensor.
        @return detection state and detected point
        @rtype (bool, Coordinates)
        """
        code, state, point, handle, snv = v.simxReadProximitySensor(
            self._id, self._handle, self._def_op_mode)
        if code == vc.simx_return_ok:
            return state, Coordinates(point[0], point[1], point[2])
        else:
            raise ReturnCommandError(code)


class VisionSensor:

    def __init__(self, id, handle):
        self._id = id
        self._handle = handle
        self._def_op_mode = v.simx_opmode_oneshot_wait

    def read(self):
        code, state, aux_packets = v.simxReadVisionSensor(
            self._id, self._handle, self._def_op_mode)
        if code == vc.simx_return_ok:
            return state, aux_packets
        else:
            raise ReturnCommandError(code)

    def raw_image(self, is_grey_scale=False):
        """
        Retrieves the image of a vision sensor.
        @return the image data
        """
        num_of_clr = 3
        if is_grey_scale:
            num_of_clr = 1

        code, resolution, image = v.simxGetVisionSensorImage(
            self._id, self._handle, int(is_grey_scale), self._def_op_mode)
        if code == vc.simx_return_ok:
            return image
        else:
            raise ReturnCommandError(code)


    def depth_buffer(self):
        """
        Retrieves the depth buffer of a vision sensor.
        """
        code, resolution, buffer = v.simxGetVisionSensorDepthBuffer(
            self._id, self._handle, self._def_op_mode)
        if code == vc.simx_return_ok:
            return buffer
        else:
            raise ReturnCommandError(code)


class ForceSensor:

    def __init__(self, id, handle):
        self._id = id
        self._handle = handle
        self._def_op_mode = v.simx_opmode_oneshot_wait

    def read(self) -> (bool, Coordinates, Coordinates):
        """
        Reads the force and torque applied to a force sensor
        (filtered values are read), and its current state ('unbroken' or 'broken').
        """
        code, state, force, torque = v.simxReadForceSensor(
            self._id, self._handle, self._def_op_mode)
        force_vector = Coordinates(force[0], force[1], force[2])
        torque_vector = Coordinates(torque[0], torque[1], torque[2])
        if code == vc.simx_return_ok:
            return state, force_vector, torque_vector
        else:
            raise ReturnCommandError(code)


class PositionSensor:

    def __init__(self, id, handle):
        self._id = id
        self._handle = handle
        self._def_op_mode = v.simx_opmode_oneshot_wait

    def get_position(self) -> Coordinates:
        """Retrieves the orientation.
        @rtype: Coordinates
        """
        code, pos = v.simxGetObjectPosition(self._id, self._handle, -1, self._def_op_mode)
        if code == vc.simx_return_ok:
            return Coordinates(pos[0], pos[1], pos[2])
        else:
            raise ReturnCommandError(code)

    def get_orientation(self) -> EulerAngles:
        """
        Retrieves the linear and angular velocity.
        @rtype EulerAngles
        """
        code, orient = v.simxGetObjectOrientation(self._id, self._handle, -1, self._def_op_mode)
        if code == vc.simx_return_ok:
            return EulerAngles(orient[0], orient[1], orient[2])
        else:
            raise ReturnCommandError(code)

    def get_velocity(self) -> (Coordinates, EulerAngles):
        """
        Retrieves the linear and angular velocity.
        @rtype (Coordinates, EulerAngles)
        """
        code, lin_vel, ang_vel = v.simxGetObjectVelocity(self._id, self._handle, self._def_op_mode)
        linear_velocity = Coordinates(lin_vel[0], lin_vel[1], lin_vel[2])
        angular_velocity = EulerAngles(ang_vel[0], ang_vel[1], ang_vel[2])
        if code == vc.simx_return_ok:
            return linear_velocity, angular_velocity
        else:
            raise ReturnCommandError(code)


class Sensors:

    def __init__(self, id):
        self._id = id
        self._def_op_mode = v.simx_opmode_oneshot_wait

    def proximity(self, name: str) -> ProximitySensor:
        handle = self._get_object_handle(name)
        return ProximitySensor(self._id, handle)

    def position(self, name: str) -> PositionSensor:
        handle = self._get_object_handle(name)
        return PositionSensor(self._id, handle)

    def vision(self, name: str) -> VisionSensor:
        handle = self._get_object_handle(name)
        return VisionSensor(self._id, handle)

    def force(self, name: str) -> ForceSensor:
        handle = self._get_object_handle(name)
        return ForceSensor(self._id, handle)

    def _get_object_handle(self, name):
        code, handle = v.simxGetObjectHandle(self._id, name, self._def_op_mode)
        if code == v.simx_return_ok:
            return handle
        else:
            raise NotFoundComponentError(name, code)
