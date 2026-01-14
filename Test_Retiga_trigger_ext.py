

from pipython import GCSDevice, pitools
import time
import numpy as np
import matplotlib.pyplot as plt 
import warnings
import tifffile as tiff 
import os


def add_path(path):
    import sys
    import os
    # add path to ospath list, assuming that the path is in a sybling folder
    from os.path import dirname
    sys.path.append(os.path.abspath(os.path.join(dirname(dirname(__file__)),path)))


def collect_frames(cam, num_frames):
    frames_received = 0
    while frames_received < num_frames:
        try:
            frame, fps, frame_count = cam.poll_frame()
            print(f"Count: {frame_count:2}  FPS: {fps:5.1f}"
                  f"  First five pixels: {frame['pixel_data'][0, 0:5]}")
            frames_received += 1
        except ValueError as e:
            print(str(e))

    return frames_received



#Connect motor
add_path('PI_ScopeFoundry')
from PI_VC_device import PI_VC_Device   
motor = PI_VC_Device('0185500006', '1')

#Connect camera
from CameraDevice import PVcamDevice
camera = PVcamDevice()



print('Motor initialized')
print('Device:', motor.pi_device.devname)
print('Mode:', motor.get_mode())
motor.set_velocity(1.0)
print('Velocity:', motor.get_velocity())
motor.move_absolute(1.5)
motor.wait_on_target()
# print('Initial position for trigger:', motor.get_position())
# motor.trigger(0.02, 2.3, 2.8, 1, 4)
# motor.move_absolute(4.5)
# motor.wait_on_target()
# print('Final position after trigger:', motor.get_position())


print("Camera initialized") 
camera.metadata_enabled = True

print('Acquisition mode is:', camera.get_trigger_mode())
camera.set_exposure(10) #MUST BE INTEGER!
print('Exposure time [ms] is:',camera.get_exposure())
print('Temperature [°C] is:',camera.get_temperature())
camera.set_binning(2)
print('Binning is:',camera.get_binning())
print('Gain is:',camera.get_gain())
print('Sensor size is (width, height):',(camera.get_width(),camera.get_height()))
print('Acquisition mode for Internal trigger is:', camera.get_trigger_mode())

# #Single frame acquisition
# camera.set_trigger_mode('Internal Trigger')
# camera.acq_start()
# image=camera.get_nparray()
# plt.figure()
# plt.imshow(image, cmap='gray')
# plt.show()
# camera.acq_stop()

# #Acquisition multiple frames
camera.set_trigger_mode('Edge Trigger')
print('Acquisition mode is:', camera.get_trigger_mode())
motor.move_absolute(1.5)
print('Initial position for trigger:', motor.get_position())
motor.trigger(0.025, 2.3, 2.4, 1, 4)

frame_num = 5
# Start acquisition: 2 possible commands
# camera.acq_start() # live acquisition
camera.acq_start_seq(frame_num) #sequential acquisition of a fixed number of frames

motor.move_absolute(4.5)
motor.wait_on_target()
print('Final position after trigger:', motor.get_position())


# #Retrieve and plot images
# for i in range(10):
#     print('Acquiring frame', i+1)
#     frame, fps, frame_count =camera.cam.poll_frame()
#     print('Frame count:', frame_count)
#     if i+1 > frame_count:
#         print('No frame acquired')
#         break
#     else:
#         image=frame['pixel_data']
#         plt.figure()
#         plt.imshow(image, cmap='gray')
#         plt.show()
#         plt.pause(0.5)   # seconds
#         plt.close()



received_frames = collect_frames(camera.cam, frame_num)
print(f'Received live frames: {received_frames}\n')
image = np.zeros((frame_num, int(camera.get_height()/camera.get_binning()), int(camera.get_width()/camera.get_binning())), dtype=np.uint16)

timestamp = time.strftime("%y%m%d_%H%M%S", time.localtime())
saving_dir = r"C:\Temp"
sample_name = f"retiga_ext_trigger_{frame_num}frames_{timestamp}"
fname = os.path.join(saving_dir, sample_name + '.tiff')

for i in range(frame_num):
    frame, fps, frame_count = camera.cam.poll_frame()

    image[i, :, : ] = frame["pixel_data"]  # 2D numpy array

#Saving as a multipage tiff
tiff.imwrite(fname, image, photometric="minisblack", bigtiff=True)


camera.acq_stop()

camera.set_trigger_mode('Internal Trigger')


motor.close()
camera.close()
print('Camera closed')
#pvc.uninit_pvcam() #uninitialize the PVCAM library



