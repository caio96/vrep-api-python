# V-Rep API Python

Simple python binding for
[Coppelia Robotics V-REP simulator](http://www.coppeliarobotics.com/) ([remote API](http://www.coppeliarobotics.com/helpFiles/en/remoteApiOverview.htm)) of version 3.3.0

## Getting started

0. Requirements: CPython version >= 3.5.2, pip
1. Import this library locally by entering this command:
```python
from pyrep.api import VRepApi
```

## V-Rep specific
This package needs a platform-specific shared library (remoteApi). You can find it in `<V-Rep-Root>/programming/remoteApiBindings/lib/lib/Linux/64Bit/` and you need to copy it inside this repository to `./pyrep/vrep/`.

This setup was tested under **LINUX ONLY**.    
    * For windows users: *NOT TESTED*
    
This package also needs the socket port number, which can be located in `<V-Rep-Root>/remoteApiConnections.txt`.

Where `<V-Rep-Root>` is the root of V-Rep-Pro-Edu directory.

## Currently implemented things

The current version does not implement features such as remote management GUI,
additional configuration properties of objects and shapes, etc.
Implemented components:
* Joint
* Proximity sensor
* Vision sensor
* Force sensor
* Position sensor (used for that dummy or shape object)
* ~~Remote function calls~~

## Example
Designed to be used with `examples/Pioneer.ttt`.
```python
import time
import sys

sys.path.append("..")
from pyrep.api import VRepApi

class PioneerP3DX:

    def __init__(self, api: VRepApi):
        self._api = api
        self._ground_truth = api.sensor.ground_truth("Pioneer_p3dx")
        self._left_motor = api.joint.with_velocity_control("Pioneer_p3dx_leftMotor")
        self._right_motor = api.joint.with_velocity_control("Pioneer_p3dx_rightMotor")
        self._sonar_sensors = []
        for i in range(1, 17):
            self._sonar_sensors.append(api.sensor.proximity("Pioneer_p3dx_ultrasonicSensor" + str(i)))

    def rotate_right(self, speed=2.0):
        self._move(speed, -speed)

    def rotate_left(self, speed=2.0):
        self._move(-speed, speed)

    def move_forward(self, speed=2.0):
        self._move(speed, speed)

    def move_backward(self, speed=2.0):
        self._move(-speed, -speed)

    def _move(self, left: float, right: float):
        self._left_motor.set_target_velocity(left)
        self._right_motor.set_target_velocity(right)

    def sensor_distance(self, sensor_number: int):
        state, coordinate = self._sonar_sensors[sensor_number].read()
        if state == 0:
            return -1
        return coordinate.get_z()

    def get_position(self):
        return self._ground_truth.get_position()

# Example usage
if __name__ == "__main__":
    with VRepApi.connect("127.0.0.1", 19997) as api:
        pioneer = PioneerP3DX(api)
        while True:
            rl = pioneer.sensor_distance(6)
            ll = pioneer.sensor_distance(3)

            if 0.01 < rl < 1:
                pioneer.rotate_left()
            elif 0.01 < ll < 1:
                pioneer.rotate_right()
            else:
                pioneer.move_forward()
            time.sleep(0.1)
```


## License
Copyright (C) 2016-2017  Stanislav Eprikov, Pavel Pletenev 

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
