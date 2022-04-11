# -*- coding:utf-8 -*-
'''
  @ Author: Aerin Sistemas <correo_para_estas_cosas@aerin.es
  @ Create Time: 2020-12-21 17:49:58
  @ Project: AITENEA
  @ Description:
  @ License: MIT License
 '''

import pandas as pd
import numpy as np
from dask import dataframe

from aitenea.logsconf.log_conf import logging_config
import logging
from logging.config import dictConfig

pd.options.mode.chained_assignment = None

loggtype = 'CONSOLE'
dictConfig(logging_config)
logger = logging.getLogger(loggtype)



class _EmissionsAux(object):
    def __init__(self):
        self.data = None
        self.a = None
        self.b = None
        self.c = None
        
    def set_parameter(self,a,b,c):
        self.a = a
        self.b = b
        self.c = c

    def calculate(self,data):
        self.data = data
        self._caudal_masico_gas_escape()
        self._caudal_masico_emision_CO2()
        self._caudal_masico_emision_NOx()
        self._aceleration()
        self._check_vel_signal()
        self._ecuaciones_dinamicas()
        self._zones()
        self._trajectory_check()
        self._potEM()
        self._emission_factors()
        self._auxiliarColumns()
        dask_data = dataframe.from_pandas(self.data, npartitions=1) 
        dask_data.repartition(partition_size='100MB')
        return dask_data


    def _caudal_masico_gas_escape(self):
        # here we calculate the stoichiometric relation for the fuel
        # this will be a constant
        # in stoichiometric condition, fuel is completely burned in the combustion
        # Mo2, MN2, MC, MH, MO are the molar weight of O2, N2, C, H and O respectively
        # ma_mf_st, stoichiometric relation
        # mg, mass flow of exhaust gas

        # lambda_med, valor medido con sonda proporcional
        # ma, mass air inlet, red from OBD
        MO2 = 31.998
        MN2 = 28.0134
        MC = 12.0107
        MH = 1.00704
        MO = 15.999
        self.data['MAFexh (g/s)' ] = 0.
        self.data['Consumo g/s CALC' ] = 0.
        ma_mf_st = ((self.a + self.b /4.0 - self. c /2.0 ) *(MO2 + 3.773 * MN2) ) / (self.a *MC + self. b *MH + self.c *MO)
        for i in range(len(self.data)):
            self.data['Consumo g/s CALC'][i]= self.data['MAF_obs (g/s)'][i] / (self.data['Lambda_OBD'][i] * ma_mf_st)
            self.data['MAFexh (g/s)'][i] = self.data['MAF_obs (g/s)'][i ] *(1 + 1/ (ma_mf_st * self.data['Lambda_OBD'][i]))   


    def _caudal_masico_emision_CO2(self):
        # chiCO2, molar concentration of CO2
        a = self.a
        b = self.b
        c = self.c
        n = 0
        MCO2 = 44.0087
        MN2 = 28.0134
        MH2 = 2.01408
        MH2O = 18.01308
        MO2 = 31.998
        const = a + b / 4 - c / 2
        self.data['Mg'] = 0.
        self.data['concentracion_CO2'] = 0.
        self.data['CO2 g/s CALC'] = 0.
        for j in range(len(self.data)):
            if self.data['Lambda_OBD'][j] >= 1:
                self.data['concentracion_CO2'][j] = a / (b / 4 + self.data['Lambda_OBD'][j] * (4.773 + n) * const + c / 2)
                self.data['Mg'][j] = (a * MCO2 + b * MH2O / 2 + 3.773 * self.data['Lambda_OBD'][j] * const * MN2 + (
                            self.data['Lambda_OBD'][j] - 1) * const * MO2) / (
                                            a + b / 2 + 3.773 * self.data['Lambda_OBD'][j] * const + (
                                                self.data['Lambda_OBD'][j] - 1) * const)
                self.data['CO2 g/s CALC'][j] = self.data['concentracion_CO2'][j] * self.data['MAFexh (g/s)'][j] * MCO2 / self.data['Mg'][j]
            else:
                e = c + 2 * self.data['Lambda_OBD'][j] * const - 2 * a
                i = b / 2 - e
                self.data['Mg'][j] = (a * MCO2 + e * MH2O + 3.773 * self.data['Lambda_OBD'][j] * const * MN2 + i * MH2) / (
                            a + e + 3.773 * self.data['Lambda_OBD'][j] * const + i)
                self.data['concentracion_CO2'][j] = a / (a + b / 2 + self.data['Lambda_OBD'][j] * (3.773 + n) * const)
                self.data['CO2 g/s CALC'][j] = self.data['concentracion_CO2'][j] * self.data['MAFexh (g/s)'][j] * MCO2 / self.data['Mg'][j]
        

    def _caudal_masico_emision_NOx(self):
        # chiNOx molar concentration NOx, measured with NOx sensor
        MNOx = 30
        mNOx_total = []
        self.data['NOx g/s calc'] = 0.
        for i in range(len(self.data)):
            self.data['NOx g/s calc'][i] = self.data['ppm NOx'][i] * (0.000001) * self.data['MAFexh (g/s)'][i] * (MNOx / self.data['Mg'][i])
        

    def _ecuaciones_dinamicas(self):
        # here we calculate the distance and the time interval
        self.data['distancia (m)'] = 0.
        self.data['Delta_t'] = 0.
        for i in range(len(self.data)):
            if i == 0:
                self.data['distancia (m)'][i] = np.nan
                self.data['Delta_t'][i] = self.data['Tiempo (s)'][i + 1] - self.data['Tiempo (s)'][i]
            else:
                self.data['Delta_t'][i] = self.data['Tiempo (s)'][i] - self.data['Tiempo (s)'][i - 1]
                self.data['distancia (m)'][i] = self.data['Velocidad (km/h)'][i] \
                                           * ((self.data['Tiempo (s)'][i] - self.data['Tiempo (s)'][i - 1]) / 3.6)
        

    def _check_vel_signal(self):
        # here we check if the velocity was measured with the proper resolution < 0.01
        a_pos = self.data['aceleracion']
        ares = a_pos[a_pos > 0].min()
        if ares <= 0.01:
            logger.info("La resolucion de la velocidad es adecuada %s",ares)
            
        else:
            # aplicamos medias moviles para suavizar la señal de velocidad
            logger.info('La resolucion de la velocidad NO es adecuada, aplicamos medias moviles %s',ares)
            n = 2
            while ares > 0.01:
                self._MA_vel( n)
                self.aceleration()
                a_pos = self.data['aceleracion']
                ares = a_pos[a_pos > 0].min()
                n = n + 1

    
    def _aceleration(self):
        # here we calculate the acceleration, deceleration
        self.data['aceleracion'] = 0.
        self.data['acc_neg'] = 0.
        self.data['acc_pos'] = 0.
        self.data['vel*acc+'] = 0.
        self.data['vel*acc'] = 0.

        for i in range(len(self.data)):
            if i == 0:
                self.data['aceleracion'][i] = (self.data['Velocidad (km/h)'][i + 1] - self.data['Velocidad (km/h)'][i]) / (
                            (self.data['Tiempo (s)'][i + 1] - self.data['Tiempo (s)'][i]) * 3.6)
            elif i == len(self.data) - 1:
                self.data['aceleracion'][i] = (self.data['Velocidad (km/h)'][i] - self.data['Velocidad (km/h)'][i - 1]) / (
                            (self.data['Tiempo (s)'][i] - self.data['Tiempo (s)'][i - 1]) * 3.6)
            else:
                self.data['aceleracion'][i] = (self.data['Velocidad (km/h)'][i + 1] - self.data['Velocidad (km/h)'][i - 1]) / (
                            (self.data['Tiempo (s)'][i + 1] - self.data['Tiempo (s)'][i - 1]) * 3.6)
            # En la mayoria de los casos la aceleracion es menor que 0.1 (en version anterior en lugar de cero esta nan)
            if self.data['aceleracion'][i] > 0.1:
                self.data['acc_pos'][i] = self.data['aceleracion'][i]
                self.data['acc_neg'][i] = 0
            else:
                self.data['acc_pos'][i] = 0
                self.data['acc_neg'][i] = self.data['aceleracion'][i]
            self.data['vel*acc+'][i] = (self.data['Velocidad (km/h)'][i] * self.data['acc_pos'][i]) / 3.6
            self.data['vel*acc'][i] = (self.data['Velocidad (km/h)'][i] * self.data['aceleracion'][i]) / 3.6
        

    def _MA_vel(self, n):
        # moving average window method, for softening the velocity signal
        self.data['MA'] = self.data['Velocidad (km/h)'].rolling(window=n).mean()
        self.data['Velocidad (km/h)'] = self.data['MA']
        data = self.data.drop(columns=['aceleracion', 'acc_neg', 'acc_pos', 'vel*acc+', 'vel*acc'], inplace=True)
        

    def _zones(self):
        self.data = self.data[self.data['Velocidad (km/h)'].notna()]
        self.data = self.data.reset_index(drop=True)
        self.data['Zone'] = 0
        for i in range(len(self.data)):
            vel = self.data['Velocidad (km/h)'][i]
            if (vel <= 60.0):
                self.data['Zone'][i] = 0
            elif 60.0 < vel <= 90.0:
                self.data['Zone'][i] = 1
            elif vel > 90.0:
                self.data['Zone'][i] = 2
        

    def _trajectory_check(self):
        # check the validity of the trip
        v_a_95 = []
        v_a = []
        self.dist = []
        self.time = []
        rpa = []
        self.vel_mean = []
        self.data['vel*acc+*Dt'] = self.data['vel*acc+'] * self.data['Delta_t']
        for i in range(self.data['Zone'].nunique()):
            self.dist.append(self.data['distancia (m)'][self.data['Zone'] == i].sum())
            self.time.append(self.data['Delta_t'][self.data['Zone'] == i].sum())
            self.vel_mean.append(self.dist[i] * 3.6 / self.time[i])
            #En la mayoria de los casos self.data['vel*acc+'] es NaN
            v_a.append(self.data['vel*acc+'][(self.data['Zone'] == i) & (self.data['vel*acc+'].notna())].tolist())
            # No se puede hacer un percentil de un vacio
            v_a_95.append(np.percentile(v_a[i], 95))
            rpa.append(self.data['vel*acc+*Dt'][(self.data['Zone'] == i) & (self.data['vel*acc+*Dt'].notna())].sum() / self.dist[i])
            ### CHECH WITH v*a_pos
            if (self.vel_mean[i] <= 74.6 and v_a_95[i] > (0.136 * self.vel_mean[i] + 14.44)):
                logger.info('Trayecto NO Valido segun va+95 en Zona %s', i)
            elif (self.vel_mean[i] <= 74.6 and v_a_95[i] <= (0.136 * self.vel_mean[i] + 14.44)):
                logger.info('Trayecto Valido segun va+95 en Zona %s', i)
 
            if (self.vel_mean[i] > 74.6 and v_a_95[i] > (0.0742 * self.vel_mean[i] + 18.966)):
                logger.info('Trayecto NO Valido segun va+95 en Zona %s', i)
            elif (self.vel_mean[i] > 74.6 and v_a_95[i] <= (0.0742 * self.vel_mean[i] + 18.966)):
                logger.info('Trayecto Valido segun va+95 en Zona %s', i)

                # CHECK WITH RPA
            if (self.vel_mean[i] <= 94.05 and rpa[i] < (-0.0016 * self.vel_mean[i] + 0.1755)):
                logger.info('Trayecto NO Valido segun RPA en Zona %s', i)
            elif (self.vel_mean[i] <= 94.05 and rpa[i] >= (-0.0016 * self.vel_mean[i] + 0.1755)):
                logger.info('Trayecto Valido segun RPA en Zona %s', i)
            if (self.vel_mean[i] > 94.05 and rpa[i] < 0.025):
                logger.info('Trayecto NO Valido segun RPA en Zona %s', i)
            elif (self.vel_mean[i] > 94.05 and rpa[i] >= 0.025):
                logger.info('Trayecto Valido segun RPA en Zona %s', i)
        

    def _emission_factors(self):
        # calculate the emission factors by zones

        self.data['NOx*Dt'] = self.data['NOx g/s calc'] * self.data['Delta_t']
        self.data['CO2*Dt'] = self.data['CO2 g/s CALC'] * self.data['Delta_t']
        self.data['consumo*Dt'] = self.data['Consumo g/s CALC'] * self.data['Delta_t']
        NOx_mass = self.data['NOx*Dt'].sum()
        CO2_mass = self.data['CO2*Dt'].sum()
        dist = []
        FE_NOx = []
        FE_CO2 = []
        FC_100Km = []
        fe_NOx = []
        fe_CO2 = []
        fc_Kwh = []
        for i in range(self.data['Zone'].nunique()):
            dist.append(self.data['distancia (m)'][self.data['Zone'] == i].sum())
            FE_NOx.append(self.data['NOx*Dt'][self.data['Zone'] == i].sum() * 1000 / (dist[i] * 0.001))
            FE_CO2.append(self.data['CO2*Dt'][self.data['Zone'] == i].sum() / (dist[i] * 0.001))
            FC_100Km.append(self.data['consumo*Dt'][self.data['Zone'] == i].sum() * 100 / (dist[i] * 0.001 * 725))
            fe_NOx.append(self.data['NOx*Dt'][self.data['Zone'] == i].sum() * 1000 / self.data['Work'][self.data['Zone'] == i].sum())
            fe_CO2.append(self.data['CO2*Dt'][self.data['Zone'] == i].sum() / self.data['Work'][self.data['Zone'] == i].sum())
            fc_Kwh.append(self.data['consumo*Dt'][self.data['Zone'] == i].sum() / self.data['Work'][self.data['Zone'] == i].sum())
        NOx_dist = sum(FE_NOx) / 1000
        CO2_dist = sum(FE_CO2)
        NOx_work = sum(fe_NOx) / 1000
        CO2_work = sum(fe_CO2)
        Consumption = sum(FC_100Km)
        Consumption_kwh = sum(fc_Kwh)
        dist_total = sum(dist)
        time_total = sum(self.time)
        # CREATE TABLE WITH POLLUTANT EMISSION FOR EACH ZONE: 0 URBAN, 1 RURAL, 2 HIGHWAY
        zone_emissions = {'zone': ['rural', 'urban', 'highway'],
                          'Time': self.time,
                          'Distance': self.dist,
                          'Average velocity': self.vel_mean,
                          'NOx(mg/Km)': FE_NOx,
                          'CO2 (g/Km)': FE_CO2,
                          'Consumption (g/100Km)': FC_100Km,
                          'NOx (mg/kWh)': fe_NOx,
                          'CO2 (g/kWh)': fe_CO2,
                          'Consumption (g/kWh)': fc_Kwh
                          }
        results = pd.DataFrame(zone_emissions)

        # CREATE TABLE WITH TOTAL POLLUTANTS EMISSIONS
        total_pollutants = [
            {'Pollutant': 'NOx', 'Mass (g)': NOx_mass, 'Mass/distance (g/Km)': NOx_dist, 'Mass/work (g/kWh)': NOx_work},
            {'Pollutant': 'CO2', 'Mass (g)': CO2_mass, 'Mass/distance (g/Km)': CO2_dist, 'Mass/work (g/kWh)': CO2_work}]

        pollutants = pd.DataFrame(total_pollutants, index=[0, 1])

        # CREATE TABLE WITH MEAN VALUES FOR DIFFERENT PARAMETERS OF INTEREST SUCH US: VELOCITY , RPM, ...
        trip_mean_values = [{'Parameter':'Velocity (Km/h)','Max.': self.data['Velocidad (km/h)'].max(), 'Avg.': self.data['Velocidad (km/h)'].mean()},
                            {'Parameter':'Engine torque (Nm)','Max.': self.data['Me [Nm]'].max(), 'Avg.': self.data['Me [Nm]'].mean()},
                            {'Parameter':'Engine speed (rpm)','Max.': self.data['RPM'].max(), 'Avg.': self.data['RPM'].mean()}]
        tripsummary = pd.DataFrame(trip_mean_values)
        
        # CREATE TABLE WITH SOME TRIP SUMMARY


        trip = [{'Trajectory':'Total distance (Km)' ,'Value': dist_total},
                {'Trajectory':'Total time (s)' ,'Value': time_total},
                {'Trajectory':'Total work (KWh)','Value': self.data['Work'].sum()}]


        tripconditions = pd.DataFrame(trip)
        
        res = {
               'Total work (KWh)': self.data['Work'].sum(),
               'MAX velocity (Km/h)': self.data['Velocidad (km/h)'].max(),
               'AVG velocity (Km/h)': self.data['Velocidad (km/h)'].mean(),
               'MAX engine torque (Nm)': self.data['Me [Nm]'].max(),
               'AVG engine torque (Nm)': self.data['Me [Nm]'].mean(),
               'MAX Engine speed (rpm)' : self.data['RPM'].max(),
               'AVG Engine speed (rpm)' : self.data['RPM'].mean(),
               'NOx (g)': NOx_mass,
               'NOx (g/Km)' : NOx_dist,
               'NOx (g/kWh)' : NOx_work,
               'CO2 (g)' : CO2_mass,
               'CO2 (g/Km)' : CO2_dist,
               'CO2 (g/kWh)' : CO2_work,
               'NOx rural (mg/Km)' : FE_NOx[0],
               'NOx urban (mg/Km)' : FE_NOx[1],
               'NOx highway (mg/Km)' : FE_NOx[2],
               'CO2 rural (mg/Km)': FE_CO2[0],
               'CO2 urban (mg/Km)' : FE_CO2[1],
               'CO2 highway (mg/Km)' : FE_CO2[2],
               'Consumption rural (g/100Km)': FC_100Km[0],
               'Consumption urban (g/100Km)' : FC_100Km[1],
               'Consumption highway (g/100Km)' : FC_100Km[2]}
        self.results=pd.DataFrame(res, index=[0])
    

    def _potEM(self):
        self.data['potEM'] = 0.
        self.data['Work'] = 0.
        for i in range(len(self.data)):
            self.data['potEM'][i] = self.data['Me [Nm]'][i] * self.data['RPM'][i] * 2 * np.pi / (60 * 10 ** 3)
            self.data['Work'][i] = self.data['potEM'][i] * self.data['Delta_t'][i] / 3600
    
    
    def _auxiliarColumns(self):
        # add auxiliary columns: column Date: datetime column
        #                               Id vehicle : column to identify the vehicle for which emissions were measured
        my_data = pd.date_range('2019-03-07 01:00:00', periods=len(self.data), freq="100L")
        self.data['Date'] = my_data
        self.data['Id_vehicle'] = 'BMAVG'