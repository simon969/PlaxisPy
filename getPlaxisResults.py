#########################################################################
#
#      Title:       Plaxis 2d and Plaxis 3d Result Output Classes
#
#########################################################################
#
#      Description: Python classes to recover results from Plaxis 2d and Plaxis 3d analysis models
#
#               my_path = r'C:\Users\Public\Documents\GEO-3523'
#               my_module = imp.find_module('getPlaxisResults', [my_path])
#               getPlaxisResults = imp.load_module('getPlaxisResults', *my_module)
#
#
#
#               p2dr = getPlaxis2dResults(o_g)
#               p2dr.getSoilResultsByRange(
#                           fileOut=None,
#                           sphaseOrder=None,
#                           sphaseStart=None,
#                           sphaseEnd=None,
#                           xMin=None, xMax=None,
#                           yMin=None, yMax=None,
#                           )
#               p2dr.getPlateResults(
#                           fileOut=None,
#                           sphaseOrder=None,
#                           sphaseStart=None,
#                           sphaseEnd=None
#                           )
#               p2dr.getAllStructuralResults(
#                           fileOut=None,
#                           sphaseOrder=None,
#                           sphaseStart=None,
#                           sphaseEnd=None
#                           )
#
#               p3dr = getPlaxis3dResults(o_g)
#               p3dr.getSoilResultsByRange(
#                           fileOut=None,
#                           sphaseOrder=None,
#                           sphaseStart=None,
#                           sphaseEnd=None,
#                           xMin=None, xMax=None,
#                           yMin=None, yMax=None,
#                           )
#
#########################################################################
#
#########################################################################
#
#       Author      Thomson, Simon simon.thomson@aecom.com
#
##########################################################################
#
#       Version:    Beta 0.0.3
#
##########################################################################
#
#       Date:       2017 November 10
#
###########################################################################

##########################################################################
#
# Boiler Plate for project file  Plaxis 2D AE/2016
#
##########################################################################
#
#
# import imp
# plaxis_path = r'C:\Program Files (x86)\Plaxis\PLAXIS 2D'
# found_module = imp.find_module('plxscripting', [plaxis_path])
# plxscripting = imp.load_module('plxscripting', *found_module)
# from plxscripting.easy import *
#
# s_o, g_o = new_server('localhost', 10000)
#                  
##############################################################################

##########################################################################
#
# Boiler Plate for project file  Plaxis3D 2017
#
##########################################################################
#
#
# import imp
# plaxis_path = r'C:\Program Files\Plaxis\PLAXIS 3D\python\Lib\site-packages'
# found_module = imp.find_module('plxscripting', [plaxis_path])
# plxscripting = imp.load_module('plxscripting', *found_module)
# from plxscripting.easy import *
#
# s_o, g_o = new_server('localhost', port=10000, password='')   
#      
#
##############################################################################

class PlaxisScripting (object):
    def __init__(self,
                 output_server
                 ):

        global g_o, pts
        g_o = output_server
        pts = []
        
    class Point2d(object):
        def __init__(self, name, x, y):
                self.name = name
                self.x = float(x)
                self.y = float(y)
               
    class Point3d(object):
        def __init__(self, name, x, y, z):
                self.name = name
                self.x = float(x)
                self.y = float(y)
                self.z = float(z)
    
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False  
    
    def isfloat(self, s, value_false):
        try:
            if s == 'NaN':
                return value_false
            if s == 'not found':
                return value_false
            else:
                f = float(s)
                print('float:', f)
                return f

        except ValueError:
            return value_false
    
    def getPhaseInt(self, 
                    phaseName):
        count = 0
        print('looking for phase:' + phaseName)
        for phase in g_o.Phases:
            if phase.Name.value == phaseName:
                print('found...', count)
                return count
            count += 1
        return -1
        
    def getCalculationInfo_CSV(self, phase=None):
        if phase is None:
            phase = g_o.Phases[0]
            
        out_str = ''
        out_str += '"' + phase.Name.value  + '",'
        out_str += '"' + phase.Identification.value  + '",'
        out_str += '"' + phase.Step.value  + '",'
    
    def setPhaseOrder(self,
                      sphaseOrder=None,
                      sphaseStart=None,
                      sphaseEnd=None):

        global phaseOrder
        phaseOrder = []

        if sphaseOrder is None:
            if sphaseStart is None and sphaseEnd is None:
                phaseOrder = g_o.Phases[:]
                if phaseOrder is not None:
                    print ('All phases added to phaseOrder')

            if sphaseStart is None and sphaseEnd is not None:
                id = self.getPhaseInt(sphaseEnd)
                phaseOrder = g_o.Phases[:id]
                if phaseOrder is not None:
                    print ('All phases up to', sphaseEnd, ' added')
    

            if sphaseStart is not None and sphaseEnd is None:
                id = self.getPhaseInt(phaseName=sphaseStart)
                phaseOrder = g_o.Phases[id:]
                if phaseOrder is not None:
                    print ('All phases from ', sphaseStart, ' added')

            if sphaseStart is not None and sphaseEnd is not None:
                id = self.getPhaseInt(sphaseStart)
                id2 = self.getPhaseInt(sphaseEnd)
                phaseOrder = g_o.Phases[id:id2 + 1]
                if phaseOrder is not None:
                    print ('All phases from ', sphaseStart, ' to ', sphaseEnd, ' added')
                    
        if sphaseOrder is not None:
            for sphase in sphaseOrder:
                id = self.getPhaseInt(sphase)
                phaseOrder.append(g_o.Phases[id])
                print('phase:', sphase ,' added')
        
        if phaseOrder is not None:
                    print ('phaseOrder initialised with', len(phaseOrder) , ' no. phases')   

                    
    def setRange (self,
                  xMin=None,
                  xMax=None,
                  yMin=None,
                  yMax=None,
                  zMin=None,
                  zMax=None
                  ):
        global g_xMin, g_xMax, g_yMin, g_yMax, g_zMin, g_zMax
        g_xMin = xMin
        g_xMax = xMax
        g_yMin = yMin
        g_yMax = yMax
        g_zMin = zMin
        g_zMax = zMax
        
    def printRange(self):
        print ('g_xMin',g_xMin, 
               'g_xMax',g_xMax,
               'g_yMin',g_yMin,
               'g_yMax',g_yMax,)
               
    def inRange (self,
                 x_val=None,
                 y_val=None,
                 z_val=None
                 ):
                 
        xMinRangeOk = True 
        xMaxRangeOk = True 
        yMinRangeOk = True
        yMaxRangeOk = True
        zMinRangeOk = True
        zMaxRangeOk = True
        
      #  self.printRange()
        
      #  print ('x_val', x_val,
      #        'y_val', y_val)
               
        if g_xMin is not None and x_val is not None:
            if x_val >= g_xMin:
                xMinRangeOk = True 
            else:
                xMinRangeOk = False  
        else:
            xMinRangeOk = True 
        
        if g_yMin is not None and y_val is not None:
            if y_val >= g_yMin:
                yMinRangeOk = True 
            else:
                yMinRangeOk = False
        else:
            yMinRangeOk = True 
        
        if g_xMax is not None and x_val is not None:
            if x_val <= g_xMax:
                xMaxRangeOk = True 
            else:
                xMaxRangeOk = False  
        else:
            xMaxRangeOk = True 
        
        if g_yMax is not None and y_val is not None:
            if y_val <= g_yMax:
                yMaxRangeOk = True 
            else:
                yMaxRangeOk = False
        else:
            yMaxRangeOk = True 
           
        if g_zMax is not None and z_val is not None:
            if z_val <= g_zMax:
                zMaxRangeOk = True 
            else:
                zMaxRangeOk = False
        else:
            zMaxRangeOk = True     
        
        if g_zMin is not None and z_val is not None:
            if z_val >= g_zMin:
                zMinRangeOk = True 
            else:
                zMinRangeOk = False
        else:
            zMinRangeOk = True 
            
        if xMinRangeOk and xMaxRangeOk and yMinRangeOk and yMaxRangeOk and zMinRangeOk and zMaxRangeOk:
           # print ('inRange x_val', x_val,
           #     'y_val', y_val)
            return True 
        else:
            return False  
            
    def setNodeList (self,
                     xMin=0.0, xMax=0.0,
                     yMin=0.0, yMax=0.0,
                     zMin=0.0, zMax=0.0):
        global NodeList
        NodeList = []
        phase = phaseOrder[0]
        count = 0
        
        self.setRange(xMin, xMax,
                      yMin, yMax, 
                      zMin, zMax)
        
        soilX = g_o.getresults(phase, g_o.ResultTypes.Soil.X, 'node')
        soilY = g_o.getresults(phase, g_o.ResultTypes.Soil.Y, 'node')
        soilZ = g_o.getresults(phase, g_o.ResultTypes.Soil.Z, 'node')
        
        print('Coordinates retrieved for Phase ', phase.Name.value)
        
        for x, y, z in zip(soilX, soilY, soilZ):
            if self.inRange (x_val = x, y_val = y, z_val = z) == True:
                count =  count + 1
                NodeList.append(self.PlPoint(count, x, y, z))
                print ('Added node at (', x, y, z, ')')
        print (len(NodeList), ' nodes added to NodeList')
        
        
    def loadNodeList (self, 
                      fileIn):
        global NodeList
        NodeList = []

        fpoint = open(fileIn, "r")

        while True:
            in_line = fpoint.readline()
            if in_line == "":
                break
            if ',' in in_line:
                print(in_line)
                [name, nx, ny, nz] = in_line.split(',')
                if self.is_number(nx):
                    if self.is_number(ny):
                        if self.is_number(nz):
                            NodeList.append(self.Point3d(name, nx, ny, nz))

        fpoint.close()                  
    
class Plaxis2dResults (PlaxisScripting):

    def __init__(self,
                 output_server
                 ):
        super(Plaxis2dResults, self).__init__(output_server)
    def getSoilResultsByRange(self,
                              fileOut=None,
                              sphaseOrder=None,
                              sphaseStart=None,
                              sphaseEnd=None,
                              xMin=None, xMax=None,
                              yMin=None, yMax=None,
                              ):

        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)
                           
        self.setRange(xMin, xMax,
                      yMin, yMax)
        
        if phaseOrder is None:
            print('No phases found for results')
            return -1

        locY = []
        locX = []
        
        Uyy = []
        Uxx = []
            
        EffSxx = []
        EffSyy = []
        EffSzz = []
        
        EffP1 = []
        EffP2 = []
        EffP3 = []        
        
        PExcess = []
        PActive = []
        PSteady = []
        PWater = []
        
        Suct = []
        EffSuct = []
        
        pPhaseName = []
        pPhaseIdent = []
        
        # look into all phases, all steps
        for phase in phaseOrder:
            print('Getting Soil results for Phase ', phase.Name.value, phase.Identification.value)
          
            soilX = g_o.getresults(phase, g_o.ResultTypes.Soil.X, 'node')
            soilY = g_o.getresults(phase, g_o.ResultTypes.Soil.Y, 'node')
            
            soilUx = g_o.getresults(phase, g_o.ResultTypes.Soil.Ux, 'node')
            soilUy = g_o.getresults(phase, g_o.ResultTypes.Soil.Uy, 'node')
            
            soilEffSxx = g_o.getresults(phase, g_o.ResultTypes.Soil.SigxxE, 'node')
            soilEffSyy = g_o.getresults(phase, g_o.ResultTypes.Soil.SigyyE, 'node')
            soilEffSzz = g_o.getresults(phase, g_o.ResultTypes.Soil.SigzzE, 'node')
            soilEffP1= g_o.getresults(phase, g_o.ResultTypes.Soil.SigmaEffective1, 'node')
            soilEffP2 = g_o.getresults(phase, g_o.ResultTypes.Soil.SigmaEffective2, 'node')
            soilEffP3 = g_o.getresults(phase, g_o.ResultTypes.Soil.SigmaEffective3, 'node')  
            
            soilPExcess = g_o.getresults(phase, g_o.Soil.PExcess, 'node')
            soilPActive = g_o.getresults(phase, g_o.Soil.PActive, 'node')
            soilPSteady = g_o.getresults(phase, g_o.Soil.PSteady, 'node')
            soilPWater = g_o.getresults(phase, g_o.Soil.PWater, 'node')
            
            soilSuction = g_o.getresults(phase, g_o.Soil.Suction, 'node')
            soilEffSuction = g_o.getresults(phase, g_o.Soil.EffSuction, 'node')
            
            for x, y, ux, uy, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su, esu in zip(
                soilX, soilY, soilUx, soilUy, soilEffSxx, soilEffSyy, soilEffSzz, soilEffP1, soilEffP2, soilEffP3, soilPExcess, soilPActive, soilPSteady, soilPWater, soilSuction, soilEffSuction):
                
                if self.inRange (x_val = x, 
                                 y_val = y) == True:
                    
                    print(phase.Name.value, phase.Identification.value, x, y, ux, uy, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su, esu)
          
                    pPhaseName.append(phase.Name.value)
                    pPhaseIdent.append(phase.Identification.value)
           
                    locX.append(x)
                    locY.append(y)
                    
                    Uxx.append(ux)
                    Uyy.append(uy)
                
                    EffSxx.append(esx)
                    EffSyy.append(esy)
                    EffSzz.append(esz)
                    
                    EffP1.append (ep1)
                    EffP2.append (ep2)
                    EffP3.append (ep3)
                    
                    PExcess.append (pe)
                    PActive.append (pa)
                    PSteady.append (ps)
                    PWater.append (pw)
        
                    Suct.append (su)
                    EffSuct.append (esu)
                    
        if fileOut:
            with open(fileOut, "w") as file:
                file.writelines(
                    ["Phase, Phase Identification, locX(m),locY(m),Ux(m},Uy(m),SigxxEff(kPa),SigyyEff(kPa),SigzzEff(kPa),SigP1Eff(kPa),SigyP2Eff(kPa),SigP3Eff(kPa),PExcess(kPa),PActive(kPa),PSteady(kPa),Pwater(kPa),Suct(kPa),EffSuct(kPa)\n"])
                file.writelines(["{},{},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}\n".format(pname, pident,  x, y, ux, uy, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su, esu )
                                 for pname, pident, x, y, ux, uy, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su, esu in zip(pPhaseName, pPhaseIdent, locX, locY, Uxx, Uyy, EffSxx, EffSyy, EffSzz, EffP1, EffP2, EffP3, PExcess, PActive, PSteady, PWater, Suct, EffSuct)])
        print('getSoilResultsByRange Done')
         
    def getSoilResultsByPoints(self,
                               filePoints=None,
                               fileOut=None,
                               sphaseOrder=None,
                               sphaseStart=None,
                               sphaseEnd=None,
                               ):

        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)
        locName = []
        locY = []
        locX = []
        
        Uyy = []
        Uxx = []
        Utot = []
            
        PUyy = []
        PUxx = []
        PUtot = []
        
        EffSxx = []
        EffSyy = []
        EffSzz = []
        
        EffP1 = []
        EffP2 = []
        EffP3 = []        
        
        PExcess = []
        PActive = []
        PSteady = []
        PWater = []
        
        Suct = []
        EffSuct = []
        
        pPhaseName = []
        pPhaseIdent = []
               

        fpoint = open(filePoints, "r")

        while True:
            in_line = fpoint.readline()
            if in_line == "":
                break
            print(in_line)
            [name, nx, ny] = in_line.split(',')
            pts.append(self.Point2d(name, nx, ny))

        fpoint.close()

       

        for phase in phaseOrder:
            print('Getting soil results ' + phase.Identification.value)
            

                       
            for pt in pts:

                try:
           
                    ux = g_o.getsingleresult(phase, g_o.Soil.Ux, (pt.x, pt.y))
                    uy = g_o.getsingleresult(phase, g_o.Soil.Uy, (pt.x, pt.y))
                    ut = g_o.getsingleresult(phase, g_o.Soil.Utot, (pt.x, pt.y))
                    pux = g_o.getsingleresult(phase, g_o.Soil.PUx, (pt.x, pt.y))
                    puy = g_o.getsingleresult(phase, g_o.Soil.PUy, (pt.x, pt.y))
                    put = g_o.getsingleresult(phase, g_o.Soil.PUtot, (pt.x, pt.y))
                    esx = g_o.getsingleresult(phase, g_o.Soil.SigxxE, (pt.x, pt.y))
                    esy = g_o.getsingleresult(phase, g_o.Soil.SigyyE, (pt.x, pt.y))
                    esz = g_o.getsingleresult(phase, g_o.Soil.SigzzE, (pt.x, pt.y))
                    ep1 = g_o.getsingleresult(phase, g_o.Soil.SigmaEffective1, (pt.x, pt.y))
                    ep2 = g_o.getsingleresult(phase, g_o.Soil.SigmaEffective2, (pt.x, pt.y))
                    ep3 = g_o.getsingleresult(phase, g_o.Soil.SigmaEffective3, (pt.x, pt.y))  
                    pe = g_o.getsingleresult(phase, g_o.Soil.PExcess, (pt.x, pt.y))
                    pa = g_o.getsingleresult(phase, g_o.Soil.PActive, (pt.x, pt.y))
                    ps = g_o.getsingleresult(phase, g_o.Soil.PSteady, (pt.x, pt.y))
                    pw = g_o.getsingleresult(phase, g_o.Soil.PWater, (pt.x, pt.y))
                    su = g_o.getsingleresult(phase, g_o.Soil.Suction, (pt.x, pt.y))
                    
                    # print (pt.name, pt.x, pt.y, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su) 
                    
                    if ux != 'not found':
                    
                        pPhaseName.append(phase.Name.value)
                        pPhaseIdent.append(phase.Identification.value)
                    
                        locName.append(pt.name)
                        locY.append(pt.y)
                        locX.append(pt.x)
                    
                        Uyy.append(uy)
                        Uxx.append(ux)
                        Utot.append(ut)
                        
                        PUyy.append(puy)
                        PUxx.append(pux)
                        PUtot.append(put)
                        
                        EffSxx.append (esx)
                        EffSyy.append (esy)
                        EffSzz.append (esz)
                           
                        EffP1.append (ep1)
                        EffP2.append (ep2)
                        EffP3.append (ep3)
                            
                        PExcess.append (pe)
                        PActive.append (pa)
                        PSteady.append (ps)
                        PWater.append (pw)
                        Suct.append (su)
                     
                except:
                    print ('...exception soil results ' + phase.Identification.value , pt.x, pt.y)
                    print (pt.name, pt.x, pt.y, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su)
          
      
        if fileOut:
            with open(fileOut, "w") as file:
                file.writelines(
                    ["Phase,Phase Identification,locName,locX(m),locY(m),Ux(m),Uy(m),Utot(m),PUx(m),PUy(m),PUtot(m),SigxxEff(kPa),SigyyEff(kPa),SigzzEff(kPa),SigP1Eff(kPa),SigyP2Eff(kPa),SigP3Eff(kPa),PExcess(kPa),PActive(kPa),PSteady(kPa),Pwater(kPa),Suct(kPa)\n"])
                file.writelines(["{},{},{},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}\n".format(pname, pident, locname, float(x), float(y), float(ux), float(uy), float(ut), float(pux), float(puy), float(put), float(esx), float(esy), float(esz), float(ep1), float(ep2), float(ep3), float(pe), float(pa), float(ps), float(pw), float(su))
                                 for pname, pident, locname, x, y, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su in zip(pPhaseName, pPhaseIdent, locName, locX, locY, Uxx, Uyy, Utot, PUxx, PUyy, PUtot, EffSxx, EffSyy, EffSzz, EffP1, EffP2, EffP3, PExcess, PActive, PSteady, PWater, Suct)])
    
        print('getSoilResultsByPoint Done')
            
    def getPlateResults(self,
                        fileOut=None,
                        sphaseOrder=None,
                        sphaseStart=None,
                        sphaseEnd=None
                        ):

        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)

        if phaseOrder is None:
            print('No phases found for results')
            return -1

        print('FileOut=', fileOut)

        # init data for lists
        pPhaseName = []
        pPhaseIdent = []
           
        pY = []
        pX = []
        pMat = []
        
        pUx = []
        pUy = []
        pUt = []

        pPUx = []
        pPUy = []
        pPUt = []

        pU1 = []
        pU2 = []

        pM2D = []
        pQ2D = []
        pNx2D = []
        pNz2D = []



        for phase in phaseOrder:
            print('Getting Plate results ' + phase.Identification.value)
            
            try: 
                plateX = g_o.getresults(phase, g_o.Plate.X, 'node')
                plateY = g_o.getresults(phase, g_o.Plate.Y, 'node')
                plateMat = g_o.getresults(phase, g_o.Plate.MaterialID, 'node')
                
                plateUx = g_o.getresults(phase, g_o.Plate.Ux, 'node')
                plateUy = g_o.getresults(phase, g_o.Plate.Uy, 'node')
                plateUt = g_o.getresults(phase, g_o.Plate.Utot, 'node')

                platePUx = g_o.getresults(phase, g_o.Plate.PUx, 'node')
                platePUy = g_o.getresults(phase, g_o.Plate.PUy, 'node')
                platePUt = g_o.getresults(phase, g_o.Plate.PUtot, 'node')

                plateU1 = g_o.getresults(phase, g_o.Plate.U1, 'node')
                plateU2 = g_o.getresults(phase, g_o.Plate.U2, 'node')

                plateM2D = g_o.getresults(phase, g_o.Plate.M2D, 'node')
                plateQ2D = g_o.getresults(phase, g_o.Plate.Q2D, 'node')
                plateNx2D = g_o.getresults(phase, g_o.Plate.Nx2D, 'node')
                plateNz2D = g_o.getresults(phase, g_o.Plate.Nz2D, 'node')
                
                print('...read Plate results ' + phase.Identification.value)
                
                for x, y, mat, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d in zip(
                        plateX, plateY, plateMat, plateUx, plateUy, plateUt, platePUx, platePUy, platePUt, plateU1, plateU2, plateM2D, plateQ2D, plateNx2D, plateNz2D):
                    # add filters in here if necessary
                    pPhaseName.append(phase.Name.value)
                    pPhaseIdent.append(phase.Identification.value)
                    pX.append(x)
                    pY.append(y)
                    pMat.append(mat)
                    pUx.append(ux)
                    pUy.append(uy)
                    pUt.append(ut)
                    pPUx.append(pux)
                    pPUy.append(puy)
                    pPUt.append(put)
                    pU1.append(u1)
                    pU2.append(u2)
                    pM2D.append(m2d)
                    pQ2D.append(q2d)
                    pNx2D.append(nx2d)
                    pNz2D.append(nz2d)
                    
            except:
                print ('...exception reading Plate results ' + phase.Identification.value)

        if fileOut:
            print('Outputing to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines(
                    ["Phase Name, Phase Indent, X(m),Y(m),Mat,Ux(m),Uy(m},Utot(m), PUx(m), PUy(m),PUt(m), U1(m),U2(m),M2D(kNm/m),Q2D(kN/m),Nx2D(kN/m),Nz2D(kN/m)\n"])
                file.writelines(["{},{},{:2f},{:2f},{},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}\n".format(pname, pident, x, y, mat, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d)
                                 for pname, pident, x, y, mat, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d in zip(pPhaseName, pPhaseIdent, pX, pY, pMat, pUx, pUy, pUt, pPUx, pPUy, pPUt, pU1, pU2, pM2D, pQ2D, pNx2D, pNz2D)])

        print('getPlateResults Done')
 
    def getEmbeddedBeamRowResults(self,
                                  fileOut=None,
                                  sphaseOrder=None,
                                  sphaseStart=None,
                                  sphaseEnd=None,
                                  ):

        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)

        if phaseOrder is None:
            print('No phases found for results')
            return -1

        print('FileOut=', fileOut)

        # init data for lists
        ePhaseName = []
        ePhaseIdent = []
           
        eY = []
        eX = []

        eUx = []
        eUy = []
        eUt = []

        ePUx = []
        ePUy = []
        ePUt = []

        eU1 = []
        eU2 = []

        eM2D = []
        eQ2D = []
        eNx2D = []
        eNz2D = []

        eTskin = []
        eTlat= []

        for phase in phaseOrder:
            #echo ResultTypes.EmbeddedBeamRow
            print ('Getting EmbeddedBeamRow results ' + phase.Identification.value)
            try:
                embeamX = g_o.getresults(phase, g_o.EmbeddedBeamRow.X, 'node')
                embeamY = g_o.getresults(phase, g_o.EmbeddedBeamRow.Y, 'node')
               
                embeamUx = g_o.getresults(phase, g_o.EmbeddedBeamRow.Ux, 'node')
                embeamUy = g_o.getresults(phase, g_o.EmbeddedBeamRow.Uy, 'node')
                embeamUt = g_o.getresults(phase, g_o.EmbeddedBeamRow.Utot, 'node')
                
                embeamPUx = g_o.getresults(phase, g_o.EmbeddedBeamRow.PUx, 'node')
                embeamPUy = g_o.getresults(phase, g_o.EmbeddedBeamRow.PUy, 'node')
                embeamPUt = g_o.getresults(phase, g_o.EmbeddedBeamRow.PUtot, 'node')
                 
                embeamU1 = g_o.getresults(phase, g_o.EmbeddedBeamRow.U1, 'node')
                embeamU2 = g_o.getresults(phase, g_o.EmbeddedBeamRow.U2, 'node')

                embeamM2D = g_o.getresults(phase, g_o.EmbeddedBeamRow.M2D, 'node')
                embeamQ2D = g_o.getresults(phase, g_o.EmbeddedBeamRow.Q2D, 'node')
                embeamNx2D = g_o.getresults(phase, g_o.EmbeddedBeamRow.Nx2D, 'node')
                embeamNz2D = g_o.getresults(phase, g_o.EmbeddedBeamRow.Nz2D, 'node')

                embeamTskin = g_o.getresults(phase, g_o.EmbeddedBeamRow.Tskin, 'node')
                embeamTlat= g_o.getresults(phase, g_o.EmbeddedBeamRow.Tlat, 'node')
                     
                print ('...read EmbeddedBeamRow results ' + phase.Identification.value)
                
                for x, y, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d, tskin, tlat in zip(
                        embeamX, embeamY, embeamUx, embeamUy, embeamUt, embeamPUx, embeamPUy, embeamPUt, embeamU1, embeamU2, embeamM2D, embeamQ2D, embeamNx2D, embeamNz2D, embeamTskin, embeamTlat):
                    # add filters in here if necessary
                    
                    ePhaseName.append(phase.Name.value)
                    ePhaseIdent.append(phase.Identification.value)
                    eX.append(x)
                    eY.append(y)
                    eUx.append(ux)
                    eUy.append(uy)
                    eUt.append(ut)
                    ePUx.append(pux)
                    ePUy.append(puy)
                    ePUt.append(put)
                    eU1.append(u1)
                    eU2.append(u2)
                    eM2D.append(m2d)
                    eQ2D.append(q2d)
                    eNx2D.append(nx2d)
                    eNz2D.append(nz2d)
                    eTskin.append(tskin)
                    eTlat.append(tlat)
            except:
                print ('...exception reading EmbeddedBeamRow '  + phase.Identification.value)
        if fileOut:
            print('Outputing to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines(
                    ["Phase, PhaseIdent, X(m),Y(m),Ux(m),Uy(m},Utot(m), PUx(m), PUy(m), PUt(m), U1(m),U2(m),M2D(kNm/m),Q2D(kN/m),Nx2D(kN/m),Nz2D(kN/m),Tskin(kN/m),Tlat(kN/m)\n"])
                file.writelines(["{},{},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}\n".format(ename, eident,x, y, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d, tskin, tlat)
                                 for ename, eident, x, y, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d, tskin, tlat in zip(ePhaseName, ePhaseIdent, eX, eY, eUx, eUy, eUt, ePUx, ePUy, ePUt, eU1, eU2, eM2D, eQ2D, eNx2D, eNz2D, eTskin, eTlat)])

        print('getEmbeddedBeamRowResults Done')
 
    def getNodeToNodeAnchorResults(self,
                                   fileOut=None,
                                   sphaseOrder=None,
                                   sphaseStart=None,
                                   sphaseEnd=None,
                                   ):

        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)

        if phaseOrder is None:
            print('No phases found for results')
            return -1

        print('FileOut=', fileOut)

        # init data for lists
        aPhaseName = []
        aPhaseIdent = []
        
        aY = []
        aX = []

        aUx = []
        aUy = []
        
        aPUx = []
        aPUy = []
        aPUt = []
        aUt = []
        aU1 = []
        aU2 = []
        
        aForce2D = []

        for phase in phaseOrder:

            print('Getting NodeToNodeAnchor results for Phase ', phase.Name.value, phase.Identification.value)
            try:
                anchorX = g_o.getresults(phase, g_o.NodeToNodeAnchor.X, 'node')
                anchorY = g_o.getresults(phase, g_o.NodeToNodeAnchor.Y, 'node')

                anchorUx = g_o.getresults(phase, g_o.NodeToNodeAnchor.Ux, 'node')
                anchorUy = g_o.getresults(phase, g_o.NodeToNodeAnchor.Uy, 'node')
                anchorUt = g_o.getresults(phase, g_o.NodeToNodeAnchor.Utot, 'node')

                anchorPUx = g_o.getresults(phase, g_o.NodeToNodeAnchor.PUx, 'node')
                anchorPUy = g_o.getresults(phase, g_o.NodeToNodeAnchor.PUy, 'node')
                anchorPUt = g_o.getresults(phase, g_o.NodeToNodeAnchor.PUtot, 'node')

                anchorU1 = g_o.getresults(phase, g_o.NodeToNodeAnchor.U1, 'node')
                anchorU2 = g_o.getresults(phase, g_o.NodeToNodeAnchor.U2, 'node')

                anchorForce2D = g_o.getresults(phase, g_o.NodeToNodeAnchor.AnchorForce2D, 'node')

                for x, y, ux, uy, ut, pux, puy, put, u1, u2, f2D in zip(
                        anchorX, anchorY, anchorUx, anchorUy, anchorUt, anchorPUx, anchorPUy, anchorPUt, anchorU1, anchorU2, anchorForce2D):
                    # add filters in here if necessary
                    aPhaseName.append(phase.Name.value)
                    aPhaseIdent.append(phase.Identification.value)
                    aX.append(x)
                    aY.append(y)
                    aUx.append(ux)
                    aUy.append(uy)
                    aUt.append(ut)
                    aPUx.append(pux)
                    aPUy.append(puy)
                    aPUt.append(put)
                    aU1.append(u1)
                    aU2.append(u2)
                    aForce2D.append(f2D)
            except:
                 print ('Exception reading  NodeToNodeAnchor in phase' + phase.Name.value, phase.Identification.value)
        if fileOut:
            print('Outputing to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines(
                    ["Phase, Indent, X(m),Y(m),Ux(m),Uy(m},Utot(m),PUx(m),PUy(m},PUtot(m),U1(m),U2(m),N(kN)\n"])
                file.writelines(["{},{},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}\n".format(pname, pident, x, y, ux, uy, ut, pux, puy, put, u1, u2, f2d)
                                 for pname, pident, x, y, ux, uy, ut, pux, puy, put, u1, u2, f2d in zip(aPhaseName, aPhaseIdent, aX, aY, aUx, aUy, aUt, aPUx, aPUy, aPUt, aU1, aU2, aForce2D)])

        print('getNodeToNodeAnchorResults Done')
   
    def getFixedEndAnchorResults(self,
                                 fileOut=None,
                                 sphaseOrder=None,
                                 sphaseStart=None,
                                 sphaseEnd=None
                                 ):

        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)

        if phaseOrder is None:
            print('No phases found for results')
            return -1

        print('FileOut=', fileOut)

        # init data for lists
        aPhaseName = []
        aPhaseIdent = []

        aY = []
        aX = []

        aUx = []
        aUy = []
        aPUx = []
        aPUy = []
        aPUt = []
        aUt = []
        aU1 = []
        aU2 = []
        
        aForce2D = []

        for phase in phaseOrder:

            print('Getting FixedEndAnchor results for ', phase.Name.value)
            try:
                anchorX = g_o.getresults(phase, g_o.FixedEndAnchor.X, 'node')
                anchorY = g_o.getresults(phase, g_o.FixedEndAnchor.Y, 'node')

                anchorUx = g_o.getresults(phase, g_o.FixedEndAnchor.Ux, 'node')
                anchorUy = g_o.getresults(phase, g_o.FixedEndAnchor.Uy, 'node')
                anchorUt = g_o.getresults(phase, g_o.FixedEndAnchor.Utot, 'node')

                anchorPUx = g_o.getresults(phase, g_o.FixedEndAnchor.PUx, 'node')
                anchorPUy = g_o.getresults(phase, g_o.FixedEndAnchor.PUy, 'node')
                anchorPUt = g_o.getresults(phase, g_o.FixedEndAnchor.PUtot, 'node')

                anchorU1 = g_o.getresults(phase, g_o.FixedEndAnchor.U1, 'node')
                anchorU2 = g_o.getresults(phase, g_o.FixedEndAnchor.U2, 'node')

                anchorForce2D = g_o.getresults(phase, g_o.FixedEndAnchor.AnchorForce2D, 'node')
                
                print('Retrieved FixedEndAnchor results for ', phase.Name.value)
          
                for x, y, ux, uy, ut, pux, puy, put, u1, u2, f2D in zip(
                        anchorX, anchorY, anchorUx, anchorUy, anchorUt, anchorPUx, anchorPUy, anchorPUt, anchorU1, anchorU2, anchorForce2D):
                    # add filters in here if necessary
                    aPhaseName.append(phase.Name.value)
                    aPhaseIdent.append(phase.Identification.value)
                    aX.append(x)
                    aY.append(y)
                    aUx.append(ux)
                    aUy.append(uy)
                    aUt.append(ut)
                    aPUx.append(pux)
                    aPUy.append(puy)
                    aPUt.append(put)
                    aU1.append(u1)
                    aU2.append(u2)
                    aForce2D.append(f2D)
            except:
                print ('Exception reading  FixedEndAnchor in phase' + phase.Name.value)
        if fileOut:
            print('Outputing to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines(
                    ["Phase, Indent, X(m),Y(m),Ux(m),Uy(m},Utot(m),PUx(m),PUy(m},PUtot(m),U1(m),U2(m),N(kN)\n"])
                file.writelines(["{},{},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}\n".format(pname, pident, x, y, ux, uy, ut, pux, puy, put, u1, u2, f2d)
                                 for pname, pident, x, y, ux, uy, ut, pux, puy, put, u1, u2, f2d in zip(aPhaseName, aPhaseIdent, aX, aY, aUx, aUy, aUt, aPUx, aPUy, aPUt, aU1, aU2, aForce2D)])

        print('getFixedEndAnchorResults Done')

    def getInterfaceResults(self,
                    fileOut=None,
                    sphaseOrder=None,
                    sphaseStart=None,
                    sphaseEnd=None
                    ):
        self.setPhaseOrder(sphaseOrder,
           sphaseStart,
           sphaseEnd)
        if phaseOrder is None:
            print('No phases found for results')
            return -1

        print('FileOut=', fileOut)
        # init data for lists
        iPhaseName = []
        iPhaseIdent = []

        iY = []
        iX = []

        iUx = []
        iUy = []
        iUt = []

        iPUx = []
        iPUy = []
        iPUt = []

        iU1 = []
        iU2 = []

        iEffNormalStress = []
        iTotNormalStress = []
        iShearStress = []
        iRelShearStress = []

        iPExcess = []
        iPActive = []
        iPSteady = []
        iPWater = []
        
        iSuction = []
        iEffSuction = []

        for phase in phaseOrder:

            print('Getting Interface results for Phase ', phase.Name.value)
            try:
                interX = g_o.getresults(phase, g_o.Interface.X, 'node')
                interY = g_o.getresults(phase, g_o.Interface.Y, 'node')

                interUx = g_o.getresults(phase, g_o.Interface.Ux, 'node')
                interUy = g_o.getresults(phase, g_o.Interface.Uy, 'node')
                interUt = g_o.getresults(phase, g_o.Interface.Utot, 'node')

                interPUx = g_o.getresults(phase, g_o.Interface.PUx, 'node')
                interPUy = g_o.getresults(phase, g_o.Interface.PUy, 'node')
                interPUt = g_o.getresults(phase, g_o.Interface.PUtot, 'node')

                interU1 = g_o.getresults(phase, g_o.Interface.U1, 'node')
                interU2 = g_o.getresults(phase, g_o.Interface.U2, 'node')

                interEffNormalStress = g_o.getresults(phase, g_o.Interface.InterfaceEffectiveNormalStress, 'node')
                interTotNormalStress = g_o.getresults(phase, g_o.Interface.InterfaceTotalNormalStress, 'node')
                interShearStress = g_o.getresults(phase, g_o.Interface.InterfaceShearStress, 'node')
                interRelShearStress = g_o.getresults(phase, g_o.Interface.InterfaceRelativeShearStress, 'node')

                interPExcess = g_o.getresults(phase, g_o.Interface.PExcess, 'node')
                interPActive = g_o.getresults(phase, g_o.Interface.PActive, 'node')
                interPSteady = g_o.getresults(phase, g_o.Interface.PSteady, 'node')
                interPWater = g_o.getresults(phase, g_o.Interface.PWater, 'node')
                
                interSuction = g_o.getresults(phase, g_o.Interface.Suction, 'node')
                interEffSuction = g_o.getresults(phase, g_o.Interface.EffSuction, 'node')

                for x, y, ux, uy, ut, pux, puy, put, u1, u2, ens, tns, ss, rss, pe, pa, pst, pw, su, esu in zip(
                        interX, interY, 
                        interUx, interUy, interUt, 
                        interPUx, interPUy, interPUt, 
                        interU1, interU2, 
                        interEffNormalStress, interTotNormalStress, interShearStress, interRelShearStress,
                        interPExcess, interPActive, interPSteady, interPWater, 
                        interSuction,  interEffSuction):
                    # add filters in here if necessary
                    iPhaseName.append(phase.Name.value)
                    iPhaseIdent.append(phase.Identification.value)
                    iX.append(x)
                    iY.append(y)
                    iUx.append(ux)
                    iUy.append(uy)
                    iUt.append(ut)
                    iPUx.append(pux)
                    iPUy.append(puy)
                    iPUt.append(put)
                    iU1.append(u1)
                    iU2.append(u2)
                    iEffNormalStress.append(ens)
                    iTotNormalStress.append(tns)
                    iShearStress.append(ss)
                    iRelShearStress.append(rss)
                    iPExcess.append(pe)
                    iPActive.append(pa)
                    iPSteady.append(pst)
                    iPWater.append(pw)
                    iSuction.append(su)
                    iEffSuction.append(esu)
            except:
                print ('Exception reading Interface results in phase' + phase.Name.value)
        if fileOut:
            print('Outputing to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines(
                    ["Phase, Phase Identification, X(m),Y(m),Ux(m),Uy(m},Utot(m), PUx(m), PUy(m), PUt(m), U1(m),U2(m), Eff.NormalStress (kPa), Tot. Normal Stress (kPa),Shear Stress (kPa), Rel. Shear Stress (kPa), Excess Porewater (kPa), Active Porewater (kPa), Steady Porewater (kPa), Suction Porewater (kPa), Porewater (kPa), Effective Suction Porewater (kPa) \n"])
                file.writelines(["{},{},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}\n".format(pname, pident, x, y, ux, uy, ut, pux, puy, put, u1, u2, ens, tns, ss, rss, pe, pa, pst, pw, su, esu)
                                 for pname, pident, x, y, ux, uy, ut, pux, puy, put, u1, u2, ens, tns, ss, rss, pe, pa, pst, pw, su, esu 
                                 in zip(iPhaseName, iPhaseIdent, iX, iY, iUx, iUy, iUt, iPUx, iPUy, iPUt, iU1, iU2, iEffNormalStress, iTotNormalStress, iShearStress, iRelShearStress, iPExcess, iPActive, iPSteady, iPWater, iSuction, iEffSuction)])

        print('getInterfaceResults Done')   
        
    def getAllStructuralResults(self,
                    folderOut=None,
                    sphaseOrder=None,
                    sphaseStart=None,
                    sphaseEnd=None
                    ):    
    
        self.getPlateResults (fileOut = folderOut + r'\getPlateResults.csv',
                       sphaseOrder=sphaseOrder,
                       sphaseStart=sphaseStart,
                       sphaseEnd=sphaseEnd
                       )
                     
        self.getEmbeddedBeamRowResults (fileOut = folderOut + r'\getEmbeddedBeamRowResults.csv',
                       sphaseOrder=sphaseOrder,
                       sphaseStart=sphaseStart,
                       sphaseEnd=sphaseEnd
                       )

        self.getNodeToNodeAnchorResults (fileOut = folderOut + r'\getNodeToNodeAnchorResults.csv',
                       sphaseOrder=sphaseOrder,
                       sphaseStart=sphaseStart,
                       sphaseEnd=sphaseEnd
                       )

        self.getFixedEndAnchorResults  (fileOut = folderOut + r'\getFixedEndAnchorResults.csv',
                       sphaseOrder=sphaseOrder,
                       sphaseStart=sphaseStart,
                       sphaseEnd=sphaseEnd
                      )
        self.getInterfaceResults (fileOut = folderOut + r'\getInterfaceResults.csv',
                       sphaseOrder=sphaseOrder,
                       sphaseStart=sphaseStart,
                       sphaseEnd=sphaseEnd
                      )
                  
class Plaxis3dResults (PlaxisScripting):
#   file:///C:/Program%20Files/Plaxis/PLAXIS%203D/Manuals/English/output_objects/contents.html
    def getSoilResultsByRange(self,
                              fileOut=None,
                              sphaseOrder=None,
                              sphaseStart=None,
                              sphaseEnd=None,
                              xMin=0.0, xMax=0.0,
                              yMin=0.0, yMax=0.0,
                              zMin=0.0, zMax=0.0,
                              Output="stress, displacement,pwp"
                              ):

        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)

        if phaseOrder is None:
            print('No phases found for results')
            return -1
        
        PhaseName = []
        PhaseIdent = []
        
        locY = []
        locX = []
        locZ = []

        Uyy = []
        Uxx = []
        Uzz = []
        Utot = []
        
        PUyy = []
        PUxx = []
        PUzz = []
        PUtot = []
        
        EffSxx = []
        EffSyy = []
        EffSzz = []
        
        EffP1 = []
        EffP2 = []
        EffP3 = []
        
        pExcess = []
        pActive = []    
        pSteady = []
        pWater = []
        
        phasenames = []

        # look into all phases, all steps
        for phase in phaseOrder:
        
            print('Getting soil results for Phase ', phase.Name.value)
        
            soilX = g_o.getresults(phase, g_o.ResultTypes.Soil.X, 'node')
            soilY = g_o.getresults(phase, g_o.ResultTypes.Soil.Y, 'node')
            soilZ = g_o.getresults(phase, g_o.ResultTypes.Soil.Z, 'node')
            
            print('Coordinates retrieved for Phase ', phase.Name.value)
            if "displacement" in Output:
                soilUx = g_o.getresults(phase, g_o.ResultTypes.Soil.Ux, 'node')
                soilUy = g_o.getresults(phase, g_o.ResultTypes.Soil.Uy, 'node')
                soilUz = g_o.getresults(phase, g_o.ResultTypes.Soil.Uz, 'node')
                soilUtot = g_o.getresults(phase, g_o.ResultTypes.Soil.Utot, 'node')
                
                soilPUx = g_o.getresults(phase, g_o.ResultTypes.Soil.PUx, 'node')
                soilPUy = g_o.getresults(phase, g_o.ResultTypes.Soil.PUy, 'node')
                soilPUz = g_o.getresults(phase, g_o.ResultTypes.Soil.PUz, 'node')
                soilPUtot = g_o.getresults(phase, g_o.ResultTypes.Soil.PUtot, 'node') 
                print('Displacments retrieved for Phase ', phase.Name.value)
            if "stress" in Output:
                soilEffSxx = g_o.getresults(phase, g_o.ResultTypes.Soil.SigxxE, 'node')
                soilEffSyy = g_o.getresults(phase, g_o.ResultTypes.Soil.SigyyE, 'node')
                soilEffSzz = g_o.getresults(phase, g_o.ResultTypes.Soil.SigzzE, 'node')
                
                soilEffP1= g_o.getresults(phase, g_o.ResultTypes.Soil.SigmaEffective1, 'node')
                soilEffP2 = g_o.getresults(phase, g_o.ResultTypes.Soil.SigmaEffective2, 'node')
                soilEffP3 = g_o.getresults(phase, g_o.ResultTypes.Soil.SigmaEffective3, 'node')  
                print('Stresses retrieved for Phase ', phase.Name.value)
            if "pwp" in Output:
                soilPExcess = g_o.getresults(phase, g_o.ResultTypes.Soil.PExcess, 'node')
                soilPActive = g_o.getresults(phase, g_o.ResultTypes.Soil.PActive, 'node')
                soilPSteady = g_o.getresults(phase, g_o.ResultTypes.Soil.PSteady, 'node')
                soilPWater = g_o.getresults(phase, g_o.ResultTypes.Soil.PWater, 'node')
                print('PWP retrieved for Phase ', phase.Name.value)
            
            print('Preparing to cycle through results for nodes within range...x(', xMin, xMax, ') y(', yMin, yMax,') z (', zMin, zMax ,')')
            
            if "displacement" in Output and "stress" in Output and "pwp" in Output: 
                for x, y, z, ux, uy, uz, utot, pux, puy, puz, putot, esxx, esyy, eszz, ep1, ep2, ep3, pex, pact, pst, pw in zip(
                        soilX, soilY, soilZ, soilUx, soilUy, soilUz, soilUtot, soilPUx, soilPUy, soilPUz, soilPUtot, soilEffSxx, soilEffSyy, soilEffSzz, soilEffP1, soilEffP2, soilEffP3,soilPExcess, soilPActive, soilPSteady, soilPWater):
                
                    if xMin < x < xMax:
                        if yMin < y < yMax:
                            if zMin < z < zMax:
                                print('Adding Results for',x,y,z)
                  
                                PhaseName.append(phase.Name.value)
                                PhaseIdent.append(phase.Identification.value)
                                
                                locX.append(x)
                                locY.append(y)
                                locZ.append(z)

                                Uxx.append(ux)
                                Uyy.append(uy)
                                Uzz.append(uz)
                                Utot.append(utot)
                                 
                                PUxx.append(pux)
                                PUyy.append(puy)
                                PUzz.append(puz)
                                PUtot.append(putot)

                                EffSxx.append(esxx)
                                EffSyy.append(esyy)
                                EffSzz.append(eszz)
                             
                                EffP1.append(esxx)
                                EffP2.append(esyy)
                                EffP3.append(eszz)
                                

                                pExcess.append(pex)
                                pActive.append(pact) 
                                pSteady.append(pst)
                                pWater.append(pw)
                if fileOut:
                        with open(fileOut, "w") as file:
                                 file.writelines(
                            ["Phase, Phase Identification, X(m), Y(m), Z(m), Ux(m}, Uy(m), Uz(m), Utot(m), PUx(m}, PUy(m), PUz(m), PUtot(m), SigxxE(kPa), SigyyE(kPa), SigzzE(kPa), SigEff1(kPa), SigEff2(kPa), SigEff3(kPa), pExcess(kPa), pActive(kPa), pSteady(kPa), pWater(kPa)\n"])
                        file.writelines(["{},{},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}\n".format(pName, pIdent, x, y, z, ux, uy, uz, utot, pux, puy, puz, put, esxx, esyy, eszz, ep1, ep2, ep3, pex, pact, pst, pw)
                                          for pName, pIdent, x, y, z, ux, uy, uz, utot, pux, puy, puz, put, esxx, esyy, eszz, ep1, ep2, ep3, pex, pact, pst, pw in zip(PhaseName, PhaseIdent, locX, locY, locZ, Uxx, Uyy, Uzz, Utot, PUxx, PUyy, PUzz, PUtot, EffSxx, EffSyy, EffSzz, EffP1, EffP2, EffP3, pExess, pActive, pSteady, pWater)])
                
            if "displacement" in Output and not "stress" in Output and not "pwp" in Output: 
                for x, y, z, ux, uy, uz, utot, pux, puy, puz, dutot in zip(
                        soilX, soilY, soilZ, soilUx, soilUy, soilUz, soilUtot, soilPUx, soilPUy, soilPUz, soilPUtot):
                    print (x, y, z)
                    if xMin < x < xMax:
                        if yMin < y < yMax:
                            if zMin < z < zMax:
                                print('Adding Results for',x,y,z)
                  
                                PhaseName.append(phase.Name.value)
                                PhaseIdent.append(phase.Identification.value)
                                
                                locX.append(x)
                                locY.append(y)
                                locZ.append(z)

                                Uxx.append(ux)
                                Uyy.append(uy)
                                Uzz.append(uz)
                                Utot.append(utot)
                                 
                                PUxx.append(pux)
                                PUyy.append(puy)
                                PUzz.append(puz)
                                PUtot.append(putot)  
                                
                if fileOut:
                    with open(fileOut, "w") as file:
                        file.writelines(["{},{},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}\n".format(pName, pIdent, x, y, z, ux, uy, uz, utot, pux, puy, puz, putot)
                            for x, y, z, ux, uy, uz, utot, pux, puy, puz, dutot in zip(PhaseName, PhaseIdent, locX, locY, locZ, Uxx, Uyy, Uzz, Utot, PUxx, PUyy, PUzz, PUtot)])
    
    def getSoilResultsByRange2(self,
                              fileOut=None,
                              sphaseOrder=None,
                              sphaseStart=None,
                              sphaseEnd=None,
                              Output="stress, displacement,pwp",
                              xMin=0.0, xMax=0.0,
                              yMin=0.0, yMax=0.0,
                              zMin=0.0, zMax=0.0,
                              ):
                              
        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)

        phaseName = []
        phaseIdent = []
        
        locY = []
        locX = []
        locZ = []

        Uyy = []
        Uxx = []
        Uzz = []
        Utot = []
        
        PUyy = []
        PUxx = []
        PUzz = []
        PUtot = []
        
        self.setNodeList (xMin, xMax,
                          yMin, yMax,
                          zMin, zMax)
       
        for phase in phaseOrder:
            
            print('retrieving results for ', phase.Name.value)  

            for pt in NodeList:
                ux = g_o.getsingleresult(phase, g_o.Soil.Ux, (pt.x, pt.y, pt.z))
                uy = g_o.getsingleresult(phase, g_o.Soil.Uy, (pt.x, pt.y, pt.z))
                uz = g_o.getsingleresult(phase, g_o.Soil.Uz, (pt.x, pt.y, pt.z))
                utot = g_o.getsingleresult(phase, g_o.Soil.Utot, (pt.x, pt.y, pt.z))
                
                pux = g_o.getsingleresult(phase, g_o.Soil.PUx, (pt.x, pt.y, pt.z))
                puy = g_o.getsingleresult(phase, g_o.Soil.PUy, (pt.x, pt.y, pt.z))
                puz = g_o.getsingleresult(phase, g_o.Soil.PUz, (pt.x, pt.y, pt.z))
                putot = g_o.getsingleresult(phase, g_o.Soil.PUtot, (pt.x, pt.y, pt.z)) 
                
                # sxx = g_o.getsingleresult(phase, g_o.Soil.SigxxE, (pt.x, pt.y, pt.z))
                # syy = g_o.getsingleresult(phase, g_o.Soil.SigyyE, (pt.x, pt.y, pt.z))
                # szz = g_o.getsingleresult(phase, g_o.Soil.SigzzE, (pt.x, pt.y, pt.z))
                # xpwp = g_o.getsingleresult(phase, g_o.Soil.PExcess, (pt.x, pt.y, pt.z))
                
                print('results for ', phase.Name.value, pt.x, pt.y, pt.z ,' retrieved')
                phaseName.append(phase.Name.value)
                phaseIdent.append(phase.Identification.value)
              
                locX.append (pt.x)
                locY.append (pt.y)
                locZ.append (pt.z)
                
                Uxx.append (ux)
                Uyy.append (uy)
                Uzz.append (uz)
                Utot.append (utot)
                
                PUxx.append (pux)
                PUyy.append (puy)
                PUzz.append (puy)
                PUtot.append (putot)
              
        if fileOut:
            with open(fileOut, "w") as file:
                file.writelines(["{},{},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}\n".format(pName, pIdent, x, y, z, ux, uy, uz, utot, pux, puy, puz, putot)
                for x, y, z, ux, uy, uz, utot, pux, puy, puz, putot in zip(PhaseName, PhaseIdent, locX, locY, locZ, Uxx, Uyy, Uzz, Utot, PUxx, PUyy, PUzz, dUtot)])
        print("end")
        file.close                  
                          
    def getSoilResultsByPoints(self,
                               filePoints=None,
                               fileOut=None,
                               sphaseOrder=None,
                               sphaseStart=None,
                               sphaseEnd=None,
                               ):
        getSoilResultsByPoints_Displacements(self,
                               filePoints=None,
                               fileOut=None,
                               sphaseOrder=None,
                               sphaseStart=None,
                               sphaseEnd=None,
                               )                           
    def getSoilResultsByPoints_Displacements(self,
                               filePoints=None,
                               fileOut=None,
                               sphaseOrder=None,
                               sphaseStart=None,
                               sphaseEnd=None,
                               ):

        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)

        self.loadNodeList(filePoints)
        
        
        phaseName = []
        phaseIdent = []
        
        locName = []
        locY = []
        locX = []
        locZ = []

        Uyy = []
        Uxx = []
        Uzz = []
        Utot = []
        
        PUyy = []
        PUxx = []
        PUzz = []
        PUtot = []
        
        Epsyy = []
        Epsxx = []
        Epszz = []

            
        for phase in phaseOrder:
            print(phase.Name.value)
    
            for pt in NodeList:
            
                ux = g_o.getsingleresult(phase, g_o.Soil.Ux, (pt.x, pt.y, pt.z))
                uy = g_o.getsingleresult(phase, g_o.Soil.Uy, (pt.x, pt.y, pt.z))
                uz = g_o.getsingleresult(phase, g_o.Soil.Uz, (pt.x, pt.y, pt.z))
                utot = g_o.getsingleresult(phase, g_o.Soil.Utot, (pt.x, pt.y, pt.z))
                
                pux = g_o.getsingleresult(phase, g_o.Soil.PUx, (pt.x, pt.y, pt.z))
                puy = g_o.getsingleresult(phase, g_o.Soil.PUy, (pt.x, pt.y, pt.z))
                puz = g_o.getsingleresult(phase, g_o.Soil.PUz, (pt.x, pt.y, pt.z))
                putot = g_o.getsingleresult(phase, g_o.Soil.PUtot, (pt.x, pt.y, pt.z)) 
                
                ex = g_o.getsingleresult(phase, g_o.Soil.Epsxx, (pt.x, pt.y, pt.z))
                ey = g_o.getsingleresult(phase, g_o.Soil.Epsyy, (pt.x, pt.y, pt.z))
                ez = g_o.getsingleresult(phase, g_o.Soil.Epszz, (pt.x, pt.y, pt.z))
                
                if ux != 'not found':
                    print('results for ', phase.Name.value, pt.x, pt.y, pt.z ,' retrieved')
                
                    phaseName.append(phase.Name.value)
                    phaseIdent.append(phase.Identification.value)
                
                    locName.append (pt.name)
                    locX.append (pt.x)
                    locY.append (pt.y)
                    locZ.append (pt.z)
                
                    Uxx.append (ux)
                    Uyy.append (uy)
                    Uzz.append (uz)
                    Utot.append (utot)
                
                    PUxx.append (pux)
                    PUyy.append (puy)
                    PUzz.append (puz)
                    PUtot.append (putot)
                
                    Epsxx.append (ex)
                    Epsyy.append (ey)
                    Epszz.append (ez)
              
                
        if fileOut:
            with open(fileOut, "w") as file:
                file.writelines(["PhaseName, PhaseId, locName, locX(m), locY(m), locZ(m), Ux(m), Uy(m), Uz(m), Utot(m), PUx(m), PUy(m), PUz(m), PUtot(m), Epsxx, Epsyy, Epszz\n"])
                file.writelines(["{},{},{},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f}\n".format(pName, pIdent,locname, float(x), float(y), float(z), float(ux), float(uy), float(uz), float(utot), float(pux), float(puy), float(puz), float(putot), float(ex), float(ey), float(ez))
                for pName, pIdent, locname, x, y, z, ux, uy, uz, utot, pux, puy, puz, putot, ex, ey, ez in zip(phaseName, phaseIdent, locName, locX, locY, locZ, Uxx, Uyy, Uzz, Utot, PUxx, PUyy, PUzz, PUtot, Epsxx, Epsyy, Epszz)])
        print("end")
        file.close
    def getSoilResultsByPoints_Stresses(self,
                               filePoints=None,
                               fileOut=None,
                               sphaseOrder=None,
                               sphaseStart=None,
                               sphaseEnd=None,
                               ):

        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)

        self.loadNodeList(filePoints)
        
        
        phaseName = []
        phaseIdent = []
        
        locName = []
        locY = []
        locX = []
        locZ = []

        Uyy = []
        Uxx = []
        Uzz = []
        Utot = []
        
        SigxxT = []
        SigyyT = []
        SigzzT = []
        
        Sigxy = []
        Sigyz = []
        Sigzx = []

            
        for phase in phaseOrder:
            print(phase.Name.value)
    
            for pt in NodeList:
            
                ux = g_o.getsingleresult(phase, g_o.Soil.Ux, (pt.x, pt.y, pt.z))
                uy = g_o.getsingleresult(phase, g_o.Soil.Uy, (pt.x, pt.y, pt.z))
                uz = g_o.getsingleresult(phase, g_o.Soil.Uz, (pt.x, pt.y, pt.z))
                utot = g_o.getsingleresult(phase, g_o.Soil.Utot, (pt.x, pt.y, pt.z))
                
                sig_xxt = g_o.getsingleresult(phase, g_o.Soil.SigxxT, (pt.x, pt.y, pt.z))
                sig_yyt = g_o.getsingleresult(phase, g_o.Soil.SigyyT, (pt.x, pt.y, pt.z))
                sig_zzt = g_o.getsingleresult(phase, g_o.Soil.SigzzT, (pt.x, pt.y, pt.z))
                            
                sig_xy = g_o.getsingleresult(phase, g_o.Soil.Sigxy, (pt.x, pt.y, pt.z))
                sig_yz = g_o.getsingleresult(phase, g_o.Soil.Sigyz, (pt.x, pt.y, pt.z))
                sig_zx = g_o.getsingleresult(phase, g_o.Soil.Sigzx, (pt.x, pt.y, pt.z))
                
                if ux != 'not found':
                    print('results for ', phase.Name.value, pt.x, pt.y, pt.z ,' retrieved')
                
                    phaseName.append(phase.Name.value)
                    phaseIdent.append(phase.Identification.value)
                
                    locName.append (pt.name)
                    locX.append (pt.x)
                    locY.append (pt.y)
                    locZ.append (pt.z)
                
                    Uxx.append (ux)
                    Uyy.append (uy)
                    Uzz.append (uz)
                    Utot.append (utot)
                
                    SigxxT.append (sig_xxt)
                    SigyyT.append (sig_yyt)
                    SigzzT.append (sig_zzt)
                
                    Sigxy.append (sig_xy)
                    Sigyz.append (sig_yz)
                    Sigzx.append (sig_zx)
              
                
        if fileOut:
            with open(fileOut, "w") as file:
                file.writelines(["PhaseName, PhaseId, locName, locX(m), locY(m), locZ(m), Ux(m), Uy(m), Uz(m), Utot(m), SigxxT(m), SigyyT(m), SigzzT(m), Sigxy, Sigyz, Sigzx\n"])
                file.writelines(["{},{},{},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f}\n".format(pName, pIdent,locname, float(x), float(y), float(z), float(ux), float(uy), float(uz), float(utot), float(sig_xxt), float(sig_yyt), float(sig_zzt), float(sig_xy), float(sig_yz), float(sig_zx))
                for pName, pIdent, locname, x, y, z, ux, uy, uz, utot, sig_xxt, sig_yyt, sig_zzt, sig_xy, sig_yz, sig_zx in zip(phaseName, phaseIdent, locName, locX, locY, locZ, Uxx, Uyy, Uzz, Utot, SigxxT, SigyyT, SigzzT, Sigxy, Sigyz, Sigzx)])
        print("end")
        file.close
    def getPlateResults(self,
                        fileOut=None,
                        sphaseOrder=None,
                        sphaseStart=None,
                        sphaseEnd=None
                        ):

        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)

        if phaseOrder is None:
            print('No phases found for results')
            return -1

        print('FileOut=', fileOut)

        # initialise data for lists
        pPhaseName = []
        pPhaseIdent = []
           
        pY = []
        pX = []
        pZ = []
        pMat = []
        
        pUx = []
        pUy = []
        pUz = []
        pUt = []

        pPUx = []
        pPUy = []
        pPUz = []
        pPUt = []

        pU1 = []
        pU2 = []
        pU3 = []
        
        pM11 = []
        pM22 = []
        pM12 = []
        
        pQ12 = []
        pQ23 = [] 
        pQ13 = []
        
        pN1 = []
        pN2 = []



        for phase in phaseOrder:
            print('Getting Plate results for Phase ', phase.Name.value, phase.Identification.value)
            
            try: 
                plateX = g_o.getresults(phase, g_o.Plate.X, 'node')
                plateY = g_o.getresults(phase, g_o.Plate.Y, 'node')
                plateZ = g_o.getresults(phase, g_o.Plate.Z, 'node')
                plateMat = g_o.getresults(phase, g_o.Plate.MaterialID, 'node')
                
                plateUx = g_o.getresults(phase, g_o.Plate.Ux, 'node')
                plateUy = g_o.getresults(phase, g_o.Plate.Uy, 'node')
                plateUz = g_o.getresults(phase, g_o.Plate.Uz, 'node')
                plateUt = g_o.getresults(phase, g_o.Plate.Utot, 'node')

                platePUx = g_o.getresults(phase, g_o.Plate.PUx, 'node')
                platePUy = g_o.getresults(phase, g_o.Plate.PUy, 'node')
                platePUz = g_o.getresults(phase, g_o.Plate.PUz, 'node')
                platePUt = g_o.getresults(phase, g_o.Plate.PUtot, 'node')

                plateU1 = g_o.getresults(phase, g_o.Plate.U1, 'node')
                plateU2 = g_o.getresults(phase, g_o.Plate.U2, 'node')
                plateU3 = g_o.getresults(phase, g_o.Plate.U3, 'node')
                
                plateN1 = g_o.getresults(phase, g_o.Plate.N11, 'node')
                plateN2 = g_o.getresults(phase, g_o.Plate.N22, 'node')                
                plateQ12 = g_o.getresults(phase, g_o.Plate.Q12, 'node')
                plateQ23 = g_o.getresults(phase, g_o.Plate.Q23, 'node')
                plateQ13 = g_o.getresults(phase, g_o.Plate.Q13, 'node')
                plateM11 = g_o.getresults(phase, g_o.Plate.M11, 'node')
                plateM22 = g_o.getresults(phase, g_o.Plate.M22, 'node')
                plateM12 = g_o.getresults(phase, g_o.Plate.M12, 'node')
                
                for x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n1, n2, q12, q23, q13, m11, m22, m12 in zip(
                        plateX, plateY, plateZ, plateMat, plateUx, plateUy, plateUz, plateUt, platePUx, platePUy, platePUz, platePUt, plateU1, plateU2, plateU3, plateN1, plateN2, plateQ12, plateQ23, plateQ13, plateM11, plateM22, plateM12):
                    # add filters in here if necessary
                    pPhaseName.append(phase.Name.value)
                    pPhaseIdent.append(phase.Identification.value)
                    
                    pX.append(x)
                    pY.append(y)
                    pZ.append(z)
                    pMat.append(mat)
                    
                    pUx.append(ux)
                    pUy.append(uy)
                    pUz.append(uz)
                    pUt.append(ut)
                    
                    pPUx.append(pux)
                    pPUy.append(puy)
                    pPUz.append(puz)
                    pPUt.append(put)
                   
                    pU1.append(u1)
                    pU2.append(u2)
                    pU3.append(u3)
                    
                    pN1.append(n1)
                    pN2.append(n2)
                    pQ12.append(q12)
                    pQ23.append(q23)
                    pQ13.append(q13)
                    pM11.append(m11)                    
                    pM22.append(m22)                  
                    pM12.append(m12) 
            except:
                print ('Exception reading Plate in phase' + phase.Name.value)

        if fileOut:
            print('Outputing to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines(
                    ["Phase Name, Phase Indent, X(m),Y(m), Z(m), Mat, Ux(m), Uy(m), Uz(m), Utot(m), PUx(m), PUy(m), PUz(m), PUt(m), U1(m), U2(m), U3(m), N1(kN/m), N2(kN/m), Q12(kN/m), Q23(kN/m), Q13(kN/m), M11(kNm/m), M22(kNm/m), M12(kNm/m)\n"])
                file.writelines(["{},{},{:2f},{:2f},{:2f},{},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}\n".format(pname, pident, x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n1, n2, q12, q23, q13, m11, m22, m12)
                                 for pname, pident, x, y, z, mat, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n1, n2, q12, q23, q13, m11, m22, m12 in zip(pPhaseName, pPhaseIdent, pX, pY, pZ, pMat, pUx, pUy, pUz, pUt, pPUx, pPUy, pPUz, pPUt, pU1, pU2, pU3, pN1, pN2, pQ12, pQ23, pQ13,pM11, pM22, pM12)])

        print('getPlateResults Done')       
   
    def getEmbeddedBeamResults(self,
                                  fileOut=None,
                                  sphaseOrder=None,
                                  sphaseStart=None,
                                  sphaseEnd=None,
                                  ):
# file:///C:/Program%20Files/Plaxis/PLAXIS%203D/manuals/english/output_objects/objects_EmbeddedBeam.html
        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)

        if phaseOrder is None:
            print('No phases found for results')
            return -1

        print('FileOut=', fileOut)

        # init data for lists
        PhaseName = []
        PhaseIdent = []
           
        eY = []
        eX = []
        eZ = []
        
        eUx = []
        eUy = []
        eUz = []
        eUt = []

        ePUx = []
        ePUy = []
        ePUz = []
        ePUt = []

        eU1 = []
        eU2 = []
        eU3 = []
        
        eN = []
        eQ12 = []
        eQ13 = []
        eM2 = []
        eM3 = []

        eTskin = []
        eTlat = []
        eTlat2 = []
        eFfoot = []
        
        for phase in phaseOrder:

            print('Getting EmbeddedBeam results for Phase ',  phase.Name.value)
            
            try:
                embeamX = g_o.getresults(phase, g_o.EmbeddedBeam.X, 'node')
                embeamY = g_o.getresults(phase, g_o.EmbeddedBeam.Y, 'node')
                embeamZ = g_o.getresults(phase, g_o.EmbeddedBeam.Z, 'node')
                #print('Retrieved U')
                embeamUx = g_o.getresults(phase, g_o.EmbeddedBeam.Ux, 'node')
                embeamUy = g_o.getresults(phase, g_o.EmbeddedBeam.Uy, 'node')
                embeamUz = g_o.getresults(phase, g_o.EmbeddedBeam.Uz, 'node')
                embeamUt = g_o.getresults(phase, g_o.EmbeddedBeam.Utot, 'node')
                #print('Retrieved U')
                embeamPUx = g_o.getresults(phase, g_o.EmbeddedBeam.PUx, 'node')
                embeamPUy = g_o.getresults(phase, g_o.EmbeddedBeam.PUy, 'node')
                embeamPUz = g_o.getresults(phase, g_o.EmbeddedBeam.PUz, 'node')
                embeamPUt = g_o.getresults(phase, g_o.EmbeddedBeam.PUtot, 'node')
                #print('Retrieved dU')
                embeamU1 = g_o.getresults(phase, g_o.EmbeddedBeam.U1, 'node')
                embeamU2 = g_o.getresults(phase, g_o.EmbeddedBeam.U2, 'node')
                embeamU3 = g_o.getresults(phase, g_o.EmbeddedBeam.U3, 'node')
                #print('Retrieved U1-U3')
                embeamN = g_o.getresults(phase, g_o.EmbeddedBeam.N, 'node')
                embeamQ12 = g_o.getresults(phase, g_o.EmbeddedBeam.Q12, 'node')
                embeamQ13 = g_o.getresults(phase, g_o.EmbeddedBeam.Q13, 'node')
                embeamM2 = g_o.getresults(phase, g_o.EmbeddedBeam.M2, 'node')
                embeamM3 = g_o.getresults(phase, g_o.EmbeddedBeam.M3, 'node')
                #print('Retrieved N')
                embeamTskin = g_o.getresults(phase, g_o.EmbeddedBeam.Tskin, 'node')
                embeamTlat= g_o.getresults(phase, g_o.EmbeddedBeam.Tlat, 'node')
                embeamTlat2= g_o.getresults(phase, g_o.EmbeddedBeam.Tlat2, 'node')
                #embeamFfoot= g_o.getresults(phase, g_o.EmbeddedBeam.Tlat2, 'node')
                
                print('Retrieved EmbeddedBeam results for ', phase.Name.value)
                
                for x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3, tskin, tlat, tlat2 in zip(
                        embeamX, embeamY, embeamZ, embeamUx, embeamUy, embeamUz, embeamUt, embeamPUx, embeamPUy,  embeamPUz, embeamPUt, embeamU1, embeamU2, embeamU3, embeamN, embeamQ12, embeamQ13, embeamM2, embeamM3, embeamTskin, embeamTlat, embeamTlat2):
                    # add filters in here if necessary
                    PhaseName.append(phase.Name.value)
                    PhaseIdent.append(phase.Identification.value)
                    eX.append(x)
                    eY.append(y)
                    eZ.append(z)
                    eUx.append(ux)
                    eUy.append(uy)
                    eUz.append(uz)
                    eUt.append(ut)
                    ePUx.append(pux)
                    ePUy.append(puy)
                    ePUz.append(puz)
                    ePUt.append(put)
                    eU1.append(u1)
                    eU2.append(u2)
                    eU3.append(u3)
                    eN.append(n)  
                    eQ12.append(q12)
                    eQ13.append(q13)
                    eM2.append(m2)
                    eM3.append(m3)
                    eTskin.append(tskin)
                    eTlat.append(tlat)
                    eTlat2.append(tlat2)
            except:
                print ('Exception reading EmbeddedBeam in phase' + phase.Name.value)
        if fileOut:
            print('Outputing to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines(
                    ["Phase, PhaseIdent, X(m), Y(m), Z(m), Ux(m), Uy(m}, Uz(m), Utot(m), PUx(m), PUy(m), PUz(m), PUt(m), U1(m), U2(m), U3(m), N(kN), Q12(kN/m), Q13(kN/m), M2(kNm/m), M3(kN/m), Tskin(kN/m), Tlat(kN/m), Tlat2(kN/m)\n"])
                file.writelines(["{},{},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}\n".format(pname, pident, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3, tskin, tlat, tlat2)
                                 for pname, pident, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, n, q12, q13, m2, m3, tskin, tlat, tlat2 in zip(PhaseName, PhaseIdent, eX, eY, eZ, eUx, eUy, eUz, eUt, ePUx, ePUy, ePUz, ePUt, eU1, eU2, eU3, eN, eQ12, eQ13, eM2, eM3, eTskin, eTlat, eTlat2)])

        print('getEmbeddedBeamResults Done')
        
    def getNodeToNodeAnchorResults(self,
                                   fileOut=None,
                                   sphaseOrder=None,
                                   sphaseStart=None,
                                   sphaseEnd=None,
                                   ):
        #file:///C:/Program%20Files/Plaxis/PLAXIS%203D/manuals/english/output_objects/objects_NodeToNodeAnchor.html
        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)

        if phaseOrder is None:
            print('No phases found for results')
            return -1

        print('FileOut=', fileOut)

        # initialize data for lists
        aPhaseName = []
        aPhaseIdent = []
        
        aY = []
        aX = []
        aZ = []
        
        aUx = []
        aUy = []
        aUz = []
        aUt = []
        
        aPUx = []
        aPUy = []
        aPUz = []
        aPUt = []
        
        aU1 = []
        aU2 = []
        aU3 = []
        
        aForce3D = []

        for phase in phaseOrder:

            print('Getting NodeToNodeAnchor results for Phase ', phase.Name.value, phase.Identification.value)
            try:
                anchorX = g_o.getresults(phase, g_o.NodeToNodeAnchor.X, 'node')
                anchorY = g_o.getresults(phase, g_o.NodeToNodeAnchor.Y, 'node')
                anchorZ = g_o.getresults(phase, g_o.NodeToNodeAnchor.Z, 'node')
                
                anchorUx = g_o.getresults(phase, g_o.NodeToNodeAnchor.Ux, 'node')
                anchorUy = g_o.getresults(phase, g_o.NodeToNodeAnchor.Uy, 'node')
                anchorUz = g_o.getresults(phase, g_o.NodeToNodeAnchor.Uz, 'node')
                anchorUt = g_o.getresults(phase, g_o.NodeToNodeAnchor.Utot, 'node')

                anchorPUx = g_o.getresults(phase, g_o.NodeToNodeAnchor.PUx, 'node')
                anchorPUy = g_o.getresults(phase, g_o.NodeToNodeAnchor.PUy, 'node')
                anchorPUz = g_o.getresults(phase, g_o.NodeToNodeAnchor.PUz, 'node')
                anchorPUt = g_o.getresults(phase, g_o.NodeToNodeAnchor.PUtot, 'node')

                anchorU1 = g_o.getresults(phase, g_o.NodeToNodeAnchor.U1, 'node')
                anchorU2 = g_o.getresults(phase, g_o.NodeToNodeAnchor.U2, 'node')
                anchorU3 = g_o.getresults(phase, g_o.NodeToNodeAnchor.U3, 'node')
                
                anchorForce3D = g_o.getresults(phase, g_o.NodeToNodeAnchor.AnchorForce3D, 'node')

                for x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, f3D in zip(
                        anchorX, anchorY, anchorZ, anchorUx, anchorUy, anchorUz, anchorUt, anchorPUx, anchorPUy, anchorPUz, anchorPUt, anchorU1, anchorU2, anchorU3, anchorForce3D):
                    # add filters in here if necessary
                    aPhaseName.append(phase.Name.value)
                    aPhaseIdent.append(phase.Identification.value)
                    
                    aX.append(x)
                    aY.append(y)
                    aZ.append(z)
                    
                    aUx.append(ux)
                    aUy.append(uy)
                    aUz.append(uz)
                    aUt.append(ut)
                    
                    aPUx.append(pux)
                    aPUy.append(puy)
                    aPUz.append(puz)
                    aPUt.append(put)
                    
                    aU1.append(u1)
                    aU2.append(u2)
                    aU3.append(u3)   
                    
                    aForce3D.append(f3D)
            except:
                 print ('Exception reading  NodeToNodeAnchor in phase' + phase.Name.value, phase.Identification.value)
        if fileOut:
            print('Outputing to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines(
                    ["Phase, Indent, X(m),Y(m),Z(m),Ux(m),Uy(m},Uz(m),Utot(m),PUx(m), PUy(m}, PUz(m), PUtot(m),U1(m),U2(m),U3(m),N(kN)\n"])
                file.writelines(["{},{},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}\n".format(pname, pident, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, f3d)
                                 for pname, pident, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, f3d in zip(aPhaseName, aPhaseIdent, aX, aY, aZ, aUx, aUy, aUz, aUt, aPUx, aPUy, aPUz, aPUt, aU1, aU2, aU3, aForce3D)])

        print('getNodeToNodeAnchorResults Done')
   
    def getFixedEndAnchorResults(self,
                                 fileOut=None,
                                 sphaseOrder=None,
                                 sphaseStart=None,
                                 sphaseEnd=None
                                 ):
        # file:///C:/Program%20Files/Plaxis/PLAXIS%203D/manuals/english/output_objects/objects_FixedEndAnchor.html
        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)

        if phaseOrder is None:
            print('No phases found for results')
            return -1

        print('FileOut=', fileOut)

        # initialize data for lists
        aPhaseName = []
        aPhaseIdent = []

        aY = []
        aX = []
        aZ = []
        
        aUx = []
        aUy = []
        aUz = []
        aUt = []
        
        aPUx = []
        aPUy = []
        aPUz = []
        aPUt = []
        
        aU1 = []
        aU2 = []
        aU3 = []
        
        aForce3D = []

        for phase in phaseOrder:

            print('Getting FixedEndAnchor results for ', phase.Name.value)
            try:
                anchorX = g_o.getresults(phase, g_o.FixedEndAnchor.X, 'node')
                anchorY = g_o.getresults(phase, g_o.FixedEndAnchor.Y, 'node')
                anchorZ = g_o.getresults(phase, g_o.FixedEndAnchor.Z, 'node')
                
                anchorUx = g_o.getresults(phase, g_o.FixedEndAnchor.Ux, 'node')
                anchorUy = g_o.getresults(phase, g_o.FixedEndAnchor.Uy, 'node')
                anchorUz = g_o.getresults(phase, g_o.FixedEndAnchor.Uz, 'node')
                anchorUt = g_o.getresults(phase, g_o.FixedEndAnchor.Utot, 'node')

                anchorPUx = g_o.getresults(phase, g_o.FixedEndAnchor.PUx, 'node')
                anchorPUy = g_o.getresults(phase, g_o.FixedEndAnchor.PUy, 'node')
                anchorPUz = g_o.getresults(phase, g_o.FixedEndAnchor.PUz, 'node')
                anchorPUt = g_o.getresults(phase, g_o.FixedEndAnchor.PUtot, 'node')

                anchorU1 = g_o.getresults(phase, g_o.FixedEndAnchor.U1, 'node')
                anchorU2 = g_o.getresults(phase, g_o.FixedEndAnchor.U2, 'node')
                anchorU3 = g_o.getresults(phase, g_o.FixedEndAnchor.U3, 'node')
                
                anchorForce3D = g_o.getresults(phase, g_o.FixedEndAnchor.AnchorForce3D, 'node')
                
                print('Retrieved FixedEndAnchor results for ', phase.Name.value)
          
                for x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, f3D in zip(
                        anchorX, anchorY, anchorZ, anchorUx, anchorUy, anchorUz, anchorUt, anchorPUx, anchorPUy, anchorPUz, anchorPUt, anchorU1, anchorU2, anchorU3, anchorForce3D):
                    # add filters in here if necessary
                    aPhaseName.append(phase.Name.value)
                    aPhaseIdent.append(phase.Identification.value)
                    
                    aX.append(x)
                    aY.append(y)
                    aZ.append(z)
                    
                    aUx.append(ux)
                    aUy.append(uy)
                    aUz.append(uz)
                    aUt.append(ut)
                    
                    aPUx.append(pux)
                    aPUy.append(puy)
                    aPUz.append(puz)
                    aPUt.append(put)
                    
                    aU1.append(u1)
                    aU2.append(u2)
                    aU3.append(u3)
                    
                    aForce3D.append(f3D)
            except:
                print ('Exception reading  FixedEndAnchor in phase' + phase.Name.value)
        if fileOut:
            print('Outputing to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines(
                    ["Phase, Indent, X(m),Y(m),Z(m),Ux(m),Uy(m},Uz(m),Utot(m),PUx(m),PUy(m},PUz(m),PUtot(m),U1(m),U2(m),U3(m),N(kN)\n"])
                file.writelines(["{},{},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}\n".format(pname, pident, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, f3d)
                                 for pname, pident, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, f3d in zip(aPhaseName, aPhaseIdent, aX, aY, aZ, aUx, aUy, aUz, aUt, aPUx, aPUy, aPUz, aPUt, aU1, aU2, aU3, aForce3D)])

        print('getFixedEndAnchorResults Done')

    def getInterfaceResults(self,
                    fileOut=None,
                    sphaseOrder=None,
                    sphaseStart=None,
                    sphaseEnd=None
                    ):
        # file:///C:/Program%20Files/Plaxis/PLAXIS%203D/manuals/english/output_objects/objects_Interface.html
        
        self.setPhaseOrder(sphaseOrder,
           sphaseStart,
           sphaseEnd)
        if phaseOrder is None:
            print('No phases found for results')
            return -1

        print('FileOut=', fileOut)
        # initialize data for lists
        iPhaseName = []
        iPhaseIdent = []

        iY = []
        iX = []
        iZ = []
        
        iUx = []
        iUy = []
        iUz = []
        iUt = []

        iPUx = []
        iPUy = []
        iPUz = []
        iPUt = []

        iU1 = []
        iU2 = []
        iU3 = []
        
        iEffNormalStress = []
        iTotNormalStress = []
        iShearStress = []
        iRelShearStress = []

        iPExcess = []
        iPActive = []
        iPSteady = []
        iPWater = []
        
        iSuction = []
        iEffSuction = []

        for phase in phaseOrder:

            print('Getting Interface results for Phase ', phase.Name.value)
            try:
                interX = g_o.getresults(phase, g_o.Interface.X, 'node')
                interY = g_o.getresults(phase, g_o.Interface.Y, 'node')
                interZ = g_o.getresults(phase, g_o.Interface.Z, 'node')
                
                interUx = g_o.getresults(phase, g_o.Interface.Ux, 'node')
                interUy = g_o.getresults(phase, g_o.Interface.Uy, 'node')
                interUz = g_o.getresults(phase, g_o.Interface.Uz, 'node')
                interUt = g_o.getresults(phase, g_o.Interface.Utot, 'node')

                interPUx = g_o.getresults(phase, g_o.Interface.PUx, 'node')
                interPUy = g_o.getresults(phase, g_o.Interface.PUy, 'node')
                interPUz = g_o.getresults(phase, g_o.Interface.PUz, 'node')
                interPUt = g_o.getresults(phase, g_o.Interface.PUtot, 'node')

                interU1 = g_o.getresults(phase, g_o.Interface.U1, 'node')
                interU2 = g_o.getresults(phase, g_o.Interface.U2, 'node')
                interU3 = g_o.getresults(phase, g_o.Interface.U3, 'node')
                
                interEffNormalStress = g_o.getresults(phase, g_o.Interface.InterfaceEffectiveNormalStress, 'node')
                interTotNormalStress = g_o.getresults(phase, g_o.Interface.InterfaceTotalNormalStress, 'node')
                interShearStress = g_o.getresults(phase, g_o.Interface.InterfaceShearStress, 'node')
                interRelShearStress = g_o.getresults(phase, g_o.Interface.InterfaceRelativeShearStress, 'node')

                interPExcess = g_o.getresults(phase, g_o.Interface.PExcess, 'node')
                interPActive = g_o.getresults(phase, g_o.Interface.PActive, 'node')
                interPSteady = g_o.getresults(phase, g_o.Interface.PSteady, 'node')
                interPWater = g_o.getresults(phase, g_o.Interface.PWater, 'node')
                
                interSuction = g_o.getresults(phase, g_o.Interface.Suction, 'node')
                interEffSuction = g_o.getresults(phase, g_o.Interface.EffSuction, 'node')

                for x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, ens, tns, ss, rss, pe, pa, pst, pw, su, esu in zip(
                        interX, interY, interZ,
                        interUx, interUy, interUz, interUt, 
                        interPUx, interPUy, interPUz, interPUt, 
                        interU1, interU2, interU3,
                        interEffNormalStress, interTotNormalStress, interShearStress, interRelShearStress,
                        interPExcess, interPActive, interPSteady, interPWater, 
                        interSuction,  interEffSuction):
                    # add filters in here if necessary
                    
                    iPhaseName.append(phase.Name.value)
                    iPhaseIdent.append(phase.Identification.value)
                    
                    iX.append(x)
                    iY.append(y)
                    
                    iUx.append(ux)
                    iUy.append(uy)
                    iUz.append(uz)
                    iUt.append(ut)
                    
                    iPUx.append(pux)
                    iPUy.append(puy)
                    iPUz.append(puz)
                    iPUt.append(put)
                    
                    iU1.append(u1)
                    iU2.append(u2)
                    iU3.append(u3)
                     
                    iEffNormalStress.append(ens)
                    iTotNormalStress.append(tns)
                    iShearStress.append(ss)
                    iRelShearStress.append(rss)
                    iPExcess.append(pe)
                    iPActive.append(pa)
                    iPSteady.append(pst)
                    iPWater.append(pw)
                    iSuction.append(su)
                    iEffSuction.append(esu)
            except:
                print ('Exception reading Interface results in phase' + phase.Name.value)
        if fileOut:
            print('Outputing to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines(
                    ["Phase, Phase Identification, X(m),Y(m),Z(m),Ux(m),Uy(m},Uz(m),Utot(m),PUx(m),PUy(m),PUz(m),PUt(m),U1(m),U2(m),U3(m),Eff.NormalStress (kPa),Tot. Normal Stress (kPa),Shear Stress (kPa),Rel. Shear Stress (kPa),Excess Porewater (kPa),Active Porewater (kPa),Steady Porewater (kPa),Suction Porewater (kPa),Porewater (kPa),Effective Suction Porewater (kPa) \n"])
                file.writelines(["{},{},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}\n".format(pname, pident, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, ens, tns, ss, rss, pe, pa, pst, pw, su, esu)
                                 for pname, pident, x, y, z, ux, uy, uz, ut, pux, puy, puz, put, u1, u2, u3, ens, tns, ss, rss, pe, pa, pst, pw, su, esu 
                                 in zip(iPhaseName, iPhaseIdent, iX, iY, iZ, iUx, iUy, iUz, iUt, iPUx, iPUy, iPUz, iPUt, iU1, iU2, iU3, iEffNormalStress, iTotNormalStress, iShearStress, iRelShearStress, iPExcess, iPActive, iPSteady, iPWater, iSuction, iEffSuction)])

        print('getInterfaceResults Done')   
        
    def getAllStructuralResults(self,
                    folderOut=None,
                    sphaseOrder=None,
                    sphaseStart=None,
                    sphaseEnd=None
                    ):    
    
        self.getPlateResults (fileOut = folderOut + r'\getPlateResults.csv',
                       sphaseOrder=sphaseOrder,
                       sphaseStart=sphaseStart,
                       sphaseEnd=sphaseEnd
                       )
                     
        self.getEmbeddedBeamResults (fileOut = folderOut + r'\getEmbeddedBeamResults.csv',
                       sphaseOrder=sphaseOrder,
                       sphaseStart=sphaseStart,
                       sphaseEnd=sphaseEnd
                       )

        self.getNodeToNodeAnchorResults (fileOut = folderOut + r'\getNodeToNodeAnchorResults.csv',
                       sphaseOrder=sphaseOrder,
                       sphaseStart=sphaseStart,
                       sphaseEnd=sphaseEnd
                       )

        self.getFixedEndAnchorResults  (fileOut = folderOut + r'\getFixedEndAnchorResults.csv',
                       sphaseOrder=sphaseOrder,
                       sphaseStart=sphaseStart,
                       sphaseEnd=sphaseEnd
                      )
                      
        self.getInterfaceResults (fileOut = folderOut + r'\getInterfaceResults.csv',
                       sphaseOrder=sphaseOrder,
                       sphaseStart=sphaseStart,
                       sphaseEnd=sphaseEnd
                      )
 
