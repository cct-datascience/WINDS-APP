# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 13:38:06 2017

@author: Pete
"""
#!/usr/bin/env python
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine

db=create_engine('mysql://UofABEWINDS:WINDSAWSPort2020@windsdatabase-1.cdzagwevzppe.us-west-1.rds.amazonaws.com:3306/winds_test')


def hg(a, b, C, z):
    value = 1
    hg = value
    for i in range(1, 40):
        value = value * (a + i - 1) * (b + i - 1) / (C + i - 1) / i * z
        hg = hg + value
    return hg

def d_total(ts, tr, zt, zwt, alpha, N):
    W = -(np.power(alpha * (zt - zwt) * 100, N))
    zwt = zwt
    hyper = hg(1, 1 - 1 / N, 1 + 1 / N, W / (W - 1))
    d_total = ts * zwt + tr * (zt - zwt) + (ts - tr) * (zt - zwt) * np.power((1 - W), (1 / N - 1)) * hyper
    return d_total

def d_cell_WT(ts, tr, zu, zl, zwt, alpha, N):
    W = -(np.power(alpha * (zu - zwt) * 100, N))
    hyper = hg(1, 1 - 1 / N, 1 + 1 / N, W / (W - 1))
    d_cell_WT = ts * (zwt - zl) + tr * (zu - zwt) + (ts - tr) * (zu - zwt) * np.power((1 - W), (1 / N - 1)) * hyper
    return d_cell_WT

def d_cell_Eq(ts, tr, zu, zl, zwt, alpha, N):
    WU = -(np.power(alpha * (zu - zwt) * 100, N))
    wl = -(np.power(alpha * (zl - zwt) * 100, N))
    hyperu = hg(1, 1 - 1 / N, 1 + 1 / N, WU / (WU - 1))
    hyperl = hg(1, 1 - 1 / N, 1 + 1 / N, wl / (wl - 1))
    d_cell_Eq = tr * (zu - zl) + (ts - tr) * (zu - zwt) * np.power((1 - WU), (1 / N - 1)) * hyperu - (ts - tr) * (zl - zwt) * np.power((1 - wl), (1 / N - 1)) * hyperl
    return d_cell_Eq
    
# The following function, if true, reads the weather from the SQL database, otherwise from Active_year_weather in the spreadsheet
# The data is read into a panda array called WeatherArray and returned
    
 
class weather:
    def __init__(self, WeatherArray):
        self.NumDays = self.EndDOY - self.SimStartDOY 
        self.w_date = WeatherArray['Date']                   #the date of the record, mm/dd/yyyy
        self.RH_min = np.array(WeatherArray['rh_min'])                      #Minimum relative humidity, percent, decimal, 8 digits
        self.WS = np.array(WeatherArray['WS'])                  #wind speed, m/sec, decimal, 8 digits
        self.ET_0 = np.array(WeatherArray['ETo (mm)'])                        #Reference ET, mm/day, decimal, 8 digits
        self.rainfall = np.array(WeatherArray['Rain (mm)'])              #Rainfall, mm/day, decimal, 8 digits
        self.Tmax = np.array(WeatherArray['tmax'])                      #Maximum temperature, Celsius, decimal, 8 digits
        self.Tmin = np.array(WeatherArray['tmin'])                      #Minimum temperature, Celsius, decimal, 8 digits
        self.Rain_time = np.array(WeatherArray['Rain time (hr)'])                 #Rain time (time of storm), hr, decimal, 5 digits

class RS_daily:
    def __init__(self, RS_dailyArray):
        self.NDVI_DOY = np.array(RS_dailyArray['NDVI_DOY'])           #The name of the planting (text), normally includes owner name, field name, crop, and year, such as GaryField1Wheat2017
        self.NDVI_daily = np.array(RS_dailyArray['NDVI'])           #The name of the planting (text), normally includes owner name, field name, crop, and year, such as GaryField1Wheat2017

class ET_daily:
    def __init__(self, ET_dailyArray):
        self.Daily_DOY = np.array(ET_dailyArray['DOY'])                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
        self.Daily_Kcb = np.array(ET_dailyArray['Kcb'])
        self.Daily_one_minus_c = np.array(ET_dailyArray['one_minus_c'])
        self.Daily_Crop_height = np.array(ET_dailyArray['Crop_height'])
        self.Daily_Root = np.array(ET_dailyArray['Root'])

class plantings:
    def __init__(self, PlantingArray):
        self.PlantingNum = PlantingArray['Planting num']                             #The long random identifier that represents the planting, for example, 9a649ac3a4353ffe6d67fdad0c6bf3a9
        self.PlantingName = PlantingArray['Planting name']                #The name of the planting (text), normally includes owner name, field name, crop, and year, such as GaryField1Wheat2017
        self.RunPlanting = PlantingArray['Run planting']                 #A Boolean that specifies whether a simulation should take place
        self.PlantingYear = PlantingArray['Planting year']                 #A Boolean that specifies whether a simulation should take place
        self.PlantingDOY = PlantingArray['Planting DOY']
        self.PlantingDate = PlantingArray['Planting date']
        self.StartDOY = PlantingArray['DOY start']                             #The long random identifier that represents the planting, for example, 9a649ac3a4353ffe6d67fdad0c6bf3a9
        self.StartDate = PlantingArray['Date start']                #The name of the planting (text), normally includes owner name, field name, crop, and year, such as GaryField1Wheat2017
        self.EndDOY = PlantingArray['DOY end']
        self.EndDate = PlantingArray['Date end']                   #The number of days ahead of the present day (integer) for which the model should predict growth, water use, and irrigations
        self.FieldNum = PlantingArray['Field num']                                #The long random identifier that represents the field, for example, 9a649ac3a4353ffe6d67fdad0c6bf3a9
        self.FieldNameP = PlantingArray['Field name']                             #The name of the field (text), which normally includes the owner and field, such as GaryField1
        self.SoilLayerNum = PlantingArray['Soil layer set num']                                #The long random identifier that represents the field, for example, 9a649ac3a4353ffe6d67fdad0c6bf3a9
        self.SoilLayerName = PlantingArray['Soil layer set name']                             #The name of the field (text), which normally includes the owner and field, such as GaryField1
        self.AccountNum = PlantingArray['Account name']                              #The long random identifier that represents the owner, for example, 9a649ac3a4353ffe6d67fdad0c6bf3a9
        self.AccountNameP = PlantingArray['Account name']        #The number of locations (integer) that are modeled in an individual planting
        self.CropNum = PlantingArray['Crop num']                         #The name of the crop (text string), which initializes the following parameters, for example, GuayuleAZ2Spring
        self.CropName = PlantingArray['Crop name']                              #The crop ID, which initializes the following parameters, but the parameters can be subsequently changed, for example, 9a649ac3a4353ffe6d67fdad0c6bf3a9 
        self.WeatherNum = PlantingArray['Weather num']       #The name of the weather station (text) to be used for this simulation, for example, Maricopa represents the AZMET Maricopa station
        self.WeatherName = PlantingArray['Weather name']          #the station ID of the record, mm/dd/yyyy
        self.WeatherSheetName = PlantingArray['Weather sheet name']
        self.ETFractionsNum = PlantingArray['ET fractions num']                              #The crop ID, which initializes the following parameters, but the parameters can be subsequently changed, for example, 9a649ac3a4353ffe6d67fdad0c6bf3a9 
        self.WettingFractionsNum = PlantingArray['Wetting fractions num']
        self.SimStartDOY = PlantingArray['SimStartDOY']
        self.SimStartDate = PlantingArray['SimStartDate']
        self.IrrNum = PlantingArray['Irr num']
        self.IrrName = PlantingArray['Irr name']
        self.IrrSection = PlantingArray['Irr section']
        self.NumIrrigations = PlantingArray['Num irrigations']
        self.NumNeutron = PlantingArray['Num neutron']
        self.FirstNeutronRow = PlantingArray['First neutron row']
        self.IP = PlantingArray['Initial_days']                                   #The number of days after planting (integer) that the development phase (IncreasingET) begins
        self.DP = PlantingArray['Development_days']                     #The number of days after planting (integer) that the Midseason (maxET) phase begins
        self.MP = PlantingArray['Midseason_days']                 #The number of days after planting (integer) that the Late Season decline phase begins
        self.LP = PlantingArray['Lateseason_days']               #The number of days after planting (integer) that the End Season (low ET) phase begins. Some crops so not have this phase
        self.EP = PlantingArray['Ending_season_days']               #The number of days after planting (integer) that the End Season (low ET) phase begins. Some crops so not have this phase
        self.DP_2 = PlantingArray['Development_days_year_2']               #The number of days after planting (integer) that the End Season (low ET) phase begins. Some crops so not have this phase
        self.MP_2 = PlantingArray['Midseason_days_year_2']               #The number of days after planting (integer) that the End Season (low ET) phase begins. Some crops so not have this phase
        self.LP_2 = PlantingArray['Lateseason_days_year_2']               #The number of days after planting (integer) that the End Season (low ET) phase begins. Some crops so not have this phase
        self.CropEndDOY = PlantingArray['Crop_end_DOY']                         #The number of days after planting (integer) that the harvest takes place.
        self.IKcb = PlantingArray['Initial_Kcb']                     #The crop coefficient during the initial stage (decimal, 5 digits), based on dual crop coefficient and FAO56
        self.MKcb = PlantingArray['Midseason_Kcb']                             #The crop coefficient during the midseason stage (decimal, 5 digits), based on dual crop coefficient and FAO56. The model increases the crop coefficient during the development stage
        self.EKcb = PlantingArray['Endseason_ Kcb']                             #The crop coefficient during the midseason stage (decimal, 5 digits), based on dual crop coefficient and FAO56. The model increases the crop coefficient during the development stage
        self.MKcb_2 = PlantingArray['Midseason_Kcb_year_2']                             #The crop coefficient during the endseason stage (decimal, 5 digits), based on dual crop coefficient and FAO56. The model decreases the crop coefficient during the lateseason stage
        self.EKcb_2 = PlantingArray['Endseason_Kcb_year_2']                             #The crop coefficient during the endseason stage (decimal, 5 digits), based on dual crop coefficient and FAO56. The model decreases the crop coefficient during the lateseason stage
        self.ICP = PlantingArray['Initial_1-C_root_height_Days']                                   #The number of days after planting (integer) that the development phase (IncreasingET) begins
        self.DCP = PlantingArray['Development_1-C_root_height_Days']                     #The number of days after planting (integer) that the Midseason (maxET) phase begins
        self.MCP = PlantingArray['Midseason_1-C_root_height_Days']                     #The number of days after planting (integer) that the Midseason (maxET) phase begins
        self.ECP = PlantingArray['Endseason_1-C_Days']                 #The number of days after planting (integer) that the Late Season decline phase begins
        self.IC = PlantingArray['Initial_1-C']                     #The number of days after planting (integer) that the Midseason (maxET) phase begins
        self.MC = PlantingArray['Midseason_1-C']                 #The number of days after planting (integer) that the Late Season decline phase begins
        self.EC = PlantingArray['Endseason_1-C']                 #The number of days after planting (integer) that the Late Season decline phase begins
        self.ERH = PlantingArray['Endseason_root_and_height_days']                 #The number of days after planting (integer) that the Late Season decline phase begins
        self.IR = PlantingArray['Initial_root_z']                     #The number of days after planting (integer) that the Midseason (maxET) phase begins
        self.DR = PlantingArray['Development_root_z']                 #The number of days after planting (integer) that the Late Season decline phase begins
        self.FR = PlantingArray['Final_root_z']                 #The number of days after planting (integer) that the Late Season decline phase begins
        self.minH = PlantingArray['Minimum_plant_height']                   #The initial crop height in the model (decimal, 5 digits, meters).
        self.maxH = PlantingArray['Maximum_plant_height']                   #The final crop height (decimal, 5 digits, meters). The model grows the crop during the development phase
        self.midH = PlantingArray['Midseason_plant_height']                   #The initial crop height in the model (decimal, 5 digits, meters).
        self.endH = PlantingArray['Endseason_plant_height']                   #The final crop height (decimal, 5 digits, meters). The model grows the crop during the development phase
        self.calculate_one_minus_c = PlantingArray['calculate_one_minus_c']                   #The final crop height (decimal, 5 digits, meters). The model grows the crop during the development phase
        self.Select_Kcb = PlantingArray['Kc_calculation_procedure']                          #The management allowable depletion (MAD) value from table 22 in FAO56. It is then adjusted for evaporation rate. fraction, 5 digits
        self.Irrigation_partition_1 = PlantingArray['Irrigation_partition_1']
        self.Irrigation_partition_2 = PlantingArray['Irrigation_partition_2']
        self.Irrigation_partition_3 = PlantingArray['Irrigation_partition_3']
        self.Irrigation_partition_4 = PlantingArray['Irrigation_partition_4']
        self.Nitrogen_simulation = PlantingArray['Simulate_nitrogen']
        self.Salinity_simulation = PlantingArray['Simulate_salinity']
        self.Rainfall_simulation = PlantingArray['Simulate_rainfall']
        self.type_irrigation = PlantingArray['Type_irrigation']
        self.Rain_infiltration_calculation = PlantingArray['Rain_infiltration_calculation']    #Boolean to determine if infiltration is calculated with Green ampt or SCS or is just assigned the rain_partition as the fraction

        self.Neglect_upper_layer_in_depletion_calc = PlantingArray['NeglectEvaporationLayerDepletion'] #Boolean that is true if upper layer is  not included in the calculation of percent depletion
        self.pTable22 = PlantingArray['MAD_p_Table22']                          #The management allowable depletion (MAD) value from table 22 in FAO56. It is then adjusted for evaporation rate. fraction, 5 digits
        self.adjust_P = PlantingArray['Adjust_p']
        #self.Max_yield = PlantingArray['Max_yield']                          #in case of economic forecast, this is in the model, but it is not currently used. (kg/ha) (Real number, 8 digits)
        #self.Ky_initial = PlantingArray['Initial_crop_sensitivity']             #The sensitivity of the crop yield to water stress during initial phase (Units can vary dramatically for different scenarios) (Decimal number, 5 digits)
        #self.Ky_DP = PlantingArray['Development_crop_sensitivity']                  #The sensitivity of the crop yield to water stress during development phase (Units can vary dramatically for different scenarios) (Decimal number, 5 digits)
        #self.Ky_MP = PlantingArray['Midseason_crop_sensitivity']                  #The sensitivity of the crop yield to water stress during midseason phase (Units can vary dramatically for different scenarios) (Decimal number, 5 digits)
        #self.Ky_late = PlantingArray['Lateseason_crop_sensitivity']                #The sensitivity of the crop yield to water stress during lateseason phase (Units can vary dramatically for different scenarios) (Decimal number, 5 digits)
        #self.Ky_end = PlantingArray['Endseason_crop_sensitivity']                  #The sensitivity of the crop yield to water stress during endseason phase (Units can vary dramatically for different scenarios) (Decimal number, 5 digits)
        self.Seal_bottom = PlantingArray['seal_bottom']                     #Boolean that is true for some class assignments in which soil physics calculations are evaluated
        self.No_infiltration = PlantingArray['no_infiltration']             #Boolean that is true for some class assignments in which soil physics calculations are evaluated
        self.No_ET = PlantingArray['no_et']                                 #Boolean that is true for some class assignments in which soil physics calculations are evaluated
        self.No_stress_reduction =PlantingArray['no_stress_reduction']                #Boolean that is true if water or salt stress is not allowed to reduce plant uptake of water .
        self.No_ET_frac_Adjustment = PlantingArray['NoETFracAdjustment']   #Boolean that is true if there is no adjustment of the layers from which water is extracted due to low water content in some layers. 
        self.No_Redistribution = PlantingArray['NoRedistributionRichardsEqn']  #Boolean that is true if Richard's equation dateddddds not redistribute water between irrigations
        self.Field_capacity_restriction = PlantingArray['Field_capacity_restriction']   #Boolean that is true if water in a layer is allowed to be greater than field capacity during infiltration
        self.Irrigation_efficiency = PlantingArray['Irrigation_efficiency']
        self.LeachingFraction = PlantingArray['Leaching_fraction']          #The fraction of water that leaches below the root zone when calculating the next irrigation depth. (decimal, 5 digits)      
        self.Eliminate_surface_evaporation = PlantingArray['Eliminate_surface_evaporation']
        self.DOY_to_eliminate_surface_evaporation = PlantingArray['DOY_to_eliminate_surface_evaporation']
        self.Num_wetting_phases = PlantingArray['Num_wetting_phases']  #this is the number of wetting phases, such as 
        self.FW_phase_DOY_1 = PlantingArray['Wetting_switch_day_1']
        self.FW_phase_DOY_2 = PlantingArray['Wetting_switch_day_2']
        self.FW_phase_DOY_3 = PlantingArray['Wetting_switch_day_3']
        self.FW_phase_DOY_4 = PlantingArray['Wetting_switch_day_4']
        self.FW_phase_DOY_5 = PlantingArray['Wetting_switch_day_5']
        self.FW_Typ_1 = PlantingArray['Irrigation_type_1']
        self.FW_Type_2 = PlantingArray['Irrigation_type_2']
        self.FW_Type_3 = PlantingArray['Irrigation_type_3']
        self.FW_Type_4 = PlantingArray['Irrigation_type_4']
        self.FW_Type_5 = PlantingArray['Irrigation_type_5']

#Salinity parameters
        self.ECiw = PlantingArray['Irrigation_water_EC'] #Salinity of the irrigation water, ranges from 0 to 5, decimal, dS/m, 5 digits
        self.Max_S = PlantingArray['Maximum_soluble_EC_act'] #Maximum solubility of salts in soil solution, actual salinity, EC, dS/m, 8 digits
        self.Waste_app_DOY = PlantingArray['DOY of salinity application'] #Date of waste (manure) application   mm/dd/yyyy
        self.Waste_sal_kgha = PlantingArray['Rate_of_salinity_application_kgha'] #The kg/ha of salts in waste applied to the field, decimal, 5 digits
        self.Waste_dissolution = PlantingArray['Rate_of_dissolution'] #1/number of days for waste to dissolve, fraction, 5 digits
        self.ECe_thresh = PlantingArray['ECe_thresh'] #the threshhold ECe, below which there is no reduction in growth, real number, 5 digits
        self.b_sal = PlantingArray['b_sal'] #The slope of the yield, ECe line
        self.WasteAppTF = PlantingArray['WasteAppTF']
        
#Nitrogen parameters
        self.nit_dissolution = PlantingArray['Fertilizer_dissolution_rate'] #1/days to dissolve into soil, fraction, 5 digits
        self.Kmnl = PlantingArray['Kmnl'] # Mineralization constant /day, fraction 8 digits
        self.qlow = PlantingArray['qlow'] # Lower threshold water content for mineralization, ml/ml, fraction 5 digits
        self.qhigh = PlantingArray['qhigh'] # Upper threshold water content for mineralization, ml/ml, fraction 5 digits
        self.Qtemp = PlantingArray['Qtemp'] # Rate of change associated with 10 degree C change in temperature, dimensionless, decimal, 8 digits
        self.Onmax = PlantingArray['Surface_organic_matter'] # Organic matter content in top layer of soil, micrograms/gram of soil, real number, 8 digits
        self.alpha = PlantingArray['alpha'] # Constant for decrease in organic matter content with depth, dimensionless, fraction 8 digits
        self.Kden = PlantingArray['Kden'] #Denitrification constant, /day, fraction, 8 digits
        self.Nmin = PlantingArray['Nmin'] # M-Menton coefficient, (mg NO3-N)/(kg soil), decimal, 5 digits
        self.Km = PlantingArray['Km'] #M-Menton coefficient, (mg NO3-N)/(kg soil), decimal, 5 digits
        self.Frac_NO3 = PlantingArray['Fraction_N_req_taken_as_nitrate'] # Fraction of total nitrogen req. taken up as nitrate (vs. ammonium), decimal, 5 digits
        self.Seasonal_N_uptake = PlantingArray['Seas_N_requirement'] # Total seasonal nitrogen requirement, kg/ha, real, 5 digits
        self.Fert1_DOY = PlantingArray['DOY_of_Fert_app_1'] #Date on which first fertilization takes place mo/da/year
        self.Fert2_DOY = PlantingArray['DOY_of_Fert_app_2'] #Date on which second fertilization takes place  mo/da/year
        self.Fert3_DOY = PlantingArray['DOY_of_Fert_app_3'] #Date on which third fertilization takes place mo/da/year
        self.Fert1_rate = PlantingArray['Rate_of_application_1'] #Rate of fertilizer application 1 (kg/ha) real, 8 digits
        self.Fert2_rate = PlantingArray['Rate_of_application_2'] #Rate of fertilizer application 2 (kg/ha) real, 8 digits
        self.Fert3_rate = PlantingArray['Rate_of_application_3'] #Rate of fertilizer application 3 (kg/ha) real, 8 digits
        self.Fert_depth = PlantingArray['Depth_of_fertilizer_application']
        self.Number_fertilizations = PlantingArray['Number_of_fertilization_events'] #Number of times fertilizer is applied, Integer
        self.Constant_Km = 1
        self.Constant_Km_1 = PlantingArray['Read_in_daily_Km_values']
        self.Constant_Km_2 = PlantingArray['Adjust_Km_in_program_for_opt']
        self.Constant_Km_3 = PlantingArray['Use_constant_Km_values']
        self.N_soil_optimal = PlantingArray['Optimal_soil_nitrate_concentration'] #Optimal soil nitrate concentration for maximum yield, real, 5 digits
        self.Frac_greater_saturation = PlantingArray['Sat_uptake_above_optimal'] #Fraction of nitrate uptake greater than optimal at saturated nitrate condition, fraction, 5 digits
        self.Upper_temp_adjust = PlantingArray['Upper_limit_of_temperature_adjust'] #Upper limit of of min den adjustment for temperature, fraction, 5 digits
        self.Upper_temp_reduction = PlantingArray['Rate_of_decrease_after_upper_lim'] #Reduction rate of temp adjustment above upper limit, fraction, 5 digits
        self.Niw = PlantingArray['Irrigation_nitrate_conc'] #Irrigation water nitrate concentration (constant for season) mg/L
        self.Range_frac = PlantingArray['Fraction_of_optimal_range'] #This is used after M-Menton to assign yield decrease based on change from optimal, fraction, 5 digits
        self.Yield_decrease_below = PlantingArray['Rate_of_yield_decrease_below_N'] #Rate of yield decrease below optimal N uptake range
        self.Yield_decrease_above = PlantingArray['Rate_of_yield_decrease_above_N'] #Rate of yield decrease above optimal N uptake range
        self.Dont_fertilize_evap_layer = PlantingArray['Dont_fertilize_evap_layer']
        self.tm = PlantingArray['tm'] #Rate of yield decrease above optimal N uptake range
        self.T_bar = PlantingArray['T_bar'] #Rate of yield decrease above optimal N uptake range
        self.A0 = PlantingArray['A0'] #Rate of yield decrease above optimal N uptake range
        self.diff = PlantingArray['Soil_thermal_diffusivity']

class fields:
    def __init__(self, Field_Array):
        self.FieldNum = Field_Array['Field num']                               #The long random identifier that represents the field, for example, 9a649ac3a4353ffe6d67fdad0c6bf3a9
        self.FieldName = Field_Array['Field name']                             #The name of the field (text), which normally includes the owner and field, such as GaryField1
        self.AccountNum = int(Field_Array['Account num'])                       #The long random identifier that represents the owner, for example, 9a649ac3a4353ffe6d67fdad0c6bf3a9
        self.AccountName = Field_Array['Account name']                              #The long random identifier that represents the owner, for example, 9a649ac3a4353ffe6d67fdad0c6bf3a9
        self.Num_layers = int(Field_Array['Num_layers'])                        #The number of layers (integer), not including the evaporation layer, that will be modeled in the current planting, which may be less than the number of field layers
        self.SAV = float(Field_Array['SAV'])                                    #Suction at wetting front (cm) decimal 5 digits, used for Green Ampt infiltration
        self.H0 = float(Field_Array['H0'])                   #Depth of water ponded in field if Green Ampt is used to calculate infiltration (I do not know why this is cm but it is) (decimal 5 digits)
        self.REW = float(Field_Array['REW']) #Readily evaporable water in the evaporation layer (read in as cm, decimal, 8 digits)
        self.TEW = float(Field_Array['TEW']) #Total evaporable water in the evaporation layer (read in as cm, decimal 8 digits)
        self.NRCS_a = float(Field_Array['NRCS_a'])                                  #The SCS a value for Kostiakov infiltration (decimal, 5 digits)
        self.NRCS_b = float(Field_Array['NRCS_b'])                                  #The SCS b value for Kostiakov infiltration (decimal, 5 digits)
        self.Intake_family = float(Field_Array['Intake_family'])              #Boolean to determine whether SCS curve numbers are used to determine infiltration
        self.Water_table_simulation = int(Field_Array['Water_table_simulation']) #Boolean that is true if there is a water table and leaching is restricted by drainage system
        self.Begin_equil = int(Field_Array['Begin_with_soil_water_in_equilibrium_with_WT'])
        self.Init_zwt = float(Field_Array['Initial_water_table_elevation']) #Initial height of the water table on the day before planting (decimal, 5 digits, meters)
        self.Drain_elevation = float(Field_Array['Drain_Elevation']) #Elevation of the drain within  the soil profile (decimal, 5 digits, meters)
        self.Kirkham_rate = int(Field_Array['Drainage_controlled_by_Kirkham']) #Boolean that is true if the Kirkham algorithm is used to calculate drainage rate
        self.Drain_rate = float(Field_Array['Multiplier_for_linear']) #A multiplier that calculates drainage rate as a function of water table height (decimal, 8 digits, dimensionless) if not using Kirkham method
        self.Drain_imp = float(Field_Array['Drain_elevation_above_impermeable']) #The elevation of the drain above the impermeable layer (decimal, 8 digits, meters), currently used in Kirkham form
        self.L_drain = float(Field_Array['Distance_between_drains']) #The distance between drains (decimal, 8 digits, m), currently used in Kirkham form
        self.Keff_horizontal = float(Field_Array['Effective_lateral_K']) #Effective horizontal conductivity (m/day, 8 digits, decimal), currently used in Kirkham form
        self.re = float(Field_Array['Effective_drain_radius']) #Effective drain radius, m (decimal, 8 digits)
        self.Horizontal_distance_from_drain = float(Field_Array['Horizontal_distance_from_drain'])
        self.Kirkham_F = float(Field_Array['Kirkham_f']) #Calculated value based on drainage geometry (m/day, decimal, 8 digits)
        self.Max_layer_of_equilibrium_layers = float(Field_Array['Max_equilibrium_layer'])
        self.Equil_max_init = float(Field_Array['Starting_equilibrium_layer']) #this is the fraction of water in the soil, above which a layer is considered in equilibrium with the water table, fraction, 5 digits
        self.Keep_equilibrium_layers_out_of_root_zone = float(Field_Array['Keep_equilibrium_layers_out_of_root_zone']) #Boolean that is true if equilibrium layers in drainage simulation are not allowed to enter the root zone
        self.Fraction_of_saturation_for_equilibrium = float(Field_Array['Fraction_of_saturation_for_equilibrium']) #Fraction of saturation for equilibrium, fraction, 5 digits
        self.Continue_drainage_rate = float(Field_Array['Continue_drainage_rate'])
        self.Rain_partition = 1
        
    
class soil:
    def __init__(self, SoilArray):
        SoilArray = SoilArray.sort_values('Layer')
        self.SoilLayerNum = np.array(SoilArray['Soil layer set num'])                            #The long random identifier that represents the field, for example, 9a649ac3a4353ffe6d67fdad0c6bf3a9
        self.LayerNumber = np.array(SoilArray['Layer'])
        self.Depth = np.array(SoilArray['Depth'])  
        self.InitWC = SoilArray['InitWC']
        self.switch_wetting_phase = 400
        self.FC = np.array(SoilArray['FC'])                                #The field capactiy of the layer, percentage, decimal, 8 digits
        self.PWP = np.array(SoilArray['PWP'])                              #The permanent wilting point of the layer, percentage, decimal, 8 digits
        self.ts = np.array(SoilArray['Sat'])                               #The saturated water content of the layer, percentage, decimal, 8 digits
        self.Ksat = np.array(SoilArray['Ksat'])                            #The saturated vertical hydraulic conductivity of the layer, percentage, decimal, 8 digits
        self.av = np.array(SoilArray['alphav'])                            #Van Genuchten alpha, decimal, 8 digits
        self.nv = np.array(SoilArray['nv'])                                #Van Genuchten n, decimal, 8 digits
        self.tr = np.array(SoilArray['ResWC'])                             #Residual water content, from Brooks Corey, decimal, 8 digits
        self.Lv = np.array(SoilArray['Lv'])                                #Van Genuchten L, decimal, 8 digits
        self.Ko = np.array(SoilArray['Ko'])                                #Matching Ko (conductivity) used in Van Genuchten hydraulic conductivity equation, decimal, 8 digits
        self.InitECe = np.array(SoilArray['ECe_init'])                     #The initial ECe at the beginning of the season in the layer, dS/m, decimal, 8 digits
        self.InitsoilN = np.array(SoilArray['Initial_soil_N'])              #Initial nitrogen concentration mg/L soil
        self.Org = np.array(SoilArray['Organic_matter'])              #Initial nitrogen concentration mg/L soil
        self.dz = np.zeros([len(self.Depth)+1])                               #the thickness of the layer, m, decimal, 8 digits
        self.Z_top_ave = np.zeros([len(self.Depth)+1])                        #Half of the thickness of two layers, m, decimal, 8 digits
        self.Total_TAW = np.zeros([len(self.Depth)+1])                        #Total available water from the top of profile down to and including the layer, m, decimal, 8 digits
        self.AWC = np.zeros([len(self.Depth)+1])                              #Readily available water from the top of profile down to and including the layer, m, decimal, 8 digits
        self.RAW = np.zeros([len(self.Depth)+1])                              #Readily available water from the top of profile down to and including the layer, m, decimal, 8 digits
        self.TAW = np.zeros([len(self.Depth)+1])                              #Readily available water from the top of profile down to and including the layer, m, decimal, 8 digits
        self.bd = np.zeros([len(self.Depth)+1])                               #Bulk density of the layer, g/cm3, decimal, 8 digits
        self.zu = np.zeros([len(self.Depth)+1])
        self.zl = np.zeros([len(self.Depth)+1])
        self.Zave = np.zeros([len(self.Depth)+1])
        self.Fw = np.zeros([len(self.Depth)+1])
        self.Fw_y = np.zeros([len(self.Depth)+1])
        self.Active_EC = np.zeros([len(self.Depth)+1])
        self.Active_n = np.zeros([len(self.Depth)+1])
        self.Active_WC = np.zeros([len(self.Depth)+1])
        self.Active_dry_n = np.zeros([len(self.Depth)+1])
        self.mv = np.zeros([len(self.Depth)+1])
        
        self.InitWC = self.InitWC / 100
        self.FC = self.FC / 100
        self.PWP = self.PWP/ 100
        self.AWC = self.FC - self.PWP
        self.ts = self.ts / 100
        self.bd = (1-self.ts)*2.65
        self.tr = self.tr / 100
        self.Ksat = self.Ksat / 100
        self.Ko = self.Ko / 100
        self.Depth = self.Depth / 100
        self.dz[0] = self.Depth[0]
        self.Z_top_ave[0] = self.Depth[0] / 2
        for i in range(1, self.Num_layers+1):
            self.dz[i] = self.Depth[i] - self.Depth[i+1]
        self.dz[self.Num_layers + 1] = self.Depth[self.Num_layers + 1]
        for i in range(1, self.Num_layers + 2):
            self.Z_top_ave[i] = self.Depth[i] - self.dz[i]/2
        for i in range(1, self.Num_layers + 2):
            self.TAW[i] = self.AWC[i] * self.dz[i]
            self.RAW[i] = self.TAW[i] * self.pTable22
            self.mv[i] = 1 - 1 / self.nv[i]
        self.Total_TAW[0] = 0
        for i in range(1, self.Num_layers + 2):
            self.Total_TAW[i] = self.Total_TAW[i - 1] + self.TAW[i]
        for i in range(1, self.Num_layers + 2):
               if (i == 1):
                    self.zu[i] = self.dz[1]
                    self.zl[i] = 0
               elif i == self.Num_layers + 1:
                    self.zu[i] = self.Depth[1]
                    self.zl[i] = self.Depth[1] - self.Depth[i]
               else:
                    self.zu[i] = self.Depth[1] - self.Depth[i+1]
                    self.zl[i] = self.Depth[1] - self.Depth[i]
               self.Zave[i] = (self.zu[i] + self.zl[i]) / 2 
       

class ET_fractions:
    def __init__(self, ET_Fractions_Array):

        self.ET_fractions = np.zeros((self.Num_layers + 2, self.Num_layers + 2))

        for j in range(1, int(self.Num_layers) + 2):
            for k in range(1, int(self.Num_layers) + 2):
                    self.ET_fractions[j][k] = ET_Fractions_Array.iloc[13-k][self.Num_layers + 5-j]
                    
                    
class Wetting_fractions:
    def __init__(self, Wetting_Fractions_Array):

        self.FW_layers = np.zeros((int(self.EndDOY) + 1, int(self.Num_layers + 2)))

        for j in range(1, int(self.EndDOY) + 1):
            for k in range(1, int(self.Num_layers) + 2):
                if j < self.FW_phase_DOY_1:
                    self.FW_layers[j][k] = Wetting_Fractions_Array.iloc[0][4+k]
                elif j < self.FW_phase_DOY_2:
                    self.FW_layers[j][k] = Wetting_Fractions_Array.iloc[1][4+k]
                elif j < self.FW_phase_DOY_3:
                    self.FW_layers[j][k] = Wetting_Fractions_Array.iloc[2][4+k]
                elif j < self.FW_phase_DOY_4:
                    self.FW_layers[j][k] = Wetting_Fractions_Array.iloc[3][4+k]
                else:
                    self.FW_layers[j][k] = Wetting_Fractions_Array.iloc[4][4+k]
                    
class irrigation:
    def __init__(self, IrrigationArray):
        self.Irrigation_depth = np.zeros(self.NumDaysInc+1)
        self.Depth_ref = np.array(IrrigationArray['Ref_mm']) 
        Sec_name = 'Sec_' + str(int(self.IrrSection))
        self.Multiplier = np.array(IrrigationArray[Sec_name])
        self.IrrigationDOY = np.array(IrrigationArray['DOY'])
        for i in range(0, len(IrrigationArray)):
            if(self.IrrigationDOY[i]-self.SimStartDOY)<len(self.Irrigation_depth):
                self.Irrigation_depth[int(self.IrrigationDOY[i])-int(self.SimStartDOY)+1] = self.Depth_ref[i]*self.Multiplier[i]


class status:
    def __init__(self, Status_Array):

        self.Water_Start = np.zeros(len(Status_Array)+1)                              #Readily available water from the top of profile down to and including the layer, m, decimal, 8 digits
        self.Salinity_Start = np.zeros(len(Status_Array)+1)                              #Readily available water from the top of profile down to and including the layer, m, decimal, 8 digits
        self.Nitrogen_Start = np.zeros(len(Status_Array)+1)                              #Readily available water from the top of profile down to and including the layer, m, decimal, 8 digits

        for k in range(1, int(self.Num_layers) + 2):
            self.Water_Start[k] = Status_Array['InitWC'].loc[(Status_Array['Layer']==k) & (Status_Array['Planting num'] == self.PlantingNum)]
            self.Salinity_Start[k] = Status_Array['ECe_init'].loc[(Status_Array['Layer']==k) & (Status_Array['Planting num'] == self.PlantingNum)]
            self.Nitrogen_Start[k] = Status_Array['Initial_soil_N'].loc[(Status_Array['Layer']==k) & (Status_Array['Planting num'] == self.PlantingNum)]
                    
class output:
    def __init__(self):
        self.NumDaysInc = int(self.NumDays)
        self.DOY = [self.StartDOY + x for x in range(0, self.NumDaysInc)]
        self.PlantingIDO = np.empty(self.NumDaysInc, dtype = object)                  #The long random identifier that represents the planting, for example, 9a649ac3a4353ffe6d67fdad0c6bf3a9
        self.PlantingNameO = np.empty(self.NumDaysInc, dtype = object)                 #The name of the planting (text), normally includes owner name, field name, crop, and year, such as GaryField1Wheat2017
        self.LocationO = np.zeros(self.NumDaysInc)                     #The position (location) in the planting, integer
        self.NDVI = np.zeros(self.NumDaysInc)                          #The NDVI measured by remote sensing for the location, decimal 8 digits
        self.NDVI_regression = np.zeros(self.NumDaysInc)               #The interpolated NDVI by regression, decimal 8 digits
        self.Kcb_NDVI = np.zeros(self.NumDaysInc)                      #The Kcb calculated from the NDVI regression, decimal 8 digits
        self.Kcb_calculated = np.zeros(self.NumDaysInc)                #The Kcb calculated from FAO equations, decimal 8 digits
        self.Kcb = np.zeros(self.NumDaysInc)                           #The Kcb used in the program, decimal 8 digits                            
        self.one_minus_c = np.zeros(self.NumDaysInc)                   #The one minus the fraction of the canopy area (ground area fraction), decimal 8 digits
        self.Crop_height = np.zeros(self.NumDaysInc)        #The h8 of the crop in meters, decimal 8 digits
        self.Root = np.zeros(self.NumDaysInc)                #The depth of the root in meters, decimal 8 digits
        self.Ke = np.zeros(self.NumDaysInc)                       #The evaporation coefficient, decimal 8 digits
        self.E = np.zeros(self.NumDaysInc)                       #The evaporation from the soil surface, mm, decimal 8 digits
        self.ET_trans = np.zeros(self.NumDaysInc)        #The transpiration from the plant, mm, decimal 8 digits
        self.ET = np.zeros(self.NumDaysInc)                         #The evapotranspiration from the crop, mm, decimal 8 digits
        self.ET_pot = np.zeros(self.NumDaysInc)         #The potential transpiration from the crop, decimal 8 digits
        self.ETcum = np.zeros(self.NumDaysInc)      #The cumulative potential evapotranspiration for the season, decimal 8 digits
        self.ET_actual_cum = np.zeros(self.NumDaysInc)#The cumulative actual evapotranspiration for the season, decimal 8 digits
        self.ET_refO = np.zeros(self.NumDaysInc)
        self.Ky = np.zeros(self.NumDaysInc)                           #The daily crop sensitivity to water stress
        self.Depletion_total = np.zeros(self.NumDaysInc)  #The depth of depletion, mm, decimal 8 digits
        self.Allowable_depletion_total = np.zeros(self.NumDaysInc)
        self.Percent_depletion_total = np.zeros(self.NumDaysInc) #The percent depletion, percentage, decimal 8 digits
        self.Irrigation = np.zeros(self.NumDaysInc)           #The depth of irrigation applied, mm, decimal 8 digits
        self.Total_Rain_plus_irrigation = np.zeros(self.NumDaysInc)           #The depth of irrigation applied, mm, decimal 8 digits
        self.P = np.zeros(self.NumDaysInc)                           #The management allowed depletion, fraction, decimal 8 digits
        self.Rainfall = np.zeros(self.NumDaysInc)                #The rainfall depth, mm, decimal 8 digits
        self.Rain_Infilt = np.zeros(self.NumDaysInc)
        self.wet_Rain_Infilt = np.zeros(self.NumDaysInc)
        self.FCave = np.zeros(self.NumDaysInc)                 #The average field capacity for soil profilel, decimal 8 digits
        self.PWPave = np.zeros(self.NumDaysInc)                #The average permanent wilting point for soil profilel, decimal 8 digits
        self.TAWsum = np.zeros(self.NumDaysInc)                #The average permanent wilting point for soil profilel, decimal 8 digits
        self.RAWsum = np.zeros(self.NumDaysInc)                #The average permanent wilting point for soil profilel, decimal 8 digits
        self.AW =np.zeros(self.NumDaysInc)                 #The amount of water left in the soil for the plant, mm, decimal 8 digits
        self.VWCave = np.zeros(self.NumDaysInc)                #The average volumetric water content for the soil profile, fraction, decimal 8 digits
        self.TDW = np.zeros(self.NumDaysInc)                   #The total depth of water in the soil profile, mm, decimal 8 digits           
        self.zwt = np.zeros(self.NumDaysInc)                   #The water table elevation above the datum, m, decimal 8 digits
        self.Equilibrium_Max = np.zeros(self.NumDaysInc)       #The number of the upper layer that is in equilibrium with the water table, integer
        self.zu_Eq_Max = np.zeros(self.NumDaysInc)       #The number of the upper layer that is in equilibrium with the water table, integer
        self.Ks = np.zeros(self.NumDaysInc)                    #Ks which is the fraction of decreased evapotranspiration due to limited water, decimal, 8 digits
        self.Irr_Sal = np.zeros(self.NumDaysInc)              #The salt mass added by irrigation water, mg/L m, decimal, 8 digits
        self.Waste_sal = np.zeros(self.NumDaysInc)            #The salt mass added by waste, mg/L m, decimal, 8 digits
        self.Irr_Salt_Added = np.zeros(self.NumDaysInc)               #The salt mass lost by seepage, mg/L m, decimal, 8 digits
        self.Waste_Salt_Added = np.zeros(self.NumDaysInc)           #The mass balance of all salts added or lost, mg/L m, decimal, 8 digits
        self.Seepage = np.zeros(self.NumDaysInc)               #The salt mass lost by seepage, mg/L m, decimal, 8 digits
        self.SumOfFluxes = np.zeros(self.NumDaysInc)           #The mass balance of all salts added or lost, mg/L m, decimal, 8 digits
        self.Total_salt = np.zeros(self.NumDaysInc)              #Total mass of salt in the root zone, mg/L m, decimal, 8 digits      
        self.SaltDiff = np.zeros(self.NumDaysInc)              #Difference in total salt between day before and present day (should equal sum of fluxes), mg/L m, decimal, 8 digits
        self.Ks_salt = np.zeros(self.NumDaysInc)                #The reduction in ET due to salt stress, fraction, 5 digits
        self.Ks_nit = np.zeros(self.NumDaysInc)                  #The reduction in ET due to nitrogen stress, fraction, 5 digits
        self.TotalIrrN = np.zeros(self.NumDaysInc)         #Total nitrate added by irrigation to soil profile on each day, mg/L m, decimal, 8 digits
        self.TotalDrainN = np.zeros(self.NumDaysInc)          #Total nitrate removed by drainage from soil profile on each day, mg/L m, decimal, 8 digits
        self.SumReactionsN = np.zeros(self.NumDaysInc)       #Total of daily reactions (should equal sum of four rections), mg/L m, decimal, 8 digits
        self.SumFluxReactionsN = np.zeros(self.NumDaysInc)  #Total of daily fluxes and reactions (should equal mass difference), mg/L m, decimal, 8 digits
        self.Total_Min = np.zeros(self.NumDaysInc)          #Total mineralization in soil profile on each day, mg/L m, decimal, 8 digits
        self.Total_Den = np.zeros(self.NumDaysInc)         #Total denitrification in soil profile on each day, mg/L m, decimal, 8 digits
        self.Total_Fer = np.zeros(self.NumDaysInc)        #Total fertilization in soil profile on each day, mg/L m, decimal, 8 digits
        self.Total_Upt = np.zeros(self.NumDaysInc)         #Total uptake in soil profile on each day, mg/L m, decimal, 8 digits
        self.UptakeReq = np.zeros(self.NumDaysInc)         #Plant uptake requirement, mg/L m, decimal, 8 digit
        self.Total_nit = np.zeros(self.NumDaysInc)          #Total nitrate in soil profile on each day, mg/L m, decimal, 8 digits
        self.Total_nit_accum = np.zeros(self.NumDaysInc)          #Total nitrate accumulated in season, mg/L m, decimal, 8 digits
        self.N_ave = np.zeros(self.NumDaysInc)                #Total mineralization in soil profile on each day, mg/L m, decimal, 8 digits
        self.N_optimal_low = np.zeros(self.NumDaysInc)   #'Calculated with range_frac in N simulation section, lower limit of optimal soil N mg/kg
        self.N_optimal_high = np.zeros(self.NumDaysInc) #'Calculated with range_frac in N simulation section, upper limit of optimal soil N mg/kg
        self.Cum_Min = np.zeros(self.NumDaysInc)              #Cumulative mineralization in soil profile during season, mg/L m, decimal, 8 digits
        self.Cum_Den = np.zeros(self.NumDaysInc)             #Cumulative denitrification in soil profile during season, mg/L m, decimal, 8 digits
        self.Cum_Fer = np.zeros(self.NumDaysInc)             #Cumulative fertilization in soil profile during season, mg/L m, decimal, 8 digits
        self.Cum_Upt = np.zeros(self.NumDaysInc)              #Cumulative uptake in soil profile during season, mg/L m, decimal, 8 digits
        self.CumIrrN = np.zeros(self.NumDaysInc)             #Cumulative nitrate added by irrigation to soil profile during season, mg/L m, decimal, 8 digits
        self.CumDrnN = np.zeros(self.NumDaysInc)             #Cumulative nitrate removed by drainage from soil profile during season, mg/L m, decimal, 8 digits
        self.CumChangeN = np.zeros(self.NumDaysInc)       #Cumulative nitrate change in soil profile during season, mg/L m, decimal, 8 digits
        self.EC_leach_eqn = np.zeros(self.NumDaysInc)
        self.Ks_water_total = np.zeros(self.NumDaysInc)
        self.Kcmax = np.zeros(self.NumDaysInc)
        self.Kr = np.zeros(self.NumDaysInc)
        self.Few = np.zeros(self.NumDaysInc)
        self.E_wet = np.zeros(self.NumDaysInc)
        self.Rain_infilt = np.zeros(self.NumDaysInc)
        self.dry_Rain_infilt = np.zeros(self.NumDaysInc)
        self.wet_Rain_infilt = np.zeros(self.NumDaysInc)
        self.ET_trans_wet = np.zeros(self.NumDaysInc)
        self.Ps = np.zeros(self.NumDaysInc)
        self.ECe_ave_effective = np.zeros(self.NumDaysInc)
        self.Fert1 = np.zeros(self.NumDaysInc)
        self.Fert2 = np.zeros(self.NumDaysInc)
        self.Fert3 = np.zeros(self.NumDaysInc)
        self.Fert = np.zeros(self.NumDaysInc)
        self.Irr_Nit = np.zeros(self.NumDaysInc)
        self.N_leach_eqn = np.zeros(self.NumDaysInc)
        self.N_upt = np.zeros(self.NumDaysInc)
        self.N_max = np.zeros(self.NumDaysInc)
        self.mupt_entire_profile = np.zeros(self.NumDaysInc)   
        self.Nitrogen_Kcb = np.zeros(self.NumDaysInc)   
        self.KN_low = np.zeros(self.NumDaysInc)   
        self.KN_high = np.zeros(self.NumDaysInc)
        
        
        for j in range(1, self.NumDaysInc - 1):
            adj_j = j + self.StartDOY - self.PlantingDOY
            if int(self.Select_Kcb) == 2:
                if adj_j < 0:
                    self.Kcb[j] = 0
                elif adj_j < self.IP:
                    self.Kcb[j] = self.IKcb
                elif adj_j < self.IP + self.DP:
                    self.Kcb[j] = self.IKcb + (adj_j - self.IP) / (self.DP) * (self.MKcb - self.IKcb)
                elif adj_j < self.IP + self.DP + self.MP:
                    self.Kcb[j] = self.MKcb
                elif adj_j < self.IP + self.DP + self.MP + self.LP:
                    self.Kcb[j] = self.MKcb + (adj_j - (self.IP + self.DP + self.MP)) / (self.LP) * (self.EKcb - self.MKcb)
                elif adj_j < self.IP + self.DP + self.MP + self.LP + self.EP:
                    self.Kcb[j] = self.EKcb
                elif adj_j < self.IP + self.DP + self.MP + self.LP + self.EP + self.DP_2:
                    self.Kcb[j] = self.EKcb + (adj_j - (self.IP + self.DP + self.MP + self.LP + self.EP)) / (self.DP_2) * (self.MKcb_2 - self.EKcb)
                elif adj_j < self.IP + self.DP + self.MP + self.LP + self.EP + self.DP_2 + self.MP_2:
                    self.Kcb[j] = self.MKcb_2
                elif adj_j < self.IP + self.DP + self.MP + self.LP + self.EP + self.DP_2 + self.MP_2 + self.LP_2:
                    self.Kcb[j] = self.MKcb_2 + (adj_j - (self.IP + self.DP + self.MP + self.LP + self.EP + self.DP_2 + self.MP_2)) / (self.LP_2) * (self.EKcb_2 - self.MKcb_2)
                else:
                    self.Kcb[j] = self.EKcb_2
                    
#1 - c#1 - c#1 - c#1 - c#1 - c#1 - c#1 - c#1 - c#1 - c#1 - c#1 - c#1 - c
                if adj_j < 0:
                    self.one_minus_c[j] = 1
                elif adj_j < self.ICP:
                    self.one_minus_c[j] = self.IC
                elif adj_j < self.ICP + self.DCP:
                    self.one_minus_c[j] = self.IC - (adj_j - self.ICP) / self.DCP * (self.IC - self.MC)
                elif adj_j < self.ICP + self.DCP + self.MCP:
                    self.one_minus_c[j] = self.MC
                elif adj_j < self.ICP + self.DCP + self.MCP + self.ECP:
                    self.one_minus_c[j] = self.MC - (adj_j - self.ICP - self.DCP - self.MCP) / self.ECP * (self.MC - self.EC)
                else:
                    self.one_minus_c[j] = self.EC
#crop height
                if adj_j < 0:
                    self.Crop_height[j] = 0
                elif adj_j < self.ICP:
                    self.Crop_height[j] = self.minH
                elif adj_j < self.ICP + self.DCP:
                    self.Crop_height[j] = self.minH + (adj_j - self.ICP) / self.DCP * (self.midH - self.minH)
                elif adj_j < self.DCP + self.MCP + self.ICP:
                    self.Crop_height[j] = self.midH
                elif adj_j < self.DCP + self.MCP + self.ICP + self.ERH:
                    self.Crop_height[j] = self.midH + (adj_j - self.ICP - self.DCP - self.MCP) / self.ECP * (self.endH - self.midH)
                else:
                    self.Crop_height[j] = self.endH
#'roots
                if adj_j < 0:
                    self.Root[j] = self.IR * 1000
                elif adj_j < self.ICP:
                    self.Root[j] = self.IR * 1000
                elif adj_j < self.ICP + self.DCP:
                    self.Root[j] = (self.IR + (adj_j - self.ICP) / self.DCP * (self.DR - self.IR)) * 1000
                elif adj_j < self.DCP + self.MCP + self.ICP:
                    self.Root[j] = self.DR * 1000
                elif adj_j < self.DCP + self.MCP + self.ICP + self.ERH:
                    self.Root[j] = (self.DR + (adj_j - self.ICP - self.DCP - self.MCP) / self.ERH * (self.FR - self.DR)) * 1000
                else:
                    self.Root[j] = self.FR * 1000
                    
            self.Ps[1] = self.pTable22                
        
        if self.Salinity_simulation == 1:
            if self.WasteAppTF == 1:
                self.waste_app_day = (self.waste_app_date - self.DateP).days
            else:
                self.waste_app_day = 10000
            for j in range(1, self.NumDaysInc):
                if self.StartDOY > self.SimStartDOY:
                    adj_j = j + self.StartDOY
                else:
                    adj_j = j + self.SimStartDOY
                self.Irr_Sal[j] = self.ECiw
                self.EC_leach_eqn[j] = 0
                if adj_j - self.waste_app_day > 0 and adj_j - self.waste_app_day - 1 < 1/self.Waste_dissolution:
                    self.Waste_sal[j] = self.Waste_dissolution * self.Waste_sal_kgha

        if self.Nitrogen_simulation == 1:
            self.KN_low[j]= 1.2
            self.KN_high[j] = 1.2
            if self.WasteAppTF == 1:
                self.Fert1_day = (self.Fert1_date - self.DateP).days
                self.Fert2_day = (self.Fert2_date - self.DateP).days
                self.Fert3_day = (self.Fert3_date - self.DateP).days
            else:
                self.Fert1_day = 10000
                self.Fert2_day = 10000
                self.Fert3_day = 10000

            self.Nitrogen_frac_sum = 0

            for j in range(1, self.NumDaysInc):
                if self.StartDOY >= self.SimStartDOY:
                    adj_j = j + self.StartDOY
                else:
                    adj_j = j + self.SimStartDOY
                self.Fert[j] = 0
                self.Irr_Nit[j] = self.Niw
                self.N_leach_eqn[j] = 0
                if self.Number_fertilizations > 0 and adj_j - self.Fert1_day > 0 and adj_j - self.Fert1_day - 1 < 1/self.nit_dissolution:
                    self.Fert1[j] = self.nit_dissolution * self.Fert1_rate
                if self.Number_fertilizations > 1 and adj_j - self.Fert2_day > 0 and adj_j - self.Fert2_day - 1 < 1/self.nit_dissolution:
                    self.Fert2[j] = self.nit_dissolution * self.Fert2_rate
                if self.Number_fertilizations > 2 and adj_j - self.Fert3_day > 0 and adj_j - self.Fert3_day - 1 < 1/self.nit_dissolution:
                    self.Fert3[j] = self.nit_dissolution * self.Fert3_rate
                self.Fert[j] = self.Fert1[j] + self.Fert2[j] + self.Fert3[j]   
                
                # if adj_j < self.dev:
                if adj_j < self.IP:
                    self.Nitrogen_Kcb[j] = 0
                elif adj_j < self.IP + self.DP:
                    self.Nitrogen_Kcb[j] = (self.MKcb - self.IKcb) * ((adj_j - self.IP) / (self.IP + self.DP - self.IP))
                    # self.Nitrogen_Kcb[j] = (self.Kcb_mid - self.Kcb_initial) * ((adj_j - self.dev) / (self.mid - self.dev))
                elif adj_j < self.LP:
                    self.Nitrogen_Kcb[j] = self.MKcb - self.IKcb
                elif adj_j < self.EP:
                    self.Nitrogen_Kcb[j] = self.MKcb - self.IKcb - (self.MKcb - self.Kcb_end) * ((adj_j - self.EP) / (self.EP - self.LP))
                else:
                   self.Nitrogen_Kcb[j] = 0
                self.Nitrogen_frac_sum = self.Nitrogen_frac_sum + self.Nitrogen_Kcb[j]
                if self.Nitrogen_frac_sum == 0:
                    self.Nitrogen_frac_sum = 1

class output_layers:
    def __init__(self, Status_Array):
        self.DAP = np.zeros((self.NumDaysInc, self.Num_layers + 2))                      #days after planting, integer
        self.PlantingIDL = np.zeros((self.NumDaysInc, self.Num_layers + 2))              #The long random identifier that represents the planting, for example, 9a649ac3a4353ffe6d67fdad0c6bf3a9
        self.PlantingNameL = np.zeros((self.NumDaysInc, self.Num_layers + 2))            #The name of the planting (text), normally includes owner name, field name, crop, and year, such as GaryField1Wheat2017
        self.LocationL = np.zeros((self.NumDaysInc, self.Num_layers + 2))                #The position (location) in the planting, integer
        self.Layer = np.zeros((self.NumDaysInc, self.Num_layers + 2))                    #The layer, integer        
        self.WC = np.zeros((self.NumDaysInc - 1, self.Num_layers + 2))                       #The water content in the soil layer, decimal, 8 digits
        self.Depletion = np.zeros((self.NumDaysInc, self.Num_layers + 2))                #The depletion of water below field capacity (mm) in the soil layer, decimal, 8 digits
        self.Act_frac = np.zeros((self.NumDaysInc, self.Num_layers + 2))                 #The fraction of total evaporated water that is removed from each soil layer, decimal, 8 digits
        self.Infilt = np.zeros((self.NumDaysInc, self.Num_layers + 2))                   #The fraction of totol ET water that is evaporated from the particular layer, decimal, 8 digits
        self.Percent_depletion = np.zeros((self.NumDaysInc, self.Num_layers + 2))        #The percent of the water between field capacity and permanent wilting point that is depleted from the layer, decimal, 8 digits
        self.EC = np.zeros((self.NumDaysInc, self.Num_layers + 2))                       #The electrical conductivity of the actual water in the layer, dS/m, decimal, 8 digits
        self.ECe = np.zeros((self.NumDaysInc, self.Num_layers + 2))                      #The electrical conductivity of the saturated paste extract from the layer, dS/m, decimal, 8 digits
        self.Mass_salt = np.zeros((self.NumDaysInc, self.Num_layers + 2))                #The total mass of salt in the layer, decimal, 8 digits
        self.N = np.zeros((self.NumDaysInc, self.Num_layers + 2))                        #Nitrate concentration in soil water, mg/L, decimal, 8 digits
        self.N_soil = np.zeros((self.NumDaysInc, self.Num_layers + 2))                   #Nitrate concentration per mass of soil in each layer, mg/kg, decimal, 8 digits
        self.hc = np.zeros((self.NumDaysInc, self.Num_layers + 2))                   #Nitrate concentration per mass of soil in each layer, mg/kg, decimal, 8 digits
        self.WC_test = np.zeros((self.Num_layers + 2, 102))
        self.WC_depth = np.zeros((self.NumDaysInc, self.Num_layers + 2))
        self.Sum_depths = np.zeros(self.NumDaysInc)
        self.Difference = np.zeros(self.NumDaysInc)
        self.Irrigation_plus_rain = np.zeros(self.NumDaysInc)
        self.ET_total = np.zeros(self.NumDaysInc)
        self.Sum_sources_and_sinks = np.zeros(self.NumDaysInc)
        self.Bottom_layer = np.zeros(self.NumDaysInc)
        self.ts_depth = np.zeros(self.Num_layers + 2)
        self.Total_TAW_Fw = np.zeros((self.NumDaysInc, self.Num_layers + 3))
        self.Uptake = np.zeros((self.NumDaysInc, self.Num_layers + 2))
        self.fmntemp = np.zeros((self.NumDaysInc, self.Num_layers + 2))
        self.kgha = np.zeros((self.NumDaysInc, self.Num_layers + 2))
        self.Net_accumulation = np.zeros((self.NumDaysInc, self.Num_layers + 2))
        self.Cum_Drain = np.zeros((self.NumDaysInc, self.Num_layers + 2))
        self.Cum_Irr = np.zeros((self.NumDaysInc, self.Num_layers + 2))
        self.Cum_Total = np.zeros((self.NumDaysInc, self.Num_layers + 2))
        
        # if len(Output_Layer_Array[Output_Layer_Array['Layer']==1].index.values) > 0:
        #     kk = int(Output_Layer_Array[Output_Layer_Array['Layer']==1].index.values)
        
        for k in range(1, self.Num_layers + 2):
            self.WC[0][k] = Status_Array['InitWC'].loc[Status_Array['Layer']==k]/100
            self.Depletion[0][k] = (self.FC[k] - self.WC[0][k]) * self.dz[k] * self.FW_layers[1][k]
            self.Percent_depletion[0][k] = (self.FC[k] - self.WC[0][k]) / (self.FC[k] - self.PWP[k])
        self.WC[0][0] = self.WC[0][1]
        for j in range(1, self.NumDaysInc - 1):
            self.Total_TAW_Fw[j][self.Num_layers + 2] = 0
            for k in range(self.Num_layers + 1, 0, -1):
                self.Total_TAW_Fw[j][k] = self.Total_TAW_Fw[j][k+1] + self.TAW[k]*self.FW_layers[j][k]            
            k = self.Num_layers + 1
            while self.Depth[k] < self.Root[j]/1000:
                k = k - 1
            self.Bottom_layer[j] = k
            if self.Bottom_layer[j] < 1:
                self.Bottom_layer[j] = 1
            self.FCave[j] = 0
            self.PWPave[j] = 0
            self.TAWsum[j] = 0
            for k in range(int(self.Bottom_layer[j]), self.Num_layers + 2):
                self.FCave[j] = self.FC[k] + self.FCave[j]    
                self.PWPave[j] = self.PWP[k] + self.PWPave[j]  
                self.TAWsum[j]= self.TAWsum[j] + (self.FC[k] - self.PWP[k]) * self.dz[k]
            self.RAWsum[j] = self.TAWsum[j] * self.Ps[j]
            self.FCave[j] = self.FCave[j] / (self.Num_layers - self.Bottom_layer[j] + 1)
            self.PWPave[j] = self.PWPave[j] / (self.Num_layers - self.Bottom_layer[j] + 1)
        sum_ET = 0
        for k in range(int(self.Bottom_layer[1]), self.Num_layers + 2):
            sum_ET = sum_ET + self.ET_fractions[1][k]

        if self.No_ET_frac_Adjustment == 1:
            for k in range(1, self.Num_layers + 2):
                self.Act_frac[1][k] = self.ET_fractions[1][k] / sum_ET
        else:
            Sum_act_frac = 0
            for k in range(self.Num_layers + 1, int(self.Bottom_layer[1]) - 1, -1):
                self.RAW[k] = self.Ps[1] * self.TAW[k]
                if self.Fw[k] < self.Fw_y[k]:
                    self.Depletion[0][k] = self.Depletion[0][k] * self.Fw[k] / self.Fw_y[k]
                if (self.Depletion[0][k] > self.RAW[k] * self.Fw[k]) and (self.Depletion[0][k] < self.TAW[k] * self.Fw[k]):
                    self.Act_frac[1][k] = self.ET_fractions[j][k] * (self.TAW[k] * self.Fw[k] - self.Depletion[0][k]) / ((self.TAW[k] - self.RAW[k]) * self.Fw[k])/sum_ET
                elif self.Depletion[0][k] > self.TAW[k] * self.Fw[k]:
                    self.Act_frac[1][k] = 0
                else:
                    self.Act_frac[1][k] = self.ET_fractions[1][k]/sum_ET
                Sum_act_frac = Sum_act_frac + self.Act_frac[1][k]
            
            if Sum_act_frac > 0:
                for k in range(self.Num_layers + 1, int(self.Bottom_layer[1]) - 1, -1):
                    self.Act_frac[1][k] = self.Act_frac[1][k] / Sum_act_frac

        if self.Salinity_simulation == 1:
            for k in range(1, self.Num_layers + 2):
                self.ECe[0][k] = self.InitECe[k]
                self.EC[0][k] = self.ECe[0][k] / self.WC[0][k] * self.ts[k]  
            Act_frac_sum = 0
            for k in range(self.Num_layers, int(self.Bottom_layer[1]) - 1, -1):
                self.ECe_ave_effective[1] = self.ECe_ave_effective[1] + self.Act_frac[1][k] * self.ECe[0][k] * self.FC[k] / self.WC[0][k]
                Act_frac_sum = Act_frac_sum + self.Act_frac[1][k]
            if Act_frac_sum == 0:
                Act_frac_sum = 1
            self.ECe_ave_effective[1] = self.ECe_ave_effective[1] / Act_frac_sum
            self.Total_salt[0] = 0
            for k in range(1, self.Num_layers + 2):
                self.Total_salt[0] = self.Total_salt[0] + self.EC[0][k] * 640 * self.WC[0][k] * self.dz[k] * self.Fw[k]
            for k in range(1, self.Num_layers + 2):
                self.Active_EC[k] = self.EC[0][k]
                                    #The electrical conductivity of the actual water in the layer, dS/m, decimal, 8 digits
        if self.Nitrogen_simulation == 1:
            for k in range(1,  self.Num_layers + 2):
                self.N_soil[0][k] = self.InitsoilN[k]       #Nitrate concentration per mass of soil in each layer, mg/kg, decimal, 8 digits
                self.N[0][k] = self.N_soil[0][k] * self.bd[k] /self.WC[0][k]                #Nitrate concentration in soil water, mg/L, decimal, 8 digits
                self.kgha[0][k] = self.N[0][k] * self.dz[k] * 10 * self.WC[0][k]
            for i in range(1, self.NumDaysInc):
                self.N_upt[i] = self.Seasonal_N_uptake * self.Nitrogen_Kcb[i] / self.Nitrogen_frac_sum
                temp = self.T_bar + self.A0 * np.sin(2 * 3.14159 / 365 * (self.DOY[i] - self.tm))
                for k in range(1, self.Num_layers + 1):
                    self.fmntemp[i][k] = self.Qtemp ** ((temp - 20) / 10)
                    if self.fmntemp[i][k] > 1.5:
                        self.fmntemp[i][k] = 1.5 - (self.fmntemp[i][k] - 1.5) / 5

    def Create_output_layer_arrays(self, Num, Num_days, Num_layers):
        self.date_layer_out = np.empty(Num, dtype = dt)
        self.pid_layer_out  = np.empty(Num, dtype = object)
        self.planting_name_layer_out =  np.empty(Num, dtype = object)
        self.Days_after_planting_layer = np.empty(Num)
        self.layer_out = np.zeros(Num)
        self.WC_layer_out = np.zeros(Num)
        self.EC_out = np.zeros(Num)
        self.N_out = np.zeros(Num)
        self.Depletion_layer_out = np.zeros(Num)
        self.ActFrac_layer_out = np.zeros(Num)
        self.Infiltration_layer_out =  np.zeros(Num)
        self.Percent_depletion_layer_out = np.zeros(Num)
        self.EC_layer_out = np.zeros(Num)
        self.ECe_layer_out = np.zeros(Num)
        self.Mass_salt_layer_out = np.zeros(Num)
        self.N_layer_out = np.zeros(Num)
        self.N_soil_layer_out = np.zeros(Num)

class model(plantings, weather, fields, status, soil, ET_fractions, Wetting_fractions, output, output_layers, irrigation, ET_daily, RS_daily):
    def __init__(self, Planting_Array,
                 Weather_Array, 
                 Field_Array, 
                 Status_Array,
                 Soil_Array,
                 ETfrac_Array, 
                 Wetting_Array, 
                 Irrigation_Array,
                 ET_Daily_Array,
                 RS_Daily_Array):
        plantings.__init__(self, Planting_Array)
        weather.__init__(self, Weather_Array)
        fields.__init__(self, Field_Array)
        status.__init__(self, Status_Array)
        soil.__init__(self, Soil_Array)
        ET_fractions.__init__(self, ETfrac_Array)
        Wetting_fractions.__init__(self, Wetting_Array)
        output.__init__(self)
        output_layers.__init__(self, Status_Array)
        irrigation.__init__(self, Irrigation_Array)
        ET_daily.__init__(self, ET_Daily_Array)
        RS_daily.__init__(self, RS_Daily_Array)
                
    def run_model(self):
        print('I am here')
        for j in range(1, int(self.NumDays) - 1):
            BL: int = int(self.Bottom_layer[j])
            for k in range(1, self.Num_layers + 2):
                self.Fw[k] = self.FW_layers[j][k]
                self.Fw_y[k]  = self.FW_layers[j - 1][k]
            if int(self.Select_Kcb) == 1:
                if self.Daily_Kcb[j] > self.Kcb_initial:
                    self.Kcb[j] = self.Daily_Kcb[j]
                    self.Root[j] = self.Daily_Root[j]
                    self.Crop_height[j] = self.Daily_crop_height[j]
            self.Depletion_total[j - 1] =  0
            for k in range(self.Num_layers + 1, BL - 1, -1):
                self.Percent_depletion[j][k] = (self.FC[k] - self.WC[j-1][k]) /(self.FC[k] - self.PWP[k]) * 100
                self.Depletion_total[j - 1] = self.Depletion_total[j - 1] + (self.FC[k] - self.WC[j - 1][k]) * self.dz[k] *  self.Fw_y[k]
            self.Percent_depletion_total[j-1] = self.Depletion_total[j-1] / self.Total_TAW_Fw[j][BL] * 100
            self.Allowable_depletion_total[j-1] = self.Total_TAW_Fw[j-1][BL]*self.Ps[j-1]
            if self.Neglect_upper_layer_in_depletion_calc == 1:
                self.Percent_depletion_total[j - 1] = (self.Depletion_total[j - 1] - (self.FC[self.Num_layers + 1] - self.WC[j - 1][self.Num_layers + 1]) * self.dz[self.Num_layers + 1] * self.Fw_y[self.Num_layers + 1]) / (self.Total_TAW_Fw[j][BL] - self.TAW[self.Num_layers + 1] * self.Fw_y[self.Num_layers + 1]) * 100
            if self.adjust_P == 1:
                if self.Ksat[self.Num_layers + 1] * 100 / 24 > 50:
                    p_adj = self.pTable22 + 0.1
                elif (self.Ksat[self.Num_layers + 1] * 100 / 24) > 25:
                    p_adj = self.pTable22 +0.05
                elif self.Ksat[self.Num_layers + 1] * 100 / 24 < 0.5:
                    p_adj = self.pTable22 -  0.1
                elif self.Ksat[self.Num_layers + 1] * 100 / 24 < 2.5:
                    p_adj = self.pTable22 - 0.05
                else:
                    p_adj = self.pTable22
                if j == 1: 
                    self.ET_trans[j - 1] = 5
                self.Ps[j] = p_adj + 0.04 * (5 - (self.ET_trans[j - 1]))
            else:
                self.Ps[j] = self.pTable22
            
            if int(self.Select_Kcb) == 6:
                self.Ps[j] = 0.75
            
            #this is for showing the dynamic simulation 
            
            self.RAWsum[j] = self.TAWsum[j] * self.Ps[j]
            self.Ks_water_total[j] = (self.Total_TAW_Fw[j][BL] - self.Depletion_total[j - 1]) / ((1 - self.Ps[j]) * self.Total_TAW_Fw[j][BL])
            if self.Ks_water_total[j] < 0: 
                self.Ks_water_total[j] = 0
            self.Ks[j] = self.Ks_water_total[j]
                    
            if self.Ks[j] > 1:
                self.Ks[j] = 1
        
            if self.Salinity_simulation == 1:
                self.Ks_salt[j] = 1 - self.b_sal / (100) * (self.ECe_ave_effective[j - 1] - self.ECe_thresh)
                if self.Ks_salt[j] > 1: 
                    self.Ks_salt[j] = 1
                if self.Ks_salt[j] < 0: 
                    self.Ks_salt[j] = 0
            else:
                self.Ks_salt[j] = 1
        
            if self.TEW > 0:
               
                if self.RH_min[j] < 20:
                    RH_used = 20
                else:
                    RH_used = self.RH_min[j]
        
                self.Kcmax[j] = 1.2 + (0.04 * (self.WS[j - 1] - 2) - 0.004 * (RH_used - 45)) * (self.Crop_height[j] / 3) ** 0.3
                
                if self.Kcb[j] + 0.05 > self.Kcmax[j]:
                    self.Kcmax[j] = self.Kcb[j] + 0.05
                
                if self.Kcb[j] < 0.15:
                    one_minus_c = 1
                else:
                    one_minus_c = 1 - ((self.Kcb[j] - 0.15) / (self.Kcmax[j] - 0.15)) ** (1 + self.Crop_height[j] * 0.5)
                if one_minus_c < 0.01:
                    one_minus_c = 0.01
                if self.Kcb[j] <= 0.15:
                    one_minus_c = 1
                else:
                    one_minus_c = 1 - ((self.Kcb[j] - 0.15) / (self.Kcmax[j] - 0.15)) ** (1 + self.Crop_height[j] * 0.5)
               
                
                if int(self.Select_Kcb) == 6:
                    if j >= self.dev:
                        one_minus_c = self.ETone_minus_c_daily[j]
                    else:
                        one_minus_c = 1
                Active_depletion = (self.FC[self.Num_layers + 1] - self.WC[j - 1][self.Num_layers + 1]) * self.dz[self.Num_layers + 1] * 1000
                if Active_depletion > self.REW:
                    self.Kr[j] = (self.TEW - Active_depletion) / (self.TEW - self.REW)
                    if self.Kr[j] > 1:
                        self.Kr[j] = 1
                    elif self.Kr[j] < 0:
                        self.Kr[j] = 0
                else:
                    self.Kr[j] = 1
                
                if (self.Kcmax[j] * one_minus_c) < ((self.Kcmax[j] - self.Kcb[j]) * self.Kr[j] * self.Fw[self.Num_layers + 1]):
                    self.Ke[j] = self.Kcmax[j] * one_minus_c
                else:
                    self.Ke[j] = (self.Kcmax[j] - self.Kcb[j]) * self.Kr[j] * self.Fw[self.Num_layers + 1]
            
                       
            else:
                self.Ke[j] = 0
        
            if self.No_stress_reduction == 1:
                self.Ks[j] = 1#
                self.Ks_salt[j] = 1#
            
            self.Ks_salt[j] = 1
            self.ET_trans[j] = self.Kcb[j] * self.Ks[j] * self.Ks_salt[j] * self.ET_0[j]
        
            self.ET_pot[j] = self.Kcb[j] * self.ET_0[j]
            self.E[j] = self.Ke[j] * self.ET_0[j]
            
               
            if self.No_ET == 1:
                self.ET_trans[j] = 0
                self.E[j] = 0
            
            self.ET_actual_cum[j] = self.ET_actual_cum[j - 1] + self.ET_trans[j]
            self.ETcum[j] = self.ETcum[j - 1] + self.ET_pot[j]
            self.ET[j] = self.ET_trans[j] + self.E[j]    
            self.Depletion_total[j] = self.Depletion_total[j - 1] + (self.ET_trans[j] + self.E[j]) / 1000
            self.Percent_depletion_total[j] = self.Depletion_total[j] / self.Total_TAW_Fw[j][BL] * 100
            self.AW[j] = self.TAWsum[j] - self.Depletion_total[j] - self.RAWsum[j]  
            if self.Rainfall_simulation == 1:
                if self.rainfall[j] > 0:
                    if self.Rain_infiltration_calculation == 1:
                        self.Rain_Infilt[j] = 1000 * self.wetting_front(j)
                    else:
                        self.Rain_Infilt[j] = self.rainfall[j] * self.Rain_partition
                else:
                    self.Rain_Infilt[j] = 0
            
            if self.No_infiltration == 1:
                self.Irrigation[j] = 0
                self.Rain_Infilt[j] = 0
            else:
                self.Irrigation[j] = self.Irrigation_depth[j]
        #         Allocate transpiration between layers based on depth of roots and actual depletion
            sum_ET = 0
            for k in range(BL, self.Num_layers + 2):
                sum_ET = sum_ET + self.ET_fractions[int(self.Bottom_layer[j])][k]
        
            if self.No_ET_frac_Adjustment == 1:
                for k in range(1, self.Num_layers + 2):
                    self.Act_frac[j][k] = self.ET_fractions[self.Bottom_layer[j]][k] / sum_ET
            else:
                Sum_act_frac = 0
                
                for k in range(self.Num_layers + 1, BL - 1, -1):
                    self.RAW[k] = self.Ps[j] * self.TAW[k]
                    if self.Fw[k] < self.Fw_y[k]:
                        self.Depletion[j - 1][k] = self.Depletion[j - 1][k] * self.Fw[k] / self.Fw_y[k]
                    if (self.Depletion[j - 1][k] > self.RAW[k] * self.Fw[k]) and (self.Depletion[j - 1][k] < self.TAW[k] * self.Fw[k]):
                        self.Act_frac[j][k] = self.ET_fractions[int(self.Bottom_layer[j])][k] * (self.TAW[k] * self.Fw[k] - self.Depletion[j - 1][k]) / ((self.TAW[k] - self.RAW[k]) * self.Fw[k])/sum_ET
                    elif self.Depletion[j - 1][k] > self.TAW[k] * self.Fw[k]:
                        self.Act_frac[j][k] = 0
                    else:
                        self.Act_frac[j][k] = self.ET_fractions[int(self.Bottom_layer[j])][k]
                    Sum_act_frac = Sum_act_frac + self.Act_frac[j][k]
                
                if Sum_act_frac > 0:
                    for k in range(self.Num_layers + 1, BL - 1, -1):
                        self.Act_frac[j][k] = self.Act_frac[j][k] / Sum_act_frac
        
            te = np.zeros(self.Num_layers + 2)
            kh = np.zeros(self.Num_layers + 2)
            Keff = np.zeros(self.Num_layers + 2)
            
            self.E_wet[j] = self.E[j] * self.Fw[self.Num_layers + 1]
            
               
            self.wet_Rain_Infilt[j] = self.Rain_Infilt[j] * self.Fw[self.Num_layers + 1]
            if self.Water_table_simulation == 1:
                self.Equilibrium_Max[j] = self.Equilibrium_Max[j-1]
            else:
                self.Equilibrium_Max[j] = 0
                
            Equil_Max = int(self.Equilibrium_Max[j])
            self.TDW[j] = 0
            
            Irrigation_drip_layer = np.zeros(14)
            
            Depthcalc = 0
            if self.type_irrigation == "combination":
               
                if self.FW_Type[j] == "drip":
                        Irrigation_surface = 0
                        Irrigation_drip_layer[self.Num_layers] = self.Irrigation[j] * self.Irrigation_partition_one
                        Irrigation_drip_layer[self.Num_layers - 1] = self.Irrigation[j] * self.Irrigation_partition_two
                        Irrigation_drip_layer[self.Num_layers - 2] = self.Irrigation[j] * self.Irrigation_partition_three
                        Irrigation_drip_layer[self.Num_layers - 3] = self.Irrigation[j] * self.Irrigation_partition_four
                        self.Few[j] = 0.5
                elif self.FW_Type[j] == "furrow":
                        Irrigation_surface = self.Irrigation[j]
                        Irrigation_drip_layer[self.Num_layers] = 0
                        Irrigation_drip_layer[self.Num_layers - 1] = 0
                        Irrigation_drip_layer[self.Num_layers - 2] = 0
                        Irrigation_drip_layer[self.Num_layers - 3] = 0
                        self.Few[j] = 1
                elif self.FW_Type[j] == "sprinkler":
                        Irrigation_surface = self.Irrigation[j]
                        Irrigation_drip_layer[self.Num_layers] = 0
                        Irrigation_drip_layer[self.Num_layers - 1] = 0
                        Irrigation_drip_layer[self.Num_layers - 2] = 0
                        Irrigation_drip_layer[self.Num_layers - 3] = 0
                        self.Few[j] = 1
                
            elif self.type_irrigation == "drip":
                Irrigation_surface = 0
                Irrigation_drip_layer[self.Num_layers] = self.Irrigation[j] * self.Irrigation_partition_1
                Irrigation_drip_layer[self.Num_layers - 1] = self.Irrigation[j] * self.Irrigation_partition_2
                Irrigation_drip_layer[self.Num_layers - 2] = self.Irrigation[j] * self.Irrigation_partition_3
                Irrigation_drip_layer[self.Num_layers - 3] = self.Irrigation[j] * self.Irrigation_partition_4
                self.Few[j] = 0.5
            elif self.type_irrigation == "furrow":
                Irrigation_surface = self.Irrigation[j]
                Irrigation_drip_layer[self.Num_layers] = 0
                Irrigation_drip_layer[self.Num_layers - 1] = 0
                Irrigation_drip_layer[self.Num_layers - 2] = 0
                Irrigation_drip_layer[self.Num_layers - 3] = 0
                self.Few[j] = 1
            elif self.type_irrigation == "sprinkler":
                Irrigation_surface = self.Irrigation[j]
                Irrigation_drip_layer[self.Num_layers] = 0
                Irrigation_drip_layer[self.Num_layers - 1] = 0
                Irrigation_drip_layer[self.Num_layers - 2] = 0
                Irrigation_drip_layer[self.Num_layers - 3] = 0
                self.Few[j] = 1
        
            for k in range(self.Num_layers + 1, Equil_Max, -1): # Equil_Max is the upper layer number of the water table. 
                self.Active_WC[k] = self.WC[j - 1][k] # self.Active is the water content ###Probably not needed for irrigation. If not, replace it with self.WC
                
                if k == self.Num_layers + 1:
                    self.WC[j][k] = self.Active_WC[k] + (Irrigation_surface - self.E_wet[j] - self.ET_trans[j] * self.Act_frac[j][k] + self.wet_Rain_Infilt[j]) / self.Fw[k]  / 1000 / self.dz[k]
                else:
                    self.WC[j][k] = self.Active_WC[k] + (Irrigation_drip_layer[k]+self.Infilt[j][k + 1] - self.ET_trans[j] / 1000 * self.Act_frac[j][k]) / self.dz[k] / self.Fw[k]
                    
                #Loop 1, if soil is restricted to field capacity
                
                
                #Loop 1, if soil is restricted to field capacity
                
                if self.WC[j][k] > self.FC[k] and self.Field_capacity_restriction == 1:
                    if k == 1 and self.Seal_bottom == 1:
                        self.Infilt[j][k]=0
                    else:
                        self.Infilt[j][k] = (self.WC[j][k] - self.FC[k]) * self.dz[k] * self.Fw[k]
                        self.WC[j][k] = self.FC[k]
                        
                #Loop 2, if soil is not restricted to field capacity
                        
                elif self.WC[j][k] > self.FC[k]:
                    if self.WC[j][k] >= self.ts[k]:
                        self.Infilt[j][k] = self.Ksat[k]
                        Original_WC_value = self.WC[j][k]
                        self.WC[j][k] = self.WC[j][k] - self.Infilt[j][k] / self.dz[k] / self.Fw[k]
                        if self.WC[j][k] < self.FC[k]:
                            self.WC[j][k] = self.FC[k]
                            self.Infilt[j][k] = (Original_WC_value - self.FC[k])*self.dz[k]*self.Fw[k]
                elif self.Active_WC[k] > self.PWP[k] and k > 1:
                    te[k] = Calculate_te(self.Active_WC[k], self.tr[k], self.ts[k])
                    te[k - 1] = Calculate_te(self.WC[j - 1][k - 1], self.tr[k - 1], self.ts[k - 1])
                    kh[k] = Calculate_k(te[k], self.mv[k], self.Ko[k], self.Lv[k])
                    kh[k - 1] = Calculate_k(te[k - 1], self.mv[k - 1], self.Ko[k - 1], self.Lv[k - 1])
                    Keff1 = (self.dz[k] + self.dz[k - 1]) / (self.dz[k] / kh[k] + self.dz[k - 1] / kh[k - 1])
                    Keff2 = (kh[k] + kh[k - 1]) / 2
                    if te[k] < te[k - 1] or self.WC[j][k] < self.FC[k]:
                        Keff[k] = Keff1
                    else:
                        Keff[k] = Keff2
                    self.hc[j][k] = -((te[k] ** (-1 / self.mv[k]) - 1) ** (1 / self.nv[k])) / self.av[k] / 100
                    self.hc[j][k - 1] = -((te[k - 1] ** (-1 / self.mv[k - 1]) - 1) ** (1 / self.nv[k - 1])) / self.av[k - 1] / 100
                    if k == 1 and self.Seal_bottom == 1:
                        self.Infilt[j][k] = 0
                    else:
                        self.Infilt[j][k] = (self.hc[j][k] - self.hc[j][k - 1] + (self.Zave[k] - self.Zave[k - 1])) / (self.Zave[k] - self.Zave[k - 1]) * Keff[k] * self.Fw[k]
                        self.Infilt[j][k] < self.Infilt[j][k] * 0.5
                        self.WC[j][k] = self.WC[j][k] - self.Infilt[j][k] / self.dz[k] / self.Fw[k]
                else:
                    self.Infilt[j][k] = 0
              
            
                self.Depletion[j][k] = (self.FC[k] - self.WC[j][k]) * self.dz[k] * self.Fw[k]
                self.Percent_depletion[j][k] = (self.FC[k] - self.WC[j][k]) / (self.FC[k] - self.PWP[k]) * 100
                if k == 1:
                    self.WC[j][0] = self.WC[j][1]
                self.TDW[j] = self.TDW[j] + self.WC[j][k]*self.dz[k]
                Depthcalc = Depthcalc + self.dz[k]
            self.VWCave[j] = self.TDW[j] / Depthcalc
                    
            if self.Neglect_upper_layer_in_depletion_calc == 1:
                self.Percent_depletion_total[j] = (self.Depletion_total[j] - (self.FC[self.Num_layers + 1] - self.WC[j][self.Num_layers + 1]) * self.dz[self.Num_layers + 1] * self.FW_layers[j - 1][self.Num_layers + 1]) / (self.Total_TAW_Fw[j][BL] - self.TAW[self.Num_layers + 1] * self.Fw[self.Num_layers + 1]) * 100
        
            if self.Salinity_simulation == 1:
                Check = 1
                for k in range(self.Num_layers + 1, 0, -1):
                    self.Active_EC[k] = self.EC[j - 1][k]
        
                for k in range(self.Num_layers + 1, 0, -1):
                 
                #Calculate salinity addition by wastewater or manure
                
                    if k == self.Num_layers + 1:
                        mwaste = 0.5 * self.Waste_sal[j] / 10 / 640
                    elif k == self.Num_layers:
                        mwaste = 0.5 * self.Waste_sal[j] / 10 / 640
                    else:
                        mwaste = 0
                        
                    self.Total_Rain_plus_irrigation[j] = self.Irrigation[j] + self.wet_Rain_Infilt[j]
                    
                    if k == self.Num_layers + 1:
                        if (self.Irrigation[j] + self.wet_Rain_Infilt[j]) / 1000 / self.Fw[k] > (self.FC[k] - self.Active_WC[k]) * self.dz[k]:
                            self.EC[j][k] = (self.Irrigation[j] / 1000 / self.Fw[k] * self.Irr_Sal[j] + mwaste + self.Active_EC[k] * self.dz[k] * self.Active_WC[k]) / ((self.Irrigation[j] + self.wet_Rain_Infilt[j]) / 1000 / self.Fw[k] + self.dz[k] * self.Active_WC[k] - (self.E_wet[j] + self.ET_trans[j] * self.Act_frac[j][k]) / self.Fw[k] / 1000)
                            self.Active_EC[k] = self.EC[j][k]
                            Check = 1
                        elif self.Infilt[j][k] < 0:
                            self.EC[j][k] = (-self.Infilt[j][k] / self.Fw[k] * self.Active_EC[self.Num_layers] + mwaste + self.Active_EC[k] * self.dz[k] * self.Active_WC[k]) / (self.dz[k] * self.WC[j][k])
                            Check = 0
                        else:
                            self.EC[j][k] = (self.Irrigation[j] / 1000 / self.Fw[k] * self.Irr_Sal[j] + mwaste - self.Infilt[j][k] * self.Active_EC[k] / self.Fw[k] + self.Active_EC[k] * self.dz[k] * self.Active_WC[k]) / (self.dz[k] * self.WC[j][k])
                            Check = 0
                        
                        self.ECe[j][k] = self.EC[j][k] * self.WC[j][k] / self.ts[k]
                    else:
                        if Check == 1 and self.Infilt[j][k] > 0:
                            self.EC[j][k] = (self.Infilt[j - 1][k] / self.Fw[k] * self.Active_EC[k + 1] + mwaste + self.Active_EC[k] * self.dz[k] * self.Active_WC[k]) / (self.Infilt[j - 1][k] / self.Fw[k] + self.dz[k] * self.Active_WC[k] - self.ET_trans_wet[j] * self.Act_frac[j][k] / self.Fw[k] / 1000)
                            self.Active_EC[k] = self.EC[j][k]
                            Check = 1
                            if k == 1:
                                self.EC_leach_eqn[j] = 1
                        elif self.Infilt[j - 1][k] <= 0 and self.Infilt[j][k] > 0:
                            self.EC[j][k] = (self.Infilt[j - 1][k] * self.Active_EC[k] / self.Fw[k] + mwaste - self.Infilt[j][k] * self.Active_EC[k] / self.Fw[k] + self.Active_EC[k] * self.dz[k] * self.WC[j - 1][k]) / (self.dz[k] * self.WC[j][k])
                        elif self.Infilt[j - 1][k] <= 0 and self.Infilt[j][k] <= 0:
                            self.EC[j][k] = (self.Infilt[j - 1][k] * self.Active_EC[k] / self.Fw[k] + mwaste - self.Infilt[j][k] * self.Active_EC[k - 1] / self.Fw[k] + self.Active_EC[k] * self.dz[k] * self.WC[j - 1][k]) / (self.dz[k] * self.WC[j][k])
                        elif self.Infilt[j - 1][k] > 0 and self.Infilt[j][k] <= 0:
                            self.EC[j][k] = (self.Infilt[j - 1][k] * self.Active_EC[k + 1] / self.Fw[k] + mwaste - self.Infilt[j][k] * self.Active_EC[k - 1] / self.Fw[k] + self.Active_EC[k] * self.dz[k] * self.WC[j - 1][k]) / (self.dz[k] * self.WC[j][k])
                        else:
                            self.EC[j][k] = (self.Infilt[j - 1][k] * self.Active_EC[k + 1] / self.Fw[k] + mwaste - self.Infilt[j][k] * self.Active_EC[k] / self.Fw[k] + self.Active_EC[k] * self.dz[k] * self.WC[j - 1][k]) / (self.dz[k] * self.WC[j][k])
        
                        if self.EC[j][k] > self.Max_S:
                            self.EC[j][k] = self.Max_S
                        self.ECe[j][k] = self.EC[j][k] * self.WC[j][k] / self.ts[k]    
                        Act_frac_sum = 0
                        self.Total_salt[j] = 0
                        for k in range(self.Num_layers, BL - 1, -1):
                            self.ECe_ave_effective[j] = self.ECe_ave_effective[j] + self.Act_frac[j][k] * self.ECe[j][k] * self.FC[k] / self.WC[j][k]
                            Act_frac_sum = Act_frac_sum + self.Act_frac[j][k]
                        if Act_frac_sum == 0: 
                            Act_frac_sum = 1
                        self.ECe_ave_effective[j] = self.ECe_ave_effective[j] / Act_frac_sum
                        for k in range(1, self.Num_layers + 2):
                            self.Total_salt[j] = self.Total_salt[j] + self.EC[j][k] * 640 * self.WC[j][k] * self.dz[k] * self.Fw[k]
                        self.EC[j][0] = self.EC[j][1]
                    
            if int(self.Nitrogen_simulation) == 1:
                
                Weighted_N = np.zeros(self.Num_layers + 2)
                
                self.Total_nit[j - 1] = 0
                for k in range(1, self.Num_layers + 2):
                    self.Total_nit[j - 1] = self.Total_nit[j - 1] + self.N[j - 1][k] * self.WC[j - 1][k] * self.dz[k] * self.Fw[k]
                for k in range(1, self.Num_layers + 2):
                    self.Active_n[k] = (self.WC[j - 1][k] * self.N[j - 1][k]) / self.WC[j - 1][k]
            
                self.Total_Min[j] = 0
                self.Total_Den[j] = 0
                self.Total_Fer[j] = 0
                self.Total_Upt[j] = 0
                self.Total_nit_accum[j] = 0
                self.Total_nit[j] = 0
        
                self.Total_N = 0
                
                N_total_weight = 0
                Total_weighting = 0
                self.Frac_total_weight = 0
                self.Total_frac_weighting = 0
                
                for k in range(BL, self.Num_layers + 2):
                    if self.WC[j][k] > self.PWP[k]:
                        Weighted_N[k] = self.N_soil[j - 1][k] * self.Act_frac[j][k]
                        N_total_weight = Weighted_N[k] + N_total_weight
                        Total_weighting = Total_weighting + self.Act_frac[j][k]
                    else:
                        Weighted_N[k] = 0
                
                if Total_weighting == 0:
                    Total_weighting = 1
                self.N_ave[j] = N_total_weight / Total_weighting
                
                average_Fw = (self.Fw[self.Num_layers] + self.Fw[self.Num_layers + 1]) / 2
                
                mupt_optimal = self.N_upt[j] / 10 * self.Frac_NO3 * average_Fw #'Adjusts uptake for units and fraction taken up as nitrate from soil
                
                self.N_max[j] = mupt_optimal * (1 + self.Frac_greater_saturation)
                
        #'Calculate Km for Michaelis-Menton, this could be specified in worksheet
        
                if self.Constant_Km == 1:
                    Km = 1 #self.Km_daily[j]
                elif self.Constant_Km == 2:
                    if self.N_upt[j] > 0:
                        Km = (self.N_soil_optimal - self.Nmin) * (self.N_max[j] / mupt_optimal - 1)
                    else:
                        Km = 100000
                else:
                    Km = self.Km
                
                self.mupt_entire_profile[j] = self.N_max[j] * (self.N_ave[j] - self.Nmin) / (Km + self.N_ave[j] - self.Nmin)
                
                self.N_optimal_low[j] = mupt_optimal * (1 - self.Range_frac / 2)
                self.N_optimal_high[j] = mupt_optimal * (1 + self.Range_frac / 2)
                
                if self.mupt_entire_profile[j] > 0:
                    if self.mupt_entire_profile[j] < self.N_optimal_low[j]:
                        self.Ks_nit[j] = 1 - self.KN_low[j] * (self.N_optimal_low[j] - self.mupt_entire_profile[j]) / self.N_optimal_low[j]
                    elif self.mupt_entire_profile[j] < self.N_optimal_high[j]:
                        self.Ks_nit[j] = 1
                    else:
                        self.Ks_nit[j] = 1 - self.KN_high[j] * (self.mupt_entire_profile[j] - self.N_optimal_high[j]) / self.N_optimal_high[j]
                else:
                    self.Ks_nit[j] = 1#
                
                if self.Ks_nit[j] < 0:
                    self.Ks_nit[j] = 0
                 
                Weighted_N_ET = 0
                
                for k in range(BL, self.Num_layers + 2):
                    if self.WC[j][k] > self.PWP[k]:
                        Weighted_N_ET = Weighted_N_ET + self.ET_fractions[j][k] * self.N_soil[j - 1][k]
                
                for k in range(self.Num_layers + 1, 0, -1):
        
                    if (k > BL - 1) and (self.WC[j][k] > self.PWP[k]):
                        mupt = self.mupt_entire_profile[j] * self.ET_fractions[j][k] * self.N_soil[j - 1][k] / Weighted_N_ET
                    else:
                        mupt = 0
                    self.Uptake[j][k] = mupt
        
        #'Calculate mineralization rate
        
                    if self.WC[j - 1][k] < self.PWP[k]:
                        fmnq = 0
                    elif self.WC[j - 1][k] < self.qlow:
                        fmnq = (self.WC[j - 1][k] - self.PWP[k]) / (self.qlow - self.PWP[k])
                    elif self.WC[j - 1][k] < self.qhigh:
                        fmnq = 1
                    else:
                        fmnq = 0.6 + 0.4 * (self.ts[k] - self.WC[j - 1][k]) / (self.ts[k] - self.qhigh)
                    
                    Gmn = self.Kmnl * self.fmntemp[j][k] * fmnq * self.bd[k] * self.Org[k]
                    
                    mMin = Gmn * self.dz[k] * self.FW_layers[j - 1][k]
                    
        #'Calculate denitrification rate
        
                    if self.WC[j - 1][k] < 0.6 * self.ts[k]:
                        fdenq = 0
                    else:
                        fdenq = ((self.WC[j - 1][k] - 0.6 * self.ts[k]) / (self.ts[k] - 0.6 * self.ts[k])) ** 2
                    
                    Gden = self.Kden * self.fmntemp[j][k] * fdenq * self.N[j - 1][k] * self.WC[j - 1][k] * np.exp(-self.alpha * self.Z_top_ave[k] * 100)
                    
                    mDen = Gden * self.dz[k] * self.FW_layers[j - 1][k]
                    
        #'Calculate fertilizer addition
        
                    if k == self.Num_layers + 1:
                        if self.Dont_fertilize_evap_layer == 1:
                            mfer = 0
                        else:
                            mfer = 0.5 * self.Fert[j] / 10
                    elif k == self.Num_layers:
                        if self.Dont_fertilize_evap_layer == 1:
                            mfer = self.Fert[j] / 10
                        else:
                            mfer = 0.5 * self.Fert[j] / 10
                    else:
                        mfer = 0
                    
        #'Make calculation of nitrogen concentrations
                    
                    if k == self.Num_layers + 1:
                            if (self.Irrigation[j] + self.wet_Rain_Infilt[j]) / 1000 / self.Fw[k] > (self.FC[k] - self.Active_WC[k]) * self.dz[k]:
                                self.N[j][k] = (self.Irrigation[j] / 1000 / self.Fw[k] * self.Irr_Nit[j] + mMin - mDen + mfer - mupt / self.Fw[k] + self.Active_n[k] * self.dz[k]* self.Active_WC[k]) / ((self.Irrigation[j] + self.wet_Rain_Infilt[j]) / 1000 / self.Fw[k] + self.dz[k] * self.Active_WC[k] - (self.E_wet[j] + self.ET_trans_wet[j] * self.Act_frac[j][k]) / self.Fw[k] / 1000)
                                self.Active_n[k] = self.N[j][k]
                                Check = 1
                            elif self.Infilt[j][k] < 0:
                                self.N[j][k] = (-self.Infilt[j][k] / self.Fw[k] * self.Active_n[self.Num_layers] + mMin - mDen + mfer - mupt / self.Fw[k] + self.Active_n[k] * self.dz[k] * self.Active_WC[k]) / (self.dz[k] * self.WC[j][k])
                                Check = 0
                            else:
                                self.N[j][k] = (self.Irrigation[j] / 1000 / self.Fw[k] * self.Irr_Nit[j] + mMin - mDen + mfer - mupt / self.Fw[k] - self.Infilt[j][k] * self.Active_n[k] / self.Fw[k] + self.Active_n[k] * self.dz[k] * self.Active_WC[k]) / (self.dz[k] * self.WC[j][k])
                                Check = 0
                            
                    else:
                            if Check == 1 and self.Infilt[j][k] > 0:
                                self.N[j][k] = (self.Infilt[j][k + 1] / self.Fw[k] * self.Active_n[k + 1] + mMin - mDen + mfer - mupt / self.Fw[k] + self.Active_n[k] * self.dz[k] * self.Active_WC[k]) / (self.Infilt[j][k + 1] / self.Fw[k] + self.dz[k] * self.Active_WC[k] - self.ET_trans_wet[j] * self.Act_frac[j][k] / self.Fw[k] / 1000)
                                Check = 1
                                self.Active_n[k] = self.N[j][k]
                                if k == 1:
                                    self.N_leach_eqn[j] = 1
                            elif self.Infilt[j][k + 1] <= 0 and self.Infilt[j][k] > 0:
                                self.N[j][k] = (self.Infilt[j][k + 1] * self.Active_n[k] / self.Fw[k] + mMin - mDen + mfer - mupt / self.Fw[k] - self.Infilt[j][k] * self.Active_n[k] / self.Fw[k] + self.Active_n[k] * self.dz[k] * self.WC[j - 1][k]) / (self.dz[k] * self.WC[j][k])
                            elif self.Infilt[j][k + 1] <= 0 and self.Infilt[j][k] <= 0:
                                self.N[j][k] = (self.Infilt[j][k + 1] * self.Active_n[k] / self.Fw[k] + mMin - mDen + mfer - mupt / self.Fw[k] - self.Infilt[j][k] * self.Active_n[k - 1] / self.Fw[k] + self.Active_n[k] * self.dz[k] * self.WC[j - 1][k]) / (self.dz[k] * self.WC[j][k])
                            elif self.Infilt[j][k + 1] > 0 and self.Infilt[j][k] <= 0:
                                self.N[j][k] = (self.Infilt[j][k + 1] * self.Active_n[k + 1] / self.Fw[k] + mMin - mDen + mfer - mupt / self.Fw[k] - self.Infilt[j][k] * self.Active_n[k - 1] / self.Fw[k] + self.Active_n[k] * self.dz[k] * self.WC[j - 1][k]) / (self.dz[k] * self.WC[j][k])
                            else:
                                self.N[j][k] = (self.Infilt[j][k + 1] * self.Active_n[k + 1] / self.Fw[k] + mMin - mDen + mfer - mupt / self.Fw[k] - self.Infilt[j][k] * self.Active_n[k] / self.Fw[k] + self.Active_n[k] * self.dz[k] * self.WC[j - 1][k]) / (self.dz[k] * self.WC[j][k])
                    self.N_soil[j][k] = self.N[j][k] * self.WC[j][k] / ((1 - self.ts[k]) * 2.65)
                    self.kgha[j][k] = self.N_soil[j][k] * (1 - self.ts[k]) * 2.65 * self.dz[k] * 10
                    self.Total_Min[j] = mMin * self.Fw[k] + self.Total_Min[j]
                    self.Total_Den[j] = mDen * self.Fw[k] + self.Total_Den[j]
                    self.Total_Fer[j] = mfer * self.Fw[k] + self.Total_Fer[j]
                    self.Total_Upt[j] = mupt * self.Fw[k] + self.Total_Upt[j]
                    self.Net_accumulation[j][k] = (mMin - mDen + mfer - mupt)
        
                self.Cum_Min[j] = self.Cum_Min[j - 1] + self.Total_Min[j] * 10
                self.Cum_Den[j] = self.Cum_Den[j - 1] - self.Total_Den[j] * 10
                self.Cum_Fer[j] = self.Cum_Fer[j - 1] + self.Total_Fer[j] * 10
                self.Cum_Upt[j] = self.Cum_Upt[j - 1] - self.Total_Upt[j] * 10
                self.Cum_Drain[j] = self.Cum_Drain[j - 1] - self.Infilt[j][1] * self.N[j][1] * 10
                self.Cum_Irr[j] = self.Cum_Irr[j - 1] + self.Irrigation[j] / 1000 * self.Irr_Nit[j] * 10
                self.Cum_Total[j] = self.Cum_Min[j] + self.Cum_Den[j] + self.Cum_Fer[j] + self.Cum_Upt[j] + self.Cum_Drain[j] + self.Cum_Irr[j]
                for k in range(1, self.Num_layers + 2):
                    self.Total_nit_accum[j] = self.Total_nit_accum[j] + self.Net_accumulation[j][k]
                    self.Total_nit[j] = self.Total_nit[j] + self.N[j][k] * self.WC[j][k] * self.dz[k] * self.Fw[k]
                self.N[j][0] = self.N[j][1]
                
        temp_output = pd.DataFrame(columns = ['Days_after_planting', 'DOY', 'pid', 'plantname', 'NDVI', 'NDVI_regression', 'Kcb_NDVI', 'Kcb_calculated', 'Kcb_used',
                                              'one_minus_c', 'Crop_height', 'Root_depth', 'Ke', 'Evap', 'Transpiration', 'ET', 'Pottranspiration', 'CumulativePotentialET',
                                              'CumulativeactualET', 'ReferenceET', 'Ky', 'Depletion_total', 'Percent_depletion_total', 'Irrigation', 'P', 'Rainfall', 'Rain_infilt',
                                              'Field_capacity_ave', 'Permanent_wilting_point_ave', 'TAWsum', 'RAWsum', 'Available_water', 'Available_water_depth_ave', 'Volumetric_water_content_ave', 'Total_depth_water',
                                              'Watertableelevation', 'HeightEqu', 'NumberEqu', 'WaterstressKs', 'IrrigationSaltAdded', 'WasteSaltAdded', 'SeepageSaltLost', 'SumOfFluxes', 
                                              'TotalSalt', 'DifferenceInSalt', 'SaltStress', 'NitStress', 'TotalIrrN', 'TotalDrainN', 'SumReactionsN', 'SumFluxReactionsN', 'TotalMin',
                                              'TotalDen', 'TotalFer', 'TotalUpt', 'UptakeReq', 'TotalNit', 'TotalNitAccum', 'NitAve', 'NOptimalLow', 'NOptimalHigh', 'CumMin', 'CumDen', 
                                              'CumFer', 'CumUpt', 'CumIrrN', 'CumDrnN', 'CumChangeN'])                 
        
        temp_Excel_output_to_sheets = pd.DataFrame(columns = ['DAP', 'Date', 'Planting_year', 'PlantingNum','Planting_name', 'Field_name', 'Account_name', 
                                                    'Crop_name', 'Crop_height', 'FEW', 'KcbUsed', 'Ke', 'Evap',	
                                                    'Transpiration', 'ET', 'PotTranspiration', 'CumulativePotentialET',	
                                                    'CumulativeActualET','ReferenceET','oneminusC', 'blank1', 'DOY','WC L1',
                                                    'WC L2', 'WC L3', 'WC L4', 'WC L5', 'WC L6', 'WC L7', 'WC L8', 'WC L9', 'WC L10', 'WC L11', 
                                                    'WC L12', 'WC L13', 'blank3', 'Dep L1', 'Dep L2', 'Dep L3', 'Dep L4', 'Dep L5', 'Dep L6',
                                                    'Dep L7', 'Dep L8', 'Dep L9', 'Dep L10', 'Dep L11', 'Dep L12', 'Dep L13', 'blank4',
                                                    'AF L1', 'AF L2', 'AF L3', 'AF L4', 'AF L5', 'AF L6', 'AF L7', 'AF L8', 'AF L9', 
                                                    'AF L10', 'AF L11', 'AF L12', 'AF L13', 'blank5', 'Inf L1', 'Inf L2', 'Inf L3',
                                                    'Inf L4', 'Inf L5', 'Inf L6', 'Inf L7', 'Inf L8', 'Inf L9', 'Inf L10', 'Inf L11',
                                                    'Inf L12', 'Inf L13', 'blank6', 'Pdep L1', 'Pdep L2', 'Pdep L3', 'Pdep L4',
                                                    'Pdep L5', 'Pdep L6', 'Pdep L7', 'Pdep L8', 'Pdep L9', 'Pdep L10', 'Pdep L11',
                                                    'Pdep L12', 'Pdep L13', 'blank7', 'blank8', 'blank9', 'blank10', 'blank11', 'zwt', 'EqMax', 'EqMaxNumber',
                                                    'IrrigationPlusRain', 'Leaching','DepthDifference', 'ET_neg',
                                                    'SumSourcesSinks', 'blank12', 'Root', 'AllowableDepletion', 'ActualDepletion', 'PercentDepletion',
                                                    'IrrigationDepth', 'MAD_fraction', 'Rain'])              

        a = self.StartDate
        a=a.replace('-','') 
        Year=int(a[0:4])
        month=int(a[4:6])
        day=int(a[6:8])
        mydate=datetime.date(Year,month,day)
        print(mydate)
        numdays = self.NumDaysInc - 2
        dateList = []
        for x in range (0, numdays):
             dateList.append(mydate + datetime.timedelta(days = x))
        DAP =  int(self.StartDOY - self.PlantingDOY - 1)
        DAPlist=[]
        planting_number = []
        planting_year = []
        planting_name = []
        field_name = []
        account_name = []
        crop_name = []
        for x in list (range(numdays)):
            DAPlist.append(DAP+x)
            planting_year.append(self.PlantingYear)
            planting_number.append(self.PlantingNum)
            planting_name.append(self.PlantingName)
            field_name.append(self.FieldNameP)
            account_name.append(self.AccountNameP)
            crop_name.append(self.CropName)
        temp_Excel_output_to_sheets['DAP']=DAPlist
        temp_Excel_output_to_sheets['Date']=dateList
        temp_Excel_output_to_sheets['Planting_year']=planting_year
        temp_Excel_output_to_sheets['PlantingNum']=planting_number
        temp_Excel_output_to_sheets['Planting_name'] = planting_name
        temp_Excel_output_to_sheets['Field_name'] = field_name
        temp_Excel_output_to_sheets['Account_name'] = account_name
        temp_Excel_output_to_sheets['Crop_name'] = crop_name
        temp_Excel_output_to_sheets['Crop_height'] = self.Crop_height[1:self.NumDaysInc - 1]
        temp_Excel_output_to_sheets['Root'] = self.Root[1:self.NumDaysInc - 1]
        temp_Excel_output_to_sheets['blank1'] = np.zeros(self.NumDaysInc-2)
        temp_Excel_output_to_sheets['FEW'] = self.Crop_height[1:self.NumDaysInc - 1]
        temp_Excel_output_to_sheets['KcbUsed'] = self.Kcb[1:self.NumDaysInc - 1]
        temp_Excel_output_to_sheets['Ke'] = self.Ke[1:self.NumDaysInc - 1]
        temp_Excel_output_to_sheets['Evap'] = self.E[1:self.NumDaysInc - 1]
        temp_Excel_output_to_sheets['Transpiration'] = self.ET_trans[1:self.NumDaysInc - 1]
        temp_Excel_output_to_sheets['ET'] = self.ET[1:self.NumDaysInc - 1]
        temp_Excel_output_to_sheets['PotTranspiration'] = self.ET_pot[1:self.NumDaysInc - 1]
        temp_Excel_output_to_sheets['CumulativePotentialET'] = self.ETcum[1:self.NumDaysInc - 1]
        temp_Excel_output_to_sheets['CumulativeActualET'] = self.ETcum[1:self.NumDaysInc - 1]
        temp_Excel_output_to_sheets['ReferenceET'] = self.ET_0[1:self.NumDaysInc - 1]
        temp_Excel_output_to_sheets['oneminusC'] = self.Ky[1:self.NumDaysInc - 1]
        temp_Excel_output_to_sheets['DOY'] = self.DOY[1:self.NumDaysInc - 1]
        for k in range(1,13):
            layer_name = 'WC L' + str(k)
            if k <= self.Num_layers + 1:
                a = np.zeros(self.NumDaysInc - 2)
                for i in range(0, self.NumDaysInc - 2):
                    a[i] = self.WC[i][k]
                temp_Excel_output_to_sheets[layer_name] = a
            else:
                temp_Excel_output_to_sheets[layer_name] = np.zeros(self.NumDaysInc - 2)
        temp_Excel_output_to_sheets['blank3'] = np.zeros(self.NumDaysInc-2)
        for k in range(1,13):
            layer_name = 'Dep L' + str(k)
            if k <= self.Num_layers + 1:
                a = np.zeros(self.NumDaysInc - 2)
                for i in range(0, self.NumDaysInc - 2):
                    a[i] = self.Depletion[i][k]
                temp_Excel_output_to_sheets[layer_name] = a
            else:
                temp_Excel_output_to_sheets[layer_name] = np.zeros(self.NumDaysInc - 2)

        temp_Excel_output_to_sheets['blank4'] = np.zeros(self.NumDaysInc-2)
        for k in range(1,13):
            layer_name = 'AF L' + str(k)
            if k <= self.Num_layers + 1:
                a = np.zeros(self.NumDaysInc - 2)
                for i in range(0, self.NumDaysInc - 2):
                    a[i] = self.Act_frac[i][k]
                temp_Excel_output_to_sheets[layer_name] = a
            else:
                temp_Excel_output_to_sheets[layer_name] = np.zeros(self.NumDaysInc - 2)
        temp_Excel_output_to_sheets['blank5'] = np.zeros(self.NumDaysInc-2)
        for k in range(1,13):
            layer_name = 'Inf L' + str(k)
            if k <= self.Num_layers + 1:
                a = np.zeros(self.NumDaysInc - 2)
                for i in range(0, self.NumDaysInc - 2):
                    a[i] = self.Infilt[i][k]
                temp_Excel_output_to_sheets[layer_name] = a
            else:
                temp_Excel_output_to_sheets[layer_name] = np.zeros(self.NumDaysInc - 2)
        temp_Excel_output_to_sheets['blank6'] = np.zeros(self.NumDaysInc-2)
        for k in range(1,13):
            layer_name = 'Pdep L' + str(k)
            if k <= self.Num_layers + 1:
                a = np.zeros(self.NumDaysInc - 2)
                for i in range(0, self.NumDaysInc - 2):
                    a[i] = self.Percent_depletion[i][k]
                temp_Excel_output_to_sheets[layer_name] = a
            else:
                temp_Excel_output_to_sheets[layer_name] = np.zeros(self.NumDaysInc - 2)
        temp_Excel_output_to_sheets['blank7'] = np.zeros(self.NumDaysInc-2)        
        temp_Excel_output_to_sheets['blank8'] = np.zeros(self.NumDaysInc-2)        
        temp_Excel_output_to_sheets['blank9'] = np.zeros(self.NumDaysInc-2)        
        temp_Excel_output_to_sheets['blank10'] = np.zeros(self.NumDaysInc-2)        
        temp_Excel_output_to_sheets['blank11'] = np.zeros(self.NumDaysInc-2)        
        temp_Excel_output_to_sheets['zwt'] = self.Equilibrium_Max[1:self.NumDaysInc - 1]
        temp_Excel_output_to_sheets['EqMax'] = self.zu_Eq_Max[1:self.NumDaysInc - 1]
        temp_Excel_output_to_sheets['EqMaxNumber'] = self.Irrigation[1:self.NumDaysInc - 1]
        for i in range(1,self.NumDaysInc - 1):
            self.Irrigation_plus_rain[i] = self.Irrigation[i] + self.Rain_Infilt[i]
        temp_Excel_output_to_sheets['IrrigationPlusRain'] = self.Irrigation_plus_rain[1:self.NumDaysInc - 1]
        for i in range(0, self.NumDaysInc - 2):
            a[i] = self.Infilt[i][1]
        temp_Excel_output_to_sheets['Leaching'] = a
        for i in range(1,self.NumDaysInc - 1):
            for k in range(1, self.Num_layers + 2):
                self.Sum_depths[i] = self.Sum_depths[i] + self.WC[i][k] * self.dz[k] * self.Fw[k]
            self.Difference[i] = 1000*(self.Sum_depths[i] - self.Sum_depths[i-1])
        temp_Excel_output_to_sheets['DepthDifference'] = self.Difference[1:self.NumDaysInc - 1]
        for i in range(1,self.NumDaysInc - 1):
            self.ET_total[i] = -(self.ET_trans[i] + self.E_wet[i])
        temp_Excel_output_to_sheets['ET_neg'] = self.ET_total[1:self.NumDaysInc - 1]
        for i in range(1,self.NumDaysInc - 1):
            self.Sum_sources_and_sinks[i] = self.ET_trans[i] - self.Infilt[i][1] * 1000 + self.Irrigation[i] + self.Rain_Infilt[i]
        temp_Excel_output_to_sheets['SumSourcesSinks'] = self.Sum_sources_and_sinks[1:self.NumDaysInc - 1]
        temp_Excel_output_to_sheets['blank12'] = np.zeros(self.NumDaysInc-2)        
        temp_Excel_output_to_sheets['Root'] = self.Root[1:self.NumDaysInc - 1]
        temp_Excel_output_to_sheets['AllowableDepletion'] = self.Allowable_depletion_total[1:self.NumDaysInc - 1]*1000
        temp_Excel_output_to_sheets['ActualDepletion'] = self.Depletion_total[1:self.NumDaysInc - 1]*1000
        temp_Excel_output_to_sheets['PercentDepletion'] = self.Percent_depletion_total[1:self.NumDaysInc - 1]
        temp_Excel_output_to_sheets['IrrigationDepth'] = self.Irrigation[1:self.NumDaysInc - 1]
        temp_Excel_output_to_sheets['MAD_fraction'] = self.Ps[1:self.NumDaysInc - 1]
        temp_Excel_output_to_sheets['Rain'] = self.wet_Rain_Infilt[1:self.NumDaysInc - 1]
        
        
#        writer = pd.ExcelWriter('WINDS_database_format6.xlsx')
        #temp_Excel_output_to_sheets.to_excel(writer, 'Output' + str(self.PlantingNum))
#        writer.save()
        
        # db=create_engine('mysql://UofABEWINDS:WINDSAWSPort2020@windsdatabase-1.cdzagwevzppe.us-west-1.rds.amazonaws.com:3306/winds_test')
        temp_Excel_output_to_sheets.replace([np.inf, -np.inf], np.nan, inplace=True)
        temp_Excel_output_to_sheets.to_sql('Output_V2', con=db, if_exists='append', index = 0)
        
        plt.figure(1)
        plt.plot(self.WC)
        plt.ylabel('ml/m')
        plt.xlabel('DOY')
        plt.show()    

    def wetting_front(self, j):
        m = np.zeros(self.Num_layers + 2) 
        Depth = np.zeros(self.Num_layers + 2)
        k = np.zeros(self.Num_layers + 2)
        z = np.zeros(self.Num_layers + 2)
        SAV = np.zeros(self.Num_layers + 2)
        Precip_rate = self.rainfall[j] / self.Rain_time[j] / 1000
        for i in range(1, self.Num_layers + 1):
            SAV[i] = self.SAV
            m[i] = self.ts[self.Num_layers + 1 - i] - self.WC[j][self.Num_layers + 1 - i]
            k[i] = self.Ksat[self.Num_layers + 1 - i] / 24
            z[i] = self.dz[self.Num_layers + 1 - i]
        
        Depth[0] = 0
        Capacity = 0
        Lf_prev = 0
        
        for i in range(1, self.Num_layers + 1):
            Depth[i] = Depth[i - 1] + z[i]
            Capacity = Capacity + z[i] * m[i]
        
        i = 1
        if m[i] < 0.01:
            while m[i] < 0.02 and i < self.Num_layers:
                i = i + 1
                Lf_prev = Depth[i]
        
        if Capacity > 0 and i < self.Num_layers:
            continuecalcs = 1
        else:
            continuecalcs = 0
            Total_Infiltration = Capacity
        
        total_time = 0
        Total_Infiltration = 0
        dt = self.Rain_time[j] / 100
        if Lf_prev > 0:
            LF = Lf_prev
        elif self.PondedDepth > 0:
            LF = 0.02
            Total_Infiltration = LF * m[1]
        else:
            LF = Precip_rate * dt / m[1]
            Total_Infiltration = LF * m[1]
        
        i = 1
        while Depth[i] < LF:
            i = i + 1
    
        j = i
        total_time = dt
        
        while total_time < self.Rain_time[j] and continuecalcs == 1 and j < self.Num_layers:
            total_time = total_time + dt
            Sum_denominator = 0
            for i in range(1, j+1):
                if i == j:
                    Sum_denominator = Sum_denominator + (LF - Depth[i - 1]) / k[i]
                else:
                    Sum_denominator = Sum_denominator + z[i] / k[i]
            Keff = LF / Sum_denominator
            Infiltration_rate = Keff * ((self.PondedDepth + self.SAV + LF) / LF)
            if Precip_rate < Infiltration_rate and self.PondedDepth > 0:
                Infiltration = Precip_rate * dt
            else:
                Infiltration = Infiltration_rate * dt
    
            Total_Infiltration = Total_Infiltration + Infiltration
            while (m[j] == 0 & continuecalcs == 1):
                j = j + 1
                LF = LF + z[j - 1]
                if j == self.Num_layers:
                    continuecalcs = 0
                    Total_Infiltration = Capacity
            if continuecalcs == 1:
                LF = LF + Infiltration / m[j]
                if LF > Depth[self.Num_layers]:
                    continuecalcs = 0
                    Total_Infiltration = Capacity
                else:
                    i = 1
                    while Depth[i] < LF:
                        i = i + 1
                    j = i
                    
            if self.Rain_Infilt[j] > self.rainfall[j]:
                self.Rain_Infilt[j] = self.rainfall[j]
            
        return Total_Infiltration;
        
    def parameterize_drainage(self, j):
        if j == 1:
            self.zwt[j - 1] = self.Init_zwt
            self.Equilibrium_Max[j - 1] = self.Equil_max_init
        
        self.ts_depth[0] = 0
        for i in range(1, self.Num_layers + 1):
            ts_depth[i] = ts_depth(i - 1) + self.ts[i] * self.dz[i]
            for ij in range(0, 101):
                self.zwt_test[i][ij] = ij * (self.zu[i]) / 100
                self.WC_test[i][ij] = 0
                for k in range(1, i + 1):
                    if self.zwt_test[i][ij] > self.zu[k]: #Water table is above cell
                        self.WC_test[i][ij] = self.ts[k] * self.dz[k] + self.WC_test[i][ij]
                    elif self.zu[k] > self.zwt_test[i][ij] and self.zl[k] < self.zwt_test[i][ij]:   #Water table is within cell
                        self.WC_test[i][ij] = d_cell_WT(self.ts[k], self.tr[k], self.zu[k], self.zl[k], self.zwt_test[i][ij], self.av[k], nv[k]) + self.WC_test[i][ij]
                    elif self.zu[k] == self.zwt_test[i][ij]: #Water table is at top of cell
                        self.WC_test[i][ij] = self.ts[k] * self.dz[k] + self.WC_test[i][ij]
                    else:    #Water table is below cell or at lower boundary of cell
                        self.WC_test[i][ij] = d_cell_Eq(self.ts[k], self.tr[k], self.zu[k], self.zl[k], self.zwt_test[i][ij], self.av[k], nv[k]) + self.WC_test[i][ij]
        
        
    def find_water_table_depths(self, j):    
        self.Sum_WC_depth[j - 1][0] = 0
        
        for k in range(1, self.Num_layers + 2):
            if zwt[j - 1] > self.zu[k]:
                self.WC[j - 1][k] = self.ts[k]
            elif self.zu[k] > zwt[j - 1] and self.zl[k] < zwt[j - 1]:
                self.WC[j - 1][k] = d_cell_WT(self.ts[k], self.tr[k], self.zu[k], self.zl[k], zwt[j - 1], self.av[k], nv[k]) / self.dz[k]
            elif self.zu[k] == zwt[j - 1]:
                self.WC[j - 1][k] = self.ts[k]
            else:
                self.WC[j - 1][k] = d_cell_Eq(self.ts[k], self.tr[k], self.zu[k], self.zl[k], zwt[j - 1], self.av[k], nv[k]) / self.dz[k]
    
            self.Sum_WC_depth[j - 1][k] = self.Sum_WC_depth[j - 1][k - 1] + self.WC[j - 1][k] * self.dz[k]
            Depletion[j - 1][k] = (self.FC[k] - self.WC[j - 1][k]) * self.dz[k] * self.Fw[k]
        self.WC[j - 1][0] = self.ts[1]
        self.Equilibrium_Max[j - 1] = 0
        self.Sum_WC_depth[j - 1][0] = 0
        for k in range(1, self.Num_layers + 2):
            self.Sum_WC_depth[j - 1][k] = self.Sum_WC_depth[j - 1][k - 1] + self.WC[j - 1][k] * self.dz[k]
            if self.Sum_WC_depth[j - 1][k] > ts_depth[k] * Fraction_of_saturation_for_equilibrium:
                self.Equilibrium_Max[j - 1] = k
    
        Sum_depths[j - 1] = 0
        if j > 1:
            Sum_depths[j - 2] = 0
        for k in range(1, self.Num_layers + 2):
            Sum_depths[j - 1] = Sum_depths[j - 1] + self.WC[j - 1][k] * self.dz[k] * self.Fw[k]
            if j > 1:
                Sum_depths[j - 2] = Sum_depths[j - 2] + self.WC[j - 1][k] * self.dz[k] * self.Fw[k]
    
    def water_table_simulation_with_eq_Max_greater_zero(self, j):
        ET_losses = 0
        for k in range(1, self.Equilibrium_Max[j] + 1):
            if k == self.Num_layers + 1:
                ET_losses = ET_losses + (self.E_wet[j] + self.ET_trans_wet[j] * self.Act_frac[j][k]) / 1000
            else:
                ET_losses = ET_losses + (self.ET_trans_wet[j] * self.Act_frac[j][k]) / 1000
        
#Find the drainage rate based on either the linear function or the Kirkham resistance function
        
        time_step = 1
        if self.Kirkham_rate == 1:
            if self.zwt[j-1] == self.Drain_elevation:
                Drain_flux = 0
            else:
                Drain_flux = self.Keff_horizontal / (1 + self.L_drain * self.Kirkham_F / (self.zwt[j-1] - self.Drain_elevation))
        else:
            if self.zwt[j-1] == self.Drain_elevation:
                Drain_flux = 0
            else:
                Drain_flux = self.Drain_rate * (self.zwt[j-1] - self.Drain_elevation) * time_step
        if Drain_flux < 0:
            Drain_flux = 0
#Find the fluxes above and below the range in equilibrium with the water table
        
        if self.Equilibrium_Max[j] == self.Num_layers + 1:
            Fluxes = self.Irrigation[j] / 1000 + self.Rain_Infilt[j] / 1000 - Drain_flux
        else:
            Fluxes = self.Infilt[j][self.Equilibrium_Max[j] + 1] - Drain_flux  #took out + 1
        
        
        k = self.Equilibrium_Max[j]
        
#Add the fluxes and ET losses to the sum of water depth from previous time step
#in the layers in equilibrium with the water table

        self.Sum_WC_depth[j][k] = self.Sum_WC_depth[j-1][k] + (Fluxes - ET_losses)
        
#Find the elevation of the water table that would result in the Sum_WC_depth depth of water in the
#equilibrium layers
                   
        i = 1   #i is the counter for WC_test, there are 100 possible elevations
                #i = 1 corresponds to a water table at the bottom of the soil profile
        while i < 101 and self.WC_test[k][i] < self.Sum_WC_depth[j][k]: #test begins in the
            i = i + 1
        
#if the depth is not found in the current layer corresponding to equilibrium_max
#then the program looks in the next layer up and incorporates a layer above the equilibrium_max level
        
        Ave_WC = self.Sum_WC_depth[j][k] / (zu(self.Equilibrium_Max[j]) - self.zl[1])
        
#Set the water table at the elevation found, otherwise set the water table at the top of the soil profile
        
        if i < 101:
            self.zwt[j] = zwt_test(k, i)
        else:
            self.zwt[j] = self.zu(self.Num_layers + 1)
        
        
        self.zwt[j] = Find_wt(self.ts[k], self.tr[k], self.zu(self.Equilibrium_Max[j]), self.zl[1], self.av[k], self.nv[k], Ave_WC, self.zwt[j])
        
        for k in range(1, self.Equilibrium_Max[j] + 1):
            if self.zwt[j] > self.zu[k]:  #Water table is above cell
                self.WC[j][k] = self.ts[k]
            elif self.zu[k] > self.zwt[j] and self.zl[k] < self.zwt[j]:   #Water table is within cell
                self.WC[j][k] = d_cell_WT(self.ts[k], tr[k], self.zu[k], self.zl[k], self.zwt[j], self.av[k], self.nv[k]) / self.dz[k]
            elif self.zu[k] == self.zwt[j]:  #Water table is at top of cell
                self.WC[j][k] = self.ts[k]
            else:    #Water table is below cell or at lower boundary of cell
                self.WC[j][k] = d_cell_Eq(self.ts[k], tr[k], self.zu[k], self.zl[k], self.zwt[j], self.av[k], self.nv[k]) / self.dz[k]
            
            
            if k == 1:
                self.Infilt[j][k] = Drain_flux
                self.WC[j][0] = self.WC[j][1]
            else:
                self.Infilt[j][k] = self.Infilt[j][k - 1] + ET_trans[j] / 1000 * self.Act_frac[j][k - 1] + (self.WC[j][k - 1] - self.WC[j - 1][k - 1]) * self.dz(k - 1)
            
            Depletion[j][k] = (self.FC[k] - self.WC[j][k]) * self.dz[k] * self.Fw[k]
            Percent_depletion[j][k] = (self.FC[k] - self.WC[j][k]) / (self.FC[k] - PWP[k]) * 100
        
        base = 0
        self.Equilibrium_Max[j] = 0
        self.Sum_WC_depth[j][0] = 0
        if Keep_equilibrium_layers_out_of_root_zone:
            Max_layer = Max_layer_of_equilibrium_layers
        else:
            Max_layer = self.Num_layers + 1
        

        for k in range(1, Max_layer + 1):
            self.Sum_WC_depth[j][k] = self.Sum_WC_depth[j][k - 1] + self.WC[j][k] * self.dz[k]
            if self.Sum_WC_depth[j][k] > ts_depth[k] * Fraction_of_saturation_for_equilibrium:
                self.Equilibrium_Max[j] = k
    def water_table_simulation_with_eq_Max_equals_zero(self, j):
        if Continue_drainage_rate:
            WC_stop = d_cell_Eq(self.ts[1], self.tr[1], self.zu[1], self.zl[1], 0, self.av[1], self.nv[1]) / self.dz[1]
            if self.WC[j - 1][1] < WC_stop:
                self.Infilt[j][1] = 0
            else:
                self.Infilt[j][1] = self.Infilt[j - 1][1] * self.Infilt[j - 1][1] / self.Infilt(j - 2, 1)
            
        else:
            self.Infilt[j][1] = 0
        
        self.WC[j][1] = self.WC[j - 1][1] - self.Infilt[j][1] / self.dz[1] / self.Fw[1] + self.Infilt[j][2] / self.dz[2] / self.Fw[2]
        

def hg(a, b, C, z):

    value = 1
    hg = value
    
    for i in range(1,41):
        value = value * (a + i - 1) * (b + i - 1) / (C + i - 1) / i * z
        hg = hg + value
    return hg

def d_total(ts, tr, zt, zwt, alpha, N):

    W = -((alpha * (zt - zwt) * 100) ** N)
    zwt = zwt
    hyper = hg(1, 1 - 1 / N, 1 + 1 / N, W / (W - 1))

    d_total = ts * zwt + tr * (zt - zwt) + (ts - tr) * (zt - zwt) * (1 - W) ** (1 / N - 1) * hyper
    return d_total

def d_cell_WT(ts, tr, zu, zl, zwt, alpha, N):

    W = -((alpha * (zu - zwt) * 100) ^ N)
    hyper = hg(1, 1 - 1 / N, 1 + 1 / N, W / (W - 1))

    d_cell_WT = ts * (zwt - zl) + tr * (zu - zwt) + (ts - tr) * (zu - zwt) * (1 - W) ** (1 / N - 1) * hyper
    return d_cell_WT

def d_cell_Eq(ts, tr, zu, zl, zwt, alpha, N):

    WU = -((alpha * (zu - zwt) * 100) ** N)
    wl = -((alpha * (zl - zwt) * 100) ** N)
    hyperu = hg(1, 1 - 1 / N, 1 + 1 / N, WU / (WU - 1))
    hyperl = hg(1, 1 - 1 / N, 1 + 1 / N, wl / (wl - 1))

    d_cell_Eq = tr * (zu - zl) + (ts - tr) * (zu - zwt) * (1 - WU) ** (1 / N - 1) * hyperu - (ts - tr) * (zl - zwt) * (1 - wl) ** (1 / N - 1) * hyperl
    return d_cell
    
def Find_wt(ts, tr, zu, zl, alpha, N, th_ave, zwt_last_time):

    dz = zu - zl
    d_layer_ave = th_ave * dz
    zwt = zwt_last_time
    
    W = -((alpha * (zu - zwt) * 100) ** N)
    
    hyper = hg(1, 1 - 1 / N, 1 + 1 / N, W / (W - 1))

    d_layer_2 = ts * (zwt - zl) + tr * (zu - zwt) + (ts - tr) * (zu - zwt) * (1 - W) ** (1 / N - 1) * hyper
    
    if zwt > 0.15:
        Convergence = 0.00001
    else:
        Convergence = 0.00001
   
    while abs(d_layer_2 - d_layer_ave) > Convergence:
    
        W = -((alpha * (zu - zwt) * 100) ** N)
        
        hyper = hg(1, 1 - 1 / N, 1 + 1 / N, W / (W - 1))
    
        d_layer_2 = ts * (zwt - zl) + tr * (zu - zwt) + (ts - tr) * (zu - zwt) * (1 - W) ** (1 / N - 1) * hyper
    
        zwt = zwt * (d_layer_ave / d_layer_2) ^ 0.5
    
    return zwt
        
def zwt_crit(ts, tr, zu, zl, zwt, alpha, N):

    W = -((alpha * (zu - zwt) * 100) ** N)
    hyper = hg(1, 1 - 1 / N, 1 + 1 / N, W / (W - 1))

    zwt_crit = ts * (zwt - zl) + tr * (zu - zwt) + (ts - tr) * (zu - zwt) * (1 - W) ** (1 / N - 1) * hyper
    return zwt_crit

def Calculate_k(te, mv, Ko, L):
        
    if te > 1:
        Calculate_k = Ko * 0.1
    else:
        Calculate_k = Ko * te ** L * (1 - (1 - te ** (1 / mv)) ** mv) ** 2
    return Calculate_k

def Calculate_te(WC, tr, ts):

    if WC > tr:
        Calculate_te = (WC - tr) / (ts - tr)
    else:
        Calculate_te = 0.00001
    return Calculate_te

def KirkhamSolution(x, S, r, h, k, re):
    
    Kirkham_height = (math.log(math.sin(3.14159 * x / (2 * S)) / math.sin(Pi * r / (2 * S))))
    sum = 0
    for m in range(1, 400):
        sum = sum + ((1 / m) * (math.cos(m * 3.14159 * r / S) - math.cos(m * 3.14159 * x / S)) * (math.exp(-m * 3.14159 * h / S) / np.sinh(m * 3.14159 * h / S)))
    Kirkham_height = Kirkham_height + sum

    Kirkham_height = re * 2 * S * Kirkham_height / (k * 3.14159)
    return Kirkham_height  



