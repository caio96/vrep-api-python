from .vrep import vrep as v
from .vrep import vrepConst as vc
from .common import NotFoundComponentError, MatchObjTypeError, ReturnCommandError

class AnyJoint:
    def __init__(self, client_id, handle, low_limit, joint_range):
        self._id = client_id
        self._handle = handle
        self._low_limit = low_limit
        self._range = joint_range

    def get_low_limit(self):
        return self._low_limit

    def get_range(self):
        return self._range

    def get_force(self, op_mode=None):
        if op_mode is None:
            op_mode = vc.simx_opmode_streaming
        code, force = v.simxGetJointForce(
            self._id, self._handle, op_mode)
        if code == v.simx_return_ok:
            return force
        elif code == v.simx_return_novalue_flag:
            return None
        raise ReturnCommandError(code)

    def get_matrix(self, op_mode=None):
        if op_mode is None:
            op_mode = vc.simx_opmode_streaming
        code, matrix = v.simxGetJointMatrix(
            self._id, self._handle, op_mode)
        if code == v.simx_return_ok:
            return matrix
        elif code == v.simx_return_novalue_flag:
            return None
        raise ReturnCommandError(code)

    def get_position(self, op_mode=None):
        if op_mode is None:
            op_mode = vc.simx_opmode_streaming
        code, position = v.simxGetJointPosition(
            self._id, self._handle, op_mode)
        if code == v.simx_return_ok:
            return position
        elif code == v.simx_return_novalue_flag:
            return None
        raise ReturnCommandError(code)

    def set_maximum_force(self, force, op_mode=None):
        if op_mode is None:
            op_mode = vc.simx_opmode_oneshot
        code = v.simxSetJointForce(
            self._id, self._handle, force, op_mode)
        if code not in (v.simx_return_ok, v.simx_return_novalue_flag):
            raise ReturnCommandError(code)

    def set_position(self, position, op_mode=None):
        if op_mode is None:
            op_mode = vc.simx_opmode_streaming
        code = v.simxSetJointPosition(
            self._id, self._handle, position, op_mode)
        if code not in (v.simx_return_ok, v.simx_return_novalue_flag):
            raise ReturnCommandError(code)

    def set_target_position(self, target, op_mode=None):
        if op_mode is None:
            op_mode = vc.simx_opmode_streaming
        code = v.simxSetJointTargetPosition(
            self._id, self._handle, target, op_mode)
        if code not in (v.simx_return_ok, v.simx_return_novalue_flag):
            raise ReturnCommandError(code)

    def set_target_velocity(self, target, op_mode=None):
        if op_mode is None:
            op_mode = vc.simx_opmode_streaming
        code = v.simxSetJointTargetVelocity(
            self._id, self._handle, target, op_mode)
        if code not in (v.simx_return_ok, v.simx_return_novalue_flag):
            raise ReturnCommandError(code)

    def set_matrix(self, matrix, op_mode=None):
        if op_mode is None:
            op_mode = vc.simx_opmode_streaming
        assert len(matrix) == 12
        code = v.simxSetSphericalJointMatrix(
            self._id, self._handle, matrix, op_mode)
        if code not in (v.simx_return_ok, v.simx_return_novalue_flag):
            raise ReturnCommandError(code)


class JointWithVelocityControl:

    def __init__(self, any_joint: AnyJoint):
        self._any_joint = any_joint

    def set_target_velocity(self, target: float, op_mode=None):
        self._any_joint.set_target_velocity(target, op_mode)

    def set_maximum_force(self, force: float, op_mode=None):
        self._any_joint.set_maximum_force(force, op_mode)

    def get_position(self, op_mode=None):
        return self._any_joint.get_position(op_mode)

    def get_force(self, op_mode=None):
        return self._any_joint.get_force(op_mode)


class JointWithPositionControl:

    def __init__(self, any_joint: AnyJoint):
        self._any_joint = any_joint

    def set_target_position(self, target: float, op_mode=None):
        self._any_joint.set_target_position(target, op_mode)

    def set_maximum_force(self, force: float, op_mode=None):
        self._any_joint.set_maximum_force(force, op_mode)

    def get_position(self, op_mode=None):
        return self._any_joint.get_position(op_mode)

    def get_force(self, op_mode=None):
        return self._any_joint.get_force(op_mode)


class PassiveJoint:

    def __init__(self, any_joint: AnyJoint):
        self._any_joint = any_joint

    def get_position(self, op_mode=None):
        return self._any_joint.get_position(op_mode)

    def set_position(self, pos: float, op_mode=None):
        self._any_joint.set_position(pos, op_mode)


class SphericalJoint:

    def __init__(self, any_joint: AnyJoint):
        self._any_joint = any_joint

    def set_matrix(self, matrix, op_mode=None):
        self._any_joint.set_matrix(matrix, op_mode)

    def get_matrix(self, op_mode=None):
        return self._any_joint.get_matrix(op_mode)


class SpringJoint:

    def __init__(self, any_joint: AnyJoint):
        self._any_joint = any_joint

    def set_target_position(self, target: float, op_mode=None):
        self._any_joint.set_target_position(target, op_mode)

    def set_maximum_force(self, force: float, op_mode=None):
        self._any_joint.set_maximum_force(force, op_mode)

    def get_position(self, op_mode=None):
        return self._any_joint.get_position(op_mode)

    def get_force(self, op_mode=None):
        return self._any_joint.get_force(op_mode)

    def set_target_velocity(self, target: float, op_mode=None):
        self._any_joint.set_target_velocity(target, op_mode)


class Joints:

    def __init__(self, client_id):
        self._id = client_id

    def spherical(self, name: str) -> SphericalJoint:
        """
        Retrieves the joint with next parameters:
            * Joint type: Spherical
            * Joint mode: Passive
        """
        joint = self._get_joint_with_param(
            name,
            [vc.sim_joint_spherical_subtype],
            vc.sim_jointmode_passive)
        return SphericalJoint(joint)

    def spring(self, name: str) -> SpringJoint:
        """
        Retrieves the joint with next parameters:
            * Joint type: Revolute or Prismatic
            * Joint mode: Force
            * Motor enabled: True
            * Control loop enabled: True
            * Spring-damper mode
        """
        joint = self._get_joint_with_param(
            name, [vc.sim_joint_revolute_subtype, vc.sim_joint_prismatic_subtype],
            vc.sim_jointmode_force)
        return SpringJoint(joint)

    def passive(self, name: str) -> PassiveJoint:
        """
        Retrieves the joint (kinematic mode)with next parameters:
            * Joint type: Revolute or Prismatic
            * Joint mode: Passive
        """
        joint = self._get_joint_with_param(
            name, [vc.sim_joint_revolute_subtype, vc.sim_joint_prismatic_subtype],
            vc.sim_jointmode_passive)
        return PassiveJoint(joint)

    def with_position_control(self, name: str) -> JointWithPositionControl:
        """
        Retrieves the joint (like servo) with next parameters:
            * Joint type: Revolute or Prismatic
            * Joint mode: Force
            * Motor Enabled: True
            * Control loop enabled: True
            * Position control (PID)
        """
        joint = self._get_joint_with_param(
            name, [vc.sim_joint_revolute_subtype, vc.sim_joint_prismatic_subtype],
            vc.sim_jointmode_force)
        return JointWithPositionControl(joint)

    def with_velocity_control(self, name: str) -> JointWithVelocityControl:
        """
        Retrieves the joint (like DC motor) with next parameters:
            * Joint type: Revolute or Prismatic
            * Joint mode: Force
            * Motor Enabled: True
        """
        joint = self._get_joint_with_param(
            name, [vc.sim_joint_revolute_subtype, vc.sim_joint_prismatic_subtype],
            vc.sim_jointmode_force)
        return JointWithVelocityControl(joint)

    def _get_joint_with_param(self, name, types, joint_mode) -> AnyJoint:
        handle = self._get_object_handle(name)
        joint_type, curr_mode, low_limit, joint_range = self._get_info_about_joint(handle)
        if joint_type in types and curr_mode == joint_mode:
            return AnyJoint(self._id, handle, low_limit, joint_range)
        raise MatchObjTypeError(name)

    def _get_info_about_joint(self, handle):
        obj_type_code = vc.sim_object_joint_type
        # 16: retrieves joint properties data
        # in intData (2 values): joint type, joint mode (bit16=hybid operation
        # In floatData (2 values): joint limit low, joint range (-1.0 if joint is cyclic)
        data_type_code = 16
        code, handles, types_and_mode, limits_and_ranges, _ = v.simxGetObjectGroupData(
            self._id, obj_type_code, data_type_code, vc.simx_opmode_oneshot_wait)
        if code == v.simx_return_ok:
            index = handles.index(handle)
            index = index * 2
            return types_and_mode[index], types_and_mode[index+1], limits_and_ranges[index], limits_and_ranges[index+1]
        raise ReturnCommandError(code)

    def _get_object_handle(self, name):
        code, handle = v.simxGetObjectHandle(self._id, name, vc.simx_opmode_oneshot_wait)
        if code == v.simx_return_ok:
            return handle
        raise NotFoundComponentError(name, code)
