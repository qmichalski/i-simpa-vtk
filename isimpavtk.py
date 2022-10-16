# -*- coding: utf-8 -*-
"""
Created on Thu May 6 10:56:31 2022

@author: Dr Quentin Michalski

Functions to convert I-SIMPA csbin results to VTK.
VTK can then be used in any data visualisation software like PARAVIEW, etc.

"""

import os
import evtk
import numpy as np
import math
import libsimpa as lbsmp

def faceEnergyTodBRsurf( wj ):
    '''
    Found in I-SIMPA tutorials.
    Convert the faceSumEnergy to dB scale
    Inputs
    -------
    wj: float faceSumEnergy from the surface receiver
    
    Returns
    -------
    faceSumEnergy: float in dB.
    
    '''
    
    if wj > 0:
        return 10*math.log10(wj/math.pow(10.,-12.))
    else:
        return np.nan

def isimpaCSBINToVTK(fileName,IN_PATH,OUT_PATH):
    '''
    Takes I-SIMPA *.csbin results and convert them to VTK format for
    easier post-processing e.g. in Paraview, Tecplot, etc.
    Careful if modifying, libsimpa can make the Python console crash.
    Make sure to stay within definition of objects, e.g. rsIndex < rsMax,
    faceIndex < faceCount, etc.
    
    Inputs
    -------
    fileName: str name of the file .csbin containing the results to export
    IN_PATH: str path to the file to read
    OUT_PATH: str path where to write vtk files

    Returns
    -------
    None.

    '''
    
    FULL_IN_PATH = os.path.join(IN_PATH,"{}".format(fileName))
    
    if os.path.isfile(FULL_IN_PATH):
        rsurfDataVar = lbsmp.rsurf_data() # libsimpa object required to read
        lbsmp.rsurf_io_Load(FULL_IN_PATH, rsurfDataVar) # loading the result file .csbin
        rsMax = rsurfDataVar.GetRsCount() # number of surface receiver
        # Iterates and convert all receivers
        for rsIndex in range(0,rsMax):
            faceCount = rsurfDataVar.GetRsFaceCount(rsIndex) # number of faces in the surface receiver
            nodeCount = rsurfDataVar.GetNodesCount() # number of nodes in the receiver
            surfaceReceptorName = rsurfDataVar.GetRsName(rsIndex) # name of the surface recevier
            print("Reading surface receptor: {}/{} {} with {} faces".format(rsIndex+1,rsMax,surfaceReceptorName,str(faceCount)))
            
            # Conversion of nodes to vertices to store in vtk
            x = np.zeros(nodeCount)
            y = np.zeros(nodeCount)
            z = np.zeros(nodeCount)
            
            for n in range(nodeCount):
                node = rsurfDataVar.GetNodePositionValue(n)
                x[n], y[n], z[n] = node[0], node[1], node[2]
            
            # Define connectivity or vertices that belongs to each element
            conn = np.zeros(3*faceCount)
            offset = np.zeros(faceCount)
            ctype = np.zeros(faceCount)
            cd = np.zeros(faceCount)
            # Iterates over all surface receiver faces
            for faceIndex in range(faceCount):
                faceVerticies = rsurfDataVar.GetFaceVertices(rsIndex, faceIndex)
                conn[3*faceIndex], conn[3*faceIndex+1], conn[3*faceIndex+2] = faceVerticies[0], faceVerticies[1], faceVerticies[2]
                offset[faceIndex] = (faceIndex+1)*3
                ctype[faceIndex] = evtk.vtk.VtkTriangle.tid
                faceSumEnergy = rsurfDataVar.GetFaceSumEnergy(rsIndex, faceIndex)
                faceSumDB = faceEnergyTodBRsurf(faceSumEnergy)

                cd[faceIndex] = faceSumDB
            
            cellData = {"SPL" : cd}
            
            FILE_PATH = os.path.join("{}".format(OUT_PATH),"{}-{}".format(fileName.split('.')[0],str(rsIndex)))
            
            evtk.hl.unstructuredGridToVTK(FILE_PATH, x, y, z, connectivity = conn, offsets = offset, cell_types = ctype, cellData = cellData)
    else:
        print('Path not valid.')
    return()

if __name__ == "__main__":
    IN_PATH = ".\\data\\isimpa"
    OUT_PATH = ".\\data\\vtk"
    fileName = "rs_cut.csbin"
    isimpaCSBINToVTK(fileName,IN_PATH,OUT_PATH)
    


