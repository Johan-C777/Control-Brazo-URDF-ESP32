import pybullet as p
import pybullet_data
import time
import serial

PUERTO = 'COM3'  # Confirma tu puerto
BAUD_RATE = 115200

try:
    ser = serial.Serial(PUERTO, BAUD_RATE, timeout=0.1)
    time.sleep(2)
    ser.reset_input_buffer()
    print("Conexión serial establecida.")
except Exception as e:
    ser = None
    print(f"Error serial: {e}. Modo sin hardware.")

physics_client = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
robot_id = p.loadURDF("brazo.urdf", [0, 0, 0.15], useFixedBase=True)

def mapear(val, in_min, in_max, out_min, out_max):
    # Protege (limita) el valor para que no se salga de 0 a 4095
    val = max(min(val, in_max), in_min)
    return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

print("Iniciando simulación...")

while True:
    if ser and ser.in_waiting > 0:
        try:
            linea = ser.readline().decode('utf-8').strip()
            datos = linea.split(',')

            if len(datos) == 3:
                pot_base, pot_brazo, pot_pinza = map(int, datos)

                # Mapeo normal a los límites del URDF
                pos_base = mapear(pot_base, 0, 4095, -2.5, 2.5)  
                pos_brazo = mapear(pot_brazo, 0, 4095, -2.0, 2.0) 
                pos_dedos = mapear(pot_pinza, 0, 4095, 0.0, 0.05) 

                p.setJointMotorControl2(robot_id, 0, p.POSITION_CONTROL, targetPosition=pos_base)
                p.setJointMotorControl2(robot_id, 1, p.POSITION_CONTROL, targetPosition=pos_brazo)
                p.setJointMotorControl2(robot_id, 3, p.POSITION_CONTROL, targetPosition=pos_dedos)
                p.setJointMotorControl2(robot_id, 4, p.POSITION_CONTROL, targetPosition=pos_dedos)
        except Exception:
            pass  # Ignorar tramas ruidosas

    p.stepSimulation()
    time.sleep(0.02)