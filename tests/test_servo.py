import os
import unittest
from aiounittest import async_test
from components import servo

# change to root directory to see 'augments' folder
os.chdir("../")


# servo for testing
@servo.add_servo({
    "name": "testservo",
    "description": "servo for test case TestServo",
    "author": "John Doe"
})
class BasicServo(servo.Servo):
    def setup(self):
        self.value1 = False
        self.value2 = False

    def sync_test(self):
        self.value1 = True

    async def async_test(self):
        self.value2 = True

    @servo.add_command({
        "name": "command1",
        "description": "command 1 for test case TestServo",
        "author": "John Doe"
    })
    async def command1(self, context):
        self.sync_test()
        await self.async_test()

    @servo.add_command({
        "name": "command2",
        "description": "command 2 for test case TestServo",
        "author": "John Doe"
    })
    async def command2(self, context):
        return True


class TestServoFunctionality(unittest.TestCase):
    def setUp(self):
        self.servo = servo.get_servo("testservo")

    # ensure the servo obtained by get_servo() and the class above are the same
    def test_get_servo(self):
        self.assertEqual(self.servo, BasicServo)

    # ensure that the information was correctly attributed
    @async_test
    def test_servo_info(self):
        self.assertEqual(self.servo.info["name"], "testservo")
        self.assertEqual(self.servo.info["description"], "servo for test case TestServo")
        self.assertEqual(self.servo.info["author"], "John Doe")

    # ensure that the commands were correctly added and that their info was correctly attributed
    @async_test
    def test_command_additions(self):
        s = self.servo()
        self.assertTrue(s.has_command("command1"))
        self.assertTrue(s.has_command("command2"))
        self.assertFalse(s.has_command("sync_test"))

    # ensure that the call() function works
    @async_test
    async def test_servo_methods(self):
        s = self.servo()
        s.set_logger("SigurTest")
        await s.call("command1", None)
        self.assertTrue(s.value1)
        self.assertTrue(s.value2)


if __name__ == "__main__":
    unittest.main()
