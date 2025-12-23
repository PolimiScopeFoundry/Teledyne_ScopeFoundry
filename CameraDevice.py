# -*- coding: utf-8 -*-
"""
Created on fri Mar 07 09:40:36 2025

@authors: Martina Riva. Politecnico di Milano
"""

import numpy as np
import matplotlib.pyplot as plt 
from pyvcam import pvc
from pyvcam.camera import Camera
from pyvcam import constants as const

class PVcamDevice(object):
    """
    Scopefoundry compatible class to run PVCAM cameras
    """
    #camera initialization 
    def __init__(self):

        #better to avoid:  __init__ The Camera's constructor. Note that this method 
        # should not be used in the construction of a Camera. Instead, use the detect_camera 
        # class method to generate Camera classes of the currently available cameras connected.

        #library initialization
        pvc.init_pvcam() 
        self.cam= next(Camera.detect_camera()) # Use generator to find first camera.  
        #alternative: self.cam=Camera.detect_camera()[0]
        self.cam.open() 
        self.cam.meta_data_enabled = True
        self.cam.binning=(1,1) #a tuple for the binning (x, y)
        self.cam.exp_mode= 'Internal Trigger' #'Internal Trigger', 'Edge Trigger', 'Trigger First', 'Software Trigger Edge', 'Software Trigger First'
        self.cam.exp_time= 1
        self.cam.number_frames=1
        
        self.cam.readout_port=0
        self.cam.speed_table_index=0
        self.cam.gain= 1 #PMUSBCam00 only supports gain indicies from 1 - 2.
        self.cam.trigger='Internal Trigger' #trigger mode: 'Internal Trigger', 'Edge Trigger', 'Trigger First', 'Software Trigger Edge', 'Software Trigger First'
        #readoutSpeed
        self.cam.roi = (0,0,3200,2200)

    def get_properties(self,param_ID):
        return self.cam.get_param(param_ID)

    def get_trigger_mode(self):
        mode = self.cam.exp_mode
        return(mode)


    def set_trigger_mode(self, mode):
        self.cam.exp_mode = mode

#_acquisition_mode is a private attribute and there is no built-in function to get it. Its values are 'Live' or 'Sequence'.
#what I am doing here is setting the exposure mode/trigger mode. Its values are 'Internal Trigger', 'Edge Trigger', 'Trigger First', 
# 'Software Trigger Edge', 'Software Trigger First'.

    
    def set_framenum(self, Nframes): #do I have to introduce another setting?
        pass
                    
    def get_temperature(self):
        return self.cam.temp
    
    def get_temperature_setpoint(self): #Returns the camera's temperature setpoint.
        return self.cam.temp_setpoint
    #if we need we can also set the setpoint temperature

    def get_width(self): # sensor size, not ROI size
        return self.cam.sensor_size[0]
    
    def get_height(self): #sensor size, not ROI size 
        return self.cam.sensor_size[1]
    
    def get_binning(self):
        return self.cam.binning[0] #returns the x binning value (we assume not to use different binning values for x and y)
    
    def set_binning(self, desired_binning):
        # desired_binning is a tuple (x, y) or a single value for square binning
        if isinstance(desired_binning, tuple):
            if len(desired_binning) != 2:
                raise ValueError('Shape must be a tuple of (binning_x, binning_y).')
            binning_x, binning_y = desired_binning
        else:
            binning_x = binning_y = desired_binning

        self.cam.binning = (binning_x, binning_y)
            
    def set_roi(self, h0, v0, width, height):
        #h0, v0 are the coordinates of the top/bottom left corner of the ROI
        #width, height are the dimensions of the ROI
        self.cam.meta_data_enabled = True
        self.cam.set_roi(h0, v0, width, height)  
        self.cam.roi = (h0, v0, width, height)
    
    def setSubarrayH(self, width):
        self.cam.meta_data_enabled = True
        h0=self.cam.roi[0]
        v0=self.cam.roi[1]
        height=self.cam.roi[3]
        self.cam.set_roi(h0, v0, width, height)  

    def setSubarrayHpos(self, h0):
        self.cam.meta_data_enabled = True
        v0=self.cam.roi[1]
        width=self.cam.roi[2]
        height=self.cam.roi[3]
        self.cam.set_roi(h0, v0, width, height)  

    def setSubarrayV(self, height):
        self.cam.meta_data_enabled = True
        h0=self.cam.roi[0]
        v0=self.cam.roi[1]
        width=self.cam.roi[2]
        self.cam.set_roi(h0, v0, width, height)  

    def setSubarrayVpos(self, v0):
        self.cam.meta_data_enabled = True
        h0=self.cam.roi[0]
        width=self.cam.roi[2]
        height=self.cam.roi[3]
        self.cam.set_roi(h0, v0, width, height)  


    def reset_roi(self):
        #reset the ROI to the full sensor size
        self.cam.reset_rois()

    def get_roi(self):
        return(self.cam.roi)

    def getParam(self, param_ID, attribute_ID):
        return self.cam.get_param(param_ID, attribute_ID)

    def get_exposure(self):
        return self.cam.exp_time 

    def set_exposure(self, desired_time): 
        self.cam.exp_time = desired_time


    def get_rate(self):
        pass

    def set_rate(self, desired_framerate):
        pass

    def get_gain(self):
        return self.cam.gain

    def set_gain(self, desired_gain):
        self.cam.gain = desired_gain

        
    def get_idname(self):
        return self.cam.name

    
    def acq_start(self):
        self.cam.start_live()       
        #circular buffer with 16 frames by default
        #not necessary to specify the exposure time since it has been set


    #def acq_start_seq(self, number_frames):
    #     self.cam.start_seq(num_frames=number_frames)
    # non-circular buffer acquisition.
           
    def get_nparray(self):
        #Returns a 2D np.array containing the pixel data from the captured frame.
        #self.cam.get_frame() is the built-in function
        #self.cam.start_seq(num_frames=1) #I don't need this if I always use acq_start before
        frame, fps, frame_count = self.cam.poll_frame() #returns a dictionary
        #self.finish() #is it necessary? Finishing acquisition may be done in the main script with acq_stop
        #return frame['pixel_data']
        return frame
    
    def acq_stop(self):
        # Ends a previously started live or sequence acquisition.
        self.cam.finish()


    def close(self):
        self.cam.close() #Closes the camera.
        pvc.uninit_pvcam() #uninitialize the PVCAM library

#USE ONLY START_SEQ AND POLL_FRAME FOR SEQUENTIAL ACQUISITION


#NOTE: All getters/setters are accessed by attribute. This means that
# it will appear that we are accessing instance variables from a 
# camera, but in reality, these getters/setters are making specially 
# formatted calls to the Camera method get_param/set_param. These 
# getters/setters make use of the property decorator that is built 
# into Python. The reasoning behind the usage of the property decorator 
# is that attributes will change dynamically during a Camera's lifetime
# and in order to abstract PVCAM as far away from the end user as possible,
# the property decorator allows for users to intuitively view and change 
# camera settings.
# In summary: I do not access the private attributes directly, but I use 
# the getters and setters to do so.

#NOTE: the method get_param gets the current value of a specified parameter.
# Usually not called directly since the getters/setters (see below) will handle
# most cases of getting camera attributes. However, not all cases may be covered 
# by the getters/setters and a direct call may need to be made to PVCAM's get_param 
# function.
#For setting: set_param sets a specified camera parameter to a new value. 


       
if __name__ == '__main__':  
    
    try:
        camera=PVcamDevice()
        print("Camera initialized") 
        camera.meta_data_enabled = True
        camera.acq_start()
        image=camera.get_nparray()
        plt.figure()
        plt.imshow(image['pixel_data'], cmap='gray')
        plt.show()
        print('Acquisition mode is:', camera.get_trigger_mode())
        print('Exposure time [ms] is:',camera.get_exposure())
        print('Temperature [°C] is:',camera.get_temperature())
        print('Binning is:',camera.get_binning())
        print('Gain is:',camera.get_gain())
        #print('Sensor size is:',(camera.get_properties(const.PARAM_SER_SIZE),camera.get_properties(const.PARAM_PAR_SIZE)))
        print('Sensor size is (width, height):',(camera.get_width(),camera.get_height()))

        # #Acquisition multiple frames
        # camera.acq_start()
        # for i in range(10):
        #     image=camera.get_nparray()
        #     plt.figure()
        #     plt.imshow(image['pixel_data'], cmap='gray')
        # plt.show()
        camera.acq_stop()

        #Setting functions 
            #trigger mode
        camera.set_trigger_mode('Internal Trigger')
        print('Acquisition mode for Internal trigger is:', camera.get_trigger_mode())
        # camera.set_trigger_mode('Edge Trigger')
        # print('Acquisition mode for External trigger is:', camera.get_trigger_mode())
            #esposure time
        camera.set_exposure(50)
        print('Exposure time [ms] is:',camera.get_exposure())
            #gain
        camera.set_gain(2) #only supports indeces from 1 to 2
        print('Gain is:',camera.get_gain()) 
            #binning
        # camera.set_binning((2,2))
        # print('Binning is:',camera.get_binning())
        #     #ROI
        # camera.set_roi(500,500,1000,1000)
        # print('ROI is:',camera.get_roi())

        # camera.setSubarrayV(500)
        # print('ROI is:',camera.get_roi())
        
        camera.acq_start()
        image=camera.get_nparray()
        plt.figure()    
        plt.imshow(image['pixel_data'], cmap='gray')
        plt.show()

        #Reading parameters
        print('Camera info:',camera.getParam(const.PARAM_PRODUCT_NAME, const.ATTR_CURRENT))
        print('Parallel size:',camera.getParam(const.PARAM_PAR_SIZE, const.ATTR_CURRENT))
        print('Serial size:',camera.getParam(const.PARAM_SER_SIZE, const.ATTR_CURRENT))
        #camera.setSubarrayH(10)
        #print('Roi horizontal:',camera.getSubarrayH())
    
        
    finally:
        camera.close()
        print('Camera closed')
        pvc.uninit_pvcam() #uninitialize the PVCAM library
    