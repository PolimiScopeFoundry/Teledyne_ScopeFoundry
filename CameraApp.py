# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 14:44:36 2025

@authors: Martina Riva. Politecnico di Milano

Software application for the PVcam camera (RETIGA E7) using ScopeFoundry.
To launch the program: 
- activate the environment retigaE7 (where pyvcam, scopefoundry 2.0.2 are installed)
- run the script
"""


from ScopeFoundry import BaseMicroscopeApp
 
class PyVCAMapp(BaseMicroscopeApp):
    
    name = 'PyVCAMapp'
    
      
    
    def setup(self):
        from CameraHW import PVcamHW
        self.add_hardware(PVcamHW(self))
        
        print("Adding Hardware Components")
        
        from CameraMeasurement import PVcamMeasure
        self.add_measurement(PVcamMeasure(self))
        print("Adding measurement components")


if __name__ == '__main__':
            
    import sys
    app = PyVCAMapp(sys.argv)
    sys.exit(app.exec_())
        
