from jetbot import Robot
import time
import cv2
from . import servoserial
#from servoserial import ServoSerial
robot = Robot()
#robot.left_motor.value = 0.8
# 0 - 1.0
#robot.right_motor.value = 0.8


#from servoserial import ServoSerial
#servo_device = ServoSerial()
# 中央位置
#servo_device.Servo_serial_control(1, 2100)
#servo_device.Servo_serial_control(2, 2048)
# index = 1 : 左右方向  600 ~ 3600
# index = 2 : 上下方向  1300 ~ 4095

BEST_MATCH_TIME = 0.05

class myRobot():
    def __init__(self):
        self.motor = Robot()
        self.servo = servoserial.ServoSerial()

    def forward(self, alpha):
        if alpha > 1:
            alpha = 1.0
        if alpha < 0:
            alpha = 0.0
        self.motor.left_motor.value = alpha * 1.0
        self.motor.right_motor.value = alpha * 1.0
    
    def turn(self, beta_l, beta_r, alpha):
        self.robot.left_motor.value = 1.0 * beta_l * alpha
        self.robot.right_motor.value = 1.0 * beta_r * alpha

    def nod(self, gamma):
        self.servo.Servo_serial_control(2, 2048 + gamma * 1000)

    def test_dance(self):
        # 逐渐加速测试
        for i in range(100):
            self.forward(i / 100.0)
            time.sleep(BEST_MATCH_TIME)

        # 逐渐减速测试
        for i in range(100, 0, -1):
            self.forward(i / 100.0)
            time.sleep(BEST_MATCH_TIME)

        # 左右转测试
        for i in range(0,50):
            self.turn(i / 100.0, i / 100.0)

        # 云台上下移动测试
        for i in range(-50, 50):
            self.nod( i / 100.0 )

KP = 1.0
KI = 1.0
KD = 1.0

class Order():
    def __init__(self, \
        error_rl=0, error_ud=0, error_qh=0,\
        beta_l=0, beta_r=0, alpha=0, gamma=0):
        # 水平方向误差
        self.error_rl = error_rl
        # 垂直方向误差
        self.error_ud = error_ud
        # 前后距离误差
        self.error_qh = error_qh
        self.al = alpha
        self.bl = beta_l
        self.br = beta_r
        self.ga = gamma


    def PID(self, last_e_rl, last_e_ud, last_e_qh):
        # 左右转驱动因子计算
        error_sum_rl = self.error_rl + last_e_rl
        rl = KP * self.error_rl + KI * error_sum_rl + KD * (self.error_rl - last_e_rl)
        # 云台上下移动驱动因子计算
        error_sum_ud = self.error_ud + last_e_ud
        ud = KP * self.error_ud + KI * error_sum_ud + KD * (self.error_ud - last_e_ud)
        # 直线运动驱动因子计算
        error_sum_qh = self.error_qh + last_e_qh
        qh = KP * self.error_qh + KI * error_sum_qh + KD * (self.error_qh - last_e_qh)
        print("rl: ", rl)
        print("ud: ", ud)
        print("qh: ", qh)
        return rl, ud, qh

def robot_move(order_queue, robot):
    last_erl = 0
    last_eud = 0
    last_eqh = 0
#    while cap.isOpened():
    while True:
        
        if not order_queue.empty():
            ords = order_queue.get()
        #if ords:
            rl, ud, qh = ords.PID(last_erl, last_eud, last_eqh)
            #robot.forward(qh * ( 1 / 1000 ))
            #robot.turn(ords.bl, ords.br, ords.al)
            #robot.nod(ords.ga)
            last_erl, last_eud, last_eqh = \
                ords.error_rl,\
                ords.error_ud,\
                ords.error_qh
        else:
            print("Order_queue is always empty")
#    cap.release()
