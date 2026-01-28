# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 08:40:36 2025

@authors: Martina Riva. Politecnico di Milano
"""

from ScopeFoundry import HardwareComponent
# from PVCAM_ScopeFoundry.CameraDevice import PVcamDevice
from CameraDevice import PVcamDevice

class PVcamHW(HardwareComponent):
    name = 'PVcamHW'
    
    def setup(self):
        # create Settings (aka logged quantities)    
        self.infos = self.settings.New(name='name', dtype=str)
        self.temperature = self.settings.New(name='temperature', dtype=float, ro=True, unit='°C')
        self.temperature_setpoint = self.settings.New(name='temperature_setpoint', dtype=float, 
                                                      ro=True, unit='°C')
        self.number_frames = self.add_logged_quantity("number_frames", dtype = int, si = False, ro = 0, 
                                        initial = 200, vmin = 1, reread_from_hardware_after_write = True)
        self.image_width = self.settings.New(name='image_width', dtype=int, ro=True)
        self.image_height = self.settings.New(name='image_height', dtype=int, ro=True)
        # self.binning_x=self.settings.New(name='binning_x', dtype=int, ro=False, choices = [1, 2, 4],
        #                                  initial = 1, reread_from_hardware_after_write = True )
        # self.binning_y=self.settings.New(name='binning_y', dtype=int, ro=False,choices = [1, 2, 4],
        #                                  initial = 1, reread_from_hardware_after_write = True)

        #NOTE: the binning is set with the same value for x and y. Code should be modified if needed.
        self.binning=self.settings.New(name='binning', dtype=int, ro=False,choices = [1, 2, 4],
                                    initial = 1, reread_from_hardware_after_write = True)

        self.subarrayh = self.settings.New("subarray_hsize", dtype=int, si = False, ro= 0,
                                                   spinbox_step = 4, spinbox_decimals = 0, initial = 3200,
                                                   vmin = 4, vmax = 3200, reread_from_hardware_after_write = True)
        
        self.subarrayv = self.settings.New("subarray_vsize", dtype=int, si = False, ro= 0, 
                                                  spinbox_step = 4, spinbox_decimals = 0, initial = 2200, 
                                                  vmin = 4, vmax = 2200, reread_from_hardware_after_write = True)
        
        self.subarrayh_pos = self.settings.New('subarrayh_pos', dtype = int, si = False, ro = 0,
                                                      spinbox_step = 4, spinbox_decimals = 0, initial = 0, 
                                                      vmin = 0, vmax = 3196, reread_from_hardware_after_write = True,
                                                      description = "The default value 0 corresponds to the first pixel starting from the left")
        
        self.subarrayv_pos = self.settings.New('subarrayv_pos', dtype = int, si = False, ro = 0,
                                                      spinbox_step = 4, spinbox_decimals = 0, initial = 0, 
                                                      vmin = 0, vmax = 2196, reread_from_hardware_after_write = True,
                                                      description = "The default value 0 corresponds to the first pixel starting from the top/bottom")
        self.readout = self.settings.New(name='readout', dtype=int, ro=False, 
                                        choices = [0, 1, 2], initial = 0, 
                                        reread_from_hardware_after_write = True)
        self.gain = self.settings.New(name='gain', initial=1, dtype=int,
                                      choices = [1, 2],
                                      ro=False, reread_from_hardware_after_write=True)
        #NOTE: maximum gain value 2 for readout modes 1 and 2. For readout mode 0 only gain value 1 is available.
        self.exposure_time = self.settings.New(name='exposure_time', initial=20, vmax =3600000,
                                               vmin = 0, spinbox_step = 0.01,dtype=int, ro=False, unit='ms',
                                               reread_from_hardware_after_write=True)
        #NOTE: maximum exposure time of 3600000 ms is available only in long exposure mode (see readout port 1 or 2)
        self.acquisition_mode = self.settings.New(name='acquisition_mode', dtype=str,
                                                  choices=['Continuous', 'MultiFrame'], initial = 'Continuous', ro=False, reread_from_hardware_after_write = True)  #Uncomment to choose acquisition mode
        self.trmode = self.add_logged_quantity('trigger_mode', dtype=str, si=False, ro=0, 
                                       choices = ['Internal Trigger', 'Edge Trigger', 'Trigger First', 'Software Trigger Edge', 'Software Trigger First'], initial = 'Internal Trigger', reread_from_hardware_after_write = True)

    def connect(self):
        # create an instance of the Device
        self.cam = PVcamDevice() 
        

        # connect settings to Device methods
        self.infos.hardware_read_func = self.cam.get_idname
        self.temperature.hardware_read_func = self.cam.get_temperature
        self.temperature_setpoint.hardware_read_func = self.cam.get_temperature_setpoint
        self.image_width.hardware_read_func = self.cam.get_width
        self.image_height.hardware_read_func = self.cam.get_height  
        self.exposure_time.hardware_read_func = self.cam.get_exposure
        #self.frame_rate.hardware_read_func = self.cam.get_rate
        self.gain.hardware_read_func = self.cam.get_gain
        self.readout.hardware_read_func = self.cam.get_readout
        self.binning.hardware_read_func = self.cam.get_binning      
        self.trmode.hardware_read_func = self.cam.get_trigger_mode    
        self.subarrayh.hardware_read_func = self.cam.getSubarrayH
        self.subarrayv.hardware_read_func = self.cam.getSubarrayV
        self.subarrayh_pos.hardware_read_func = self.cam.getSubarrayHpos
        self.subarrayv_pos.hardware_read_func = self.cam.getSubarrayVpos
        #self.roi.hardware_read_func = self.cam.get_roi

        self.exposure_time.hardware_set_func=self.cam.set_exposure
        self.binning.hardware_set_func = self.cam.set_binning
        self.gain.hardware_set_func = self.cam.set_gain
        self.readout.hardware_set_func = self.cam.set_readout
        self.subarrayh.hardware_set_func = self.cam.setSubarrayH
        self.subarrayv.hardware_set_func = self.cam.setSubarrayV
        self.subarrayh_pos.hardware_set_func = self.cam.setSubarrayHpos
        self.subarrayv_pos.hardware_set_func = self.cam.setSubarrayVpos
        #self.roi.hardware_set_func = self.cam.set_roi
        self.trmode.hardware_set_func = self.cam.set_trigger_mode
        self.read_from_hardware()

        
    def disconnect(self):
        if hasattr(self, 'cam'):
            self.cam.close() 
            del self.cam
            
        for lq in self.settings.as_list():
            lq.hardware_read_func = None
            lq.hardware_set_func = None