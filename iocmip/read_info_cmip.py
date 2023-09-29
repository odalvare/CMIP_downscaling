# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 10:40:07 2023

@author: danie 

This class reads the primary execution parameter for downscaling CMIP

"""
import sys
import os
import platform
import gc

#Detect operaring system and apply folder delimiter
ost=platform.system()
delim='/'
if(ost=='Windows'):
    delim='//'
    
import numpy as np
import rasterio

class bldCMIP:
    
    #Begining of constructor --------------------------------------------------
    def __init__(self,project):
        """
        Construction of an instance for reading downscaling basic execution parameters

        Parameters:
        ----------
            workspace : string
                The folder location of the project
        
        Returns:
        -------
            null
            
        """
        #Constructor begins here
        self.__workspace=project
        self.__parameters={}
        self.__metaref={}
        
        self.readcmipdowndata(verbose=True)
        
        # Read secondary information and saves array and metadata
        
        mdert=self.__workspace+delim+'data'+delim+'downscaling'+delim+'mde.tif'
        mde = rasterio.open(mdert)
        
        mde_bnds = mde.bounds
        print(mde_bnds)
        minxmde=mde_bnds[0]
        print(minxmde)
        minymde=mde_bnds[1]
        maxxmde=mde_bnds[2]
        maxymde=mde_bnds[3]
        
        print('Checking boundaries')
        
        for i in range(21):
            
            year=2001 + i
            yro = year
            yrf = yro + 1
            
            print(str(yro))
        
            flnm='pcp_chirps_TATACOA_1d_5km_'+str(yro)+'0101_'+str(yrf)+'0101.tif'
            chrt=self.__workspace+delim+'data'+delim+'downscaling'+delim+'chirps'+delim+flnm
            chirps = rasterio.open(chrt)
        
            chirps_bnds = chirps.bounds
            # print(chirps_bnds)
            minxchirps=chirps_bnds[0]
            minychirps=chirps_bnds[1]
            maxxchirps=chirps_bnds[2]
            maxychirps=chirps_bnds[3]
            
            if(minxchirps>minxmde):
                raise Exception('Invalid chirps border in minx')
                sys.exit()
            if(maxxchirps<maxxmde):
                raise Exception('Invalid chirps border in maxx')
                sys.exit()
            if(minychirps>minymde):
                raise Exception('Invalid chirps border in miny')
                sys.exit()
            if(maxychirps<maxymde):
                raise Exception('Invalid chirps border in maxy')
                sys.exit()
        
            chirps.close()
            
            flnmevi='evi_mod13q1_colombia_16d_250m_'+str(yro)+'0101_'+str(yrf)+'0101.tif'
            evirt=self.__workspace+delim+'data'+delim+'downscaling'+delim+'modis'+delim+'evi'+delim+flnmevi
            evi = rasterio.open(evirt)
            
            evi_bnds = evi.bounds
            # print(evi_bnds)
            minxevi=evi_bnds[0]
            minyevi=evi_bnds[1]
            maxxevi=evi_bnds[2]
            maxyevi=evi_bnds[3]
            
            if(minxevi>minxmde):
                raise Exception('Invalid evi border in minx')
                sys.exit()
            if(maxxevi<maxxmde):
                raise Exception('Invalid evi border in maxx')
                sys.exit()
            if(minyevi>minymde):
                raise Exception('Invalid evi border in miny')
                sys.exit()
            if(maxyevi<maxymde):
                raise Exception('Invalid evi border in maxy')
                sys.exit()
        
            evi.close()
        
            flnmndvi='ndvi_mod13q1_colombia_16d_250m_'+str(yro)+'0101_'+str(yrf)+'0101.tif'
            ndvirt=self.__workspace+delim+'data'+delim+'downscaling'+delim+'modis'+delim+'ndvi'+delim+flnmndvi
            ndvi = rasterio.open(ndvirt)
            
            ndvi_bnds =  ndvi.bounds
            # print(ndvi_bnds)
            minxndvi=ndvi_bnds[0]
            minyndvi=ndvi_bnds[1]
            maxxndvi=ndvi_bnds[2]
            maxyndvi=ndvi_bnds[3]
            
            if(minxndvi>minxmde):
                raise Exception('Invalid evi border in minx')
                sys.exit()
            if(maxxndvi<maxxmde):
                raise Exception('Invalid evi border in maxx')
                sys.exit()
            if(minyndvi>minymde):
                raise Exception('Invalid evi border in miny')
                sys.exit()
            if(maxyndvi<maxymde):
                raise Exception('Invalid evi border in maxy')
                sys.exit()
        
            ndvi.close()
            mde.close()
        
    #End of constructor ------------------------------------------------------- 
    
    #Begining of method -------------------------------------------------------    
    def readcmipdowndata(self,verbose=False): 
        """
        Method for reading the KAGB basic settings
        
        Parameters
        ----------        
            verbose: logical
                flag to detect error in reading input data
        
        Returns
        -------        
            parameters : dictionary
                required data for running downscaling CMIP.
                keys of parameters dictionary:
                    name: Project's name (str)
                    EPSG: Geographic reference of the project (str)
                    minX: Most Western coordinate in the working area (integer)
                    minY: Most Southern coordinate in the working area (integer)
                    res: Pixel size (float)
                    rows: Number of rows on which the domain is discretized (integer)
                    cols: Number of columns on which the domain is discretized (integer)
                    n_years: Number of years with modis data (integer)
                    down_id: Type of multivariate bias corrected regression (int)
                        1: Linear regression
                        2: Exponential regression
                        3. Power regression                    
                    n_vbles: Number of variables in multivariate bias corrected regression
                    variables: Name of the variables in multivariate bias corrected regression (str list)
                
        """
        
        #code begins here
        
        flnm=self.__workspace+'data'+delim+'basic'+delim+'config_downsc.dat'
        
        try:
            
            with open(flnm, 'rb') as in_file:
                # A dictionary to contain info about the grid                
                if verbose :
                    print(('\n    Reading file: "{0}"'.format(flnm)))
                    
                print('*--- Preparing simulation, reading downscaling CMIP information ---*')
                
                # Project name
                line=in_file.readline()
                line=in_file.readline()                
                line_split=line.split()
                strg=line_split[0].decode("utf-8") 
                self.__parameters['name']=strg
                print('Name='+str(self.__parameters['name']))
                
                # Geographic reference
                line=in_file.readline()
                line=in_file.readline()
                line=in_file.readline()
                line_split=line.split()
                c=str(line_split[0])
                self.__parameters['EPSG']=c[2:len(c)-1]
                print('EPSG='+str(self.__parameters['EPSG']))
                
                # Geographic reference
                line=in_file.readline()
                line=in_file.readline()
                line=in_file.readline()
                line_split=line.split()
                self.__parameters['minX']=float(line_split[1])
                print('minX='+str(self.__parameters['minX'])) 
                line=in_file.readline()
                line_split=line.split()
                self.__parameters['minY']=float(line_split[1])
                print('minY='+str(self.__parameters['minY'])) 
                line=in_file.readline()
                line_split=line.split()
                self.__parameters['res']=float(line_split[1])
                print('Res='+str(self.__parameters['res'])) 
                line=in_file.readline()
                line_split=line.split()
                self.__parameters['rows']=int(line_split[1])
                print('Rows='+str(self.__parameters['rows'])) 
                line=in_file.readline()
                line_split=line.split()
                self.__parameters['columns']=int(line_split[1])
                print('Columns='+str(self.__parameters['columns']))
                
                # Reading the simulation drivers
                line=in_file.readline()
                line=in_file.readline()
                line=in_file.readline()
                line_split=line.split()
                self.__parameters['n_years']=int(line_split[1])
                print('n_years='+str(self.__parameters['n_years']))
                
                # Reading the years with landcover data
                line=in_file.readline()
                line=in_file.readline()
                years=np.zeros((self.__parameters['n_years']),dtype=np.int64)
                for i in range(self.__parameters['n_years']):
                    line=in_file.readline()
                    line_split=line.split()
                    years[i]=int(line_split[0])
                self.__parameters['years']=years
                
                # Reading the CMIP downscaling alternatives
                line=in_file.readline()
                line=in_file.readline()
                line=in_file.readline()
                line_split=line.split()
                self.__parameters['down_id']=int(line_split[0])
                print('down_id='+str(self.__parameters['down_id']))
                
                # Reading the number of variables for regression
                line=in_file.readline()
                line=in_file.readline()
                line=in_file.readline()
                line_split=line.split()
                self.__parameters['n_vbles']=int(line_split[0])
                print('n_vbles='+str(self.__parameters['n_vbles']))
                
                # Reading the downscaling variables
                line=in_file.readline()
                line=in_file.readline()
                vbles=[]
                for i in range(self.__parameters['n_vbles']):
                    line=in_file.readline()
                    line_split=line.split()
                    vbles.append(line_split[0])
                self.__parameters['variables']=vbles
                
        except IOError:
            print(('    Error reading file "{0}"'.format(flnm)))
            print('    Check if the file exists...')
            sys.exit(0)
            
        in_file.close()

        print('*---Succesfull reading of the execution data in file '+flnm+'---*')
                
    # Ending of method -------------------------------------------------------
    
    #Begining of method -------------------------------------------------------
    def getParameters(self):
        '''
        Return the dictionary with the downscaling parameters

        Returns
        -------
        parameters : dictionary
            required data for running downscaling CMIP.
            keys of parameters dictionary:
                name: Project's name (str)
                EPSG: Geographic reference of the project (str)
                minX: Most Western coordinate in the working area (integer)
                minY: Most Southern coordinate in the working area (integer)
                res: Pixel size (float)
                rows: Number of rows on which the domain is discretized (integer)
                cols: Number of columns on which the domain is discretized (integer)
                n_years: Number of years with modis data (integer)
                down_id: Type of multivariate bias corrected regression (int)
                    1: Linear regression
                    2: Exponential regression
                    3. Power regression                    
                n_vbles: Number of variables in multivariate bias corrected regression
                variables: Name of the variables in multivariate bias corrected regression (str list)

        '''
        return self.__parameters
    
    # Ending of method -------------------------------------------------------

         
    



