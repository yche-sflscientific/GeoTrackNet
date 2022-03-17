# coding: utf-8

# MIT License
# 
# Copyright (c) 2018 Duong Nguyen
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

"""
A script to merge AIS messages into AIS tracks.
"""
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
#sys.path.append("..")
#import utils
import pickle
import copy
import csv
from datetime import datetime
import time
from io import StringIO
from tqdm import tqdm as tqdm

import pdb
import pandas as pd
import dask.dataframe as dd

## PARAMS
#======================================

## Bretagne dataset
# LAT_MIN = 46.5
# LAT_MAX = 50.5
# LON_MIN = -8.0
# LON_MAX = -3.0

# # Pkl filenames.
# pkl_filename = "bretagne_20170103_track.pkl"
# pkl_filename_train = "bretagne_20170103_10_20_train_track.pkl"
# pkl_filename_valid = "bretagne_20170103_10_20_valid_track.pkl"
# pkl_filename_test  = "bretagne_20170103_10_20_test_track.pkl"

# # Path to csv files.
# dataset_path = "./"
# l_csv_filename =["positions_bretagne_jan_mar_2017.csv"]


# # Training/validation/test/total period.
# t_train_min = time.mktime(time.strptime("01/01/2017 00:00:00", "%d/%m/%Y %H:%M:%S"))
# t_train_max = time.mktime(time.strptime("10/03/2017 23:59:59", "%d/%m/%Y %H:%M:%S"))
# t_valid_min = time.mktime(time.strptime("11/03/2017 00:00:00", "%d/%m/%Y %H:%M:%S"))
# t_valid_max = time.mktime(time.strptime("20/03/2017 23:59:59", "%d/%m/%Y %H:%M:%S"))
# t_test_min  = time.mktime(time.strptime("21/03/2017 00:00:00", "%d/%m/%Y %H:%M:%S"))
# t_test_max  = time.mktime(time.strptime("31/03/2017 23:59:59", "%d/%m/%Y %H:%M:%S"))
# t_min = time.mktime(time.strptime("01/01/2017 00:00:00", "%d/%m/%Y %H:%M:%S"))
# t_max = time.mktime(time.strptime("31/03/2017 23:59:59", "%d/%m/%Y %H:%M:%S"))

# cargo_tanker_filename = "bretagne_20170103_cargo_tanker.npy"

# # ## Aruba
# LAT_MIN = 9.0
# LAT_MAX = 14.0
# LON_MIN = -71.0
# LON_MAX = -66.0

# D2C_MIN = 2000 #meters


# #===============
# """
# dataset_path = "./"
# l_csv_filename =["aruba_5x5deg_2017305_2018031.csv",
#                  "aruba_5x5deg_2018305_2019031.csv",
#                  "aruba_5x5deg_2019305_2020031.csv"]
# l_csv_filename =["aruba_5x5deg_2017305_2018031.csv"]
# pkl_filename = "aruba_20172020_track.pkl"
# pkl_filename_train = "aruba_20172020_train_track.pkl"
# pkl_filename_valid = "aruba_20172020_valid_track.pkl"
# pkl_filename_test  = "aruba_20172020_test_track.pkl"

# cargo_tanker_filename = "aruba_20172020_cargo_tanker.npy"

# t_train_min = time.mktime(time.strptime("01/01/2017 00:00:00", "%d/%m/%Y %H:%M:%S"))
# t_train_max = time.mktime(time.strptime("31/01/2019 23:59:59", "%d/%m/%Y %H:%M:%S"))
# t_valid_min = time.mktime(time.strptime("01/11/2019 00:00:00", "%d/%m/%Y %H:%M:%S"))
# t_valid_max = time.mktime(time.strptime("31/12/2019 23:59:59", "%d/%m/%Y %H:%M:%S"))
# t_test_min  = time.mktime(time.strptime("01/01/2020 00:00:00", "%d/%m/%Y %H:%M:%S"))
# t_test_max  = time.mktime(time.strptime("31/01/2020 23:59:59", "%d/%m/%Y %H:%M:%S"))
# t_min = time.mktime(time.strptime("01/01/2017 00:00:00", "%d/%m/%Y %H:%M:%S"))
# t_max = time.mktime(time.strptime("31/01/2020 23:59:59", "%d/%m/%Y %H:%M:%S"))

# """

# #===============
# """
# dataset_path = "./"
# l_csv_filename =["aruba_zone1_5x5deg_2017121_2017244.csv",
#                  "aruba_5x5deg_2018121_2018244.csv",
#                  "aruba_zone1_5x5deg_2019121_2019244.csv"]
# #l_csv_filename =["aruba_5x5deg_2018121_2018244.csv"]
# pkl_filename = "aruba_20172020_summer_track.pkl"
# pkl_filename_train = "aruba_20172020_summer_train_track.pkl"
# pkl_filename_valid = "aruba_20172020_summer_valid_track.pkl"
# pkl_filename_test  = "aruba_20172020_summer_test_track.pkl"

# cargo_tanker_filename = "aruba_20172020_summer_cargo_tanker.npy"

# t_train_min = time.mktime(time.strptime("01/01/2017 00:00:00", "%d/%m/%Y %H:%M:%S"))
# t_train_max = time.mktime(time.strptime("31/08/2018 23:59:59", "%d/%m/%Y %H:%M:%S"))
# t_valid_min = time.mktime(time.strptime("01/05/2019 00:00:00", "%d/%m/%Y %H:%M:%S"))
# t_valid_max = time.mktime(time.strptime("31/07/2019 23:59:59", "%d/%m/%Y %H:%M:%S"))
# t_test_min  = time.mktime(time.strptime("01/08/2019 00:00:00", "%d/%m/%Y %H:%M:%S"))
# t_test_max  = time.mktime(time.strptime("31/08/2019 23:59:59", "%d/%m/%Y %H:%M:%S"))
# t_min = time.mktime(time.strptime("01/01/2017 00:00:00", "%d/%m/%Y %H:%M:%S"))
# t_max = time.mktime(time.strptime("31/01/2020 23:59:59", "%d/%m/%Y %H:%M:%S"))
# """

# #===============
# """
# dataset_path = "./"
# l_csv_filename =["aruba_zone1_5x5deg_2017121_2017244.csv",
#                  "aruba_5x5deg_2017305_2018031.csv",
#                  "aruba_5x5deg_2018121_2018244.csv",
#                  "Aruba_5x5deg_2018305_2019031.csv",
#                  "aruba_zone1_5x5deg_2019121_2019244.csv"]
# #l_csv_filename =["Aruba_5x5deg_2018305_2019031.csv"]
# pkl_filename = "aruba_20172019_track.pkl"
# pkl_filename_train = "aruba_20172019_all_train_track.pkl"
# pkl_filename_valid = "aruba_20172019_all_valid_track.pkl"
# pkl_filename_test  = "aruba_20172019_all_test_track.pkl"

# cargo_tanker_filename = "aruba_20172019_all_cargo_tanker.npy"

# t_train_min = time.mktime(time.strptime("01/01/2017 00:00:00", "%d/%m/%Y %H:%M:%S"))
# t_train_max = time.mktime(time.strptime("31/01/2019 23:59:59", "%d/%m/%Y %H:%M:%S"))
# t_valid_min = time.mktime(time.strptime("01/05/2019 00:00:00", "%d/%m/%Y %H:%M:%S"))
# t_valid_max = time.mktime(time.strptime("31/07/2019 23:59:59", "%d/%m/%Y %H:%M:%S"))
# t_test_min  = time.mktime(time.strptime("01/08/2019 00:00:00", "%d/%m/%Y %H:%M:%S"))
# t_test_max  = time.mktime(time.strptime("31/08/2019 23:59:59", "%d/%m/%Y %H:%M:%S"))
# t_min = time.mktime(time.strptime("01/01/2017 00:00:00", "%d/%m/%Y %H:%M:%S"))
# t_max = time.mktime(time.strptime("31/01/2020 23:59:59", "%d/%m/%Y %H:%M:%S"))
# """

# #===============
# # ## Est Aruba
# LAT_MIN = 10.0
# LAT_MAX = 14.0
# LON_MIN = -66.0
# LON_MAX = -60.0

# dataset_path = "./"
# l_csv_filename =["Est-aruba_5x5deg_2018001_2018120.csv",
#                  "Est-aruba_5x5deg_2018001_2018180.csv",
#                 "Est-aruba_5x5deg_2019240_2019365_.csv"]
# #l_csv_filename =["Est-aruba_5x5deg_2018001_2018180.csv"]
# pkl_filename = "estaruba_20182019_track.pkl"
# pkl_filename_train = "estaruba_20182019_train_track.pkl"
# pkl_filename_valid = "estaruba_20182019_valid_track.pkl"
# pkl_filename_test  = "estaruba_20182019_test_track.pkl"

# cargo_tanker_filename = "estaruba_20182019_cargo_tanker.npy"

# t_train_min = time.mktime(time.strptime("01/01/2018 00:00:00", "%d/%m/%Y %H:%M:%S"))
# t_train_max = time.mktime(time.strptime("30/04/2019 23:59:59", "%d/%m/%Y %H:%M:%S"))
# t_valid_min = time.mktime(time.strptime("01/09/2019 00:00:00", "%d/%m/%Y %H:%M:%S"))
# t_valid_max = time.mktime(time.strptime("30/11/2019 23:59:59", "%d/%m/%Y %H:%M:%S"))
# t_test_min  = time.mktime(time.strptime("01/12/2019 00:00:00", "%d/%m/%Y %H:%M:%S"))
# t_test_max  = time.mktime(time.strptime("31/12/2019 23:59:59", "%d/%m/%Y %H:%M:%S"))
# t_min = time.mktime(time.strptime("01/01/2017 00:00:00", "%d/%m/%Y %H:%M:%S"))
# t_max = time.mktime(time.strptime("31/01/2020 23:59:59", "%d/%m/%Y %H:%M:%S"))

#===============
# ## NOLA
LAT_MIN = 28.0
LAT_MAX = 29.5
LON_MIN = -91.0
LON_MAX = -88

dataset_path = "/Users/yucheng/Documents/IUU/iuu_data/US_coastal_scenes/"
l_csv_filename =["AIS_2020_03_30.csv", "AIS_2020_03_31.csv"]
#l_csv_filename =["Est-aruba_5x5deg_2018001_2018180.csv"]
pkl_filename = "nola_2018_0330_track.pkl"
pkl_filename_train = "nola_2018_0330_track.pkl"
pkl_filename_valid = "nola_2018_0330_valid.pkl"
pkl_filename_test  = "nola_2018_0330_test.pkl"

cargo_tanker_filename = "nola_2010_0330_cargo_tanker.npy"

t_train_min = '2020-03-30T00:00:00'
t_train_max = '2020-03-30T23:59:59'
t_valid_min = '2020-03-31T00:00:00'
t_valid_max = '2020-03-31T11:59:59'
t_test_min  = '2020-03-31T12:00:00'
t_test_max  = '2020-03-31T23:59:59'
t_min = '2020-03-30T00:00:00'
t_max = '2020-03-31T23:59:59'


#========================================================================
LAT_RANGE = LAT_MAX - LAT_MIN
LON_RANGE = LON_MAX - LON_MIN
SOG_MAX = 30.0  # the SOG is truncated to 30.0 knots max.

EPOCH = datetime(1970, 1, 1)
#LAT, LON, SOG, COG, HEADING, ROT, NAV_STT, TIMESTAMP, MMSI, SHIPTYPE, D2C  = list(range(11))
fields = ["LAT", "LON", "SOG", "COG", "Heading", "TransceiverClass", "Status", "BaseDateTime", "MMSI", "VesselType", "CallSign"]
MMSI, LAT, LON, SOG, COG, Heading, ROT, NAV_STT, TIMESTAMP, SHIPTYPE = 0, 2, 3, 4, 5, 6, 7, 9, 1, 8

CARGO_TANKER_ONLY = False
dask = True

if  CARGO_TANKER_ONLY:
    pkl_filename = "ct_"+pkl_filename
    pkl_filename_train = "ct_"+pkl_filename_train
    pkl_filename_valid = "ct_"+pkl_filename_valid
    pkl_filename_test  = "ct_"+pkl_filename_test
    
print(pkl_filename_train)


## LOADING CSV FILES
#======================================
if not dask:
    l_l_msg = [] # list of AIS messages, each row is a message (list of AIS attributes)
    n_error = 0
    for csv_filename in l_csv_filename:
        data_path = os.path.join(dataset_path,csv_filename)
        print("Reading ", csv_filename, "...")
        df_tmp = pd.read_csv(data_path, index_col=None, header=0, usecols=fields)
        l_l_msg.append(df_tmp)
    frame = pd.concat(l_l_msg, axis=0, ignore_index=True)    

    m_msg = np.array(frame)
    del l_l_msg
else:
    flist = [os.path.join(dataset_path, fname) for fname in l_csv_filename]
    frame = dd.read_csv(flist, dtype={'IMO': 'object', 'Status': 'float64'})

print("Total number of AIS messages: ",len(frame))


print("Lat min: ",np.min(frame['LAT']), "Lat max: ",np.max(frame['LAT']))
print("Lon min: ",np.min(frame['LON']), "Lon max: ",np.max(frame['LON']))
print("Ts min: ",np.min(frame['BaseDateTime']), "Ts max: ",np.max(frame['BaseDateTime']))

# if m_msg[0,TIMESTAMP] > 1584720228: 
#     m_msg[:,TIMESTAMP] = m_msg[:,TIMESTAMP]/1000 # Convert to suitable timestamp format

print("Time min: ", np.min(frame['BaseDateTime']))
print("Time max: ", np.max(frame['BaseDateTime']))

## Vessel Type    
#======================================
# print("Selecting vessel type ...")
# def sublist(lst1, lst2):
#    ls1 = [element for element in lst1 if element in lst2]
#    ls2 = [element for element in lst2 if element in lst1]
#    return (len(ls1) != 0) and (ls1 == ls2)


# VesselTypes = dict()
# l_mmsi = []
# n_error = 0
# for v_msg in tqdm(m_msg):
#     try:
#         mmsi_ = v_msg[MMSI]
#         type_ = v_msg[SHIPTYPE]
#         if mmsi_ not in l_mmsi :
#             VesselTypes[mmsi_] = [type_]
#             l_mmsi.append(mmsi_)
#         elif type_ not in VesselTypes[mmsi_]:
#             VesselTypes[mmsi_].append(type_)
#     except:
#         n_error += 1
#         continue
# print(n_error)
# for mmsi_ in tqdm(list(VesselTypes.keys())):
#     VesselTypes[mmsi_] = np.sort(VesselTypes[mmsi_])
    
# l_cargo_tanker = []
# l_fishing = []
# # Use the code of VesselTypes to select Cargos/Tankers or Fishing
# for mmsi_ in list(VesselTypes.keys()):
#     if sublist(VesselTypes[mmsi_], list(range(70,80))) or sublist(VesselTypes[mmsi_], list(range(80,90))):
#         l_cargo_tanker.append(mmsi_)
#     if sublist(VesselTypes[mmsi_], [30]):
#         l_fishing.append(mmsi_)

l_cargo_tanker = frame[(frame['VesselType']<=90) & (frame['VesselType']>=70)]['MMSI'].unique()
l_fishing = frame[frame['VesselType']==30]['MMSI'].unique()

# print("Total number of vessels: ",len(VesselTypes))
print("Total number of cargos/tankers: ",len(l_cargo_tanker))
print("Total number of fishing: ",len(l_fishing))

# print("Saving vessels' type list to ", cargo_tanker_filename)
np.save(cargo_tanker_filename,l_cargo_tanker)
np.save(cargo_tanker_filename.replace("_cargo_tanker.npy","_fishing.npy"),l_fishing)

## FILTERING 
#======================================
# Selecting AIS messages in the ROI and in the period of interest.

# ## LAT LON
# m_msg = m_msg[m_msg[:,LAT]>=LAT_MIN]
# m_msg = m_msg[m_msg[:,LAT]<=LAT_MAX]
# m_msg = m_msg[m_msg[:,LON]>=LON_MIN]
# m_msg = m_msg[m_msg[:,LON]<=LON_MAX]
# # SOG
# m_msg = m_msg[m_msg[:,SOG]>=0]
# m_msg = m_msg[m_msg[:,SOG]<=SOG_MAX]
# # COG
# m_msg = m_msg[m_msg[:,SOG]>=0]
# m_msg = m_msg[m_msg[:,COG]<=360]
# # # D2C
# # m_msg = m_msg[m_msg[:,D2C]>=D2C_MIN]

# # TIME
# #m_msg = m_msg[m_msg[:,TIMESTAMP]>=0]

# m_msg = m_msg[m_msg[:,TIMESTAMP]>=t_min]
# m_msg = m_msg[m_msg[:,TIMESTAMP]<=t_max]
# m_msg_train = m_msg[m_msg[:,TIMESTAMP]>=t_train_min]
# m_msg_train = m_msg_train[m_msg_train[:,TIMESTAMP]<=t_train_max]
# m_msg_valid = m_msg[m_msg[:,TIMESTAMP]>=t_valid_min]
# m_msg_valid = m_msg_valid[m_msg_valid[:,TIMESTAMP]<=t_valid_max]
# m_msg_test  = m_msg[m_msg[:,TIMESTAMP]>=t_test_min]
# m_msg_test  = m_msg_test[m_msg_test[:,TIMESTAMP]<=t_test_max]


# Alternative, use Pandas to filter
# LAT/LON
frame = frame[(frame['LAT']>=LAT_MIN) & (frame['LAT']<=LAT_MAX) & (frame['LON']>=LON_MIN) & (frame['LON']<=LON_MAX)]

# SOG
frame = frame[(frame['SOG']>=0) & (frame['SOG']<=SOG_MAX)]

# COG
frame = frame[(frame['COG']>=0) & (frame['COG']<=360)]

# TIME
frame = frame[(frame['BaseDateTime']>=t_min) & (frame['BaseDateTime']<=t_max)]

# SHIPTYPE 
try:
    frame = frame.compute()
except:
    pass

# Split
train = frame[(frame['BaseDateTime']>=t_train_min) & (frame['BaseDateTime']<=t_train_max)]
valid = frame[(frame['BaseDateTime']>=t_valid_min) & (frame['BaseDateTime']<=t_valid_max)]
test = frame[(frame['BaseDateTime']>=t_test_min) & (frame['BaseDateTime']<=t_test_max)]

m_msg_train = np.array(train)
m_msg_valid = np.array(valid)
m_msg_test = np.array(test)

print("Total msgs: ",len(frame))
print("Number of msgs in the training set: ",len(m_msg_train))
print("Number of msgs in the validation set: ",len(m_msg_valid))
print("Number of msgs in the test set: ",len(m_msg_test))


## MERGING INTO DICT
#======================================
# Creating AIS tracks from the list of AIS messages.
# Each AIS track is formatted by a dictionary.
print("Convert to dicts of vessel's tracks...")

# Training set
Vs_train = dict()
for v_msg in tqdm(m_msg_train):
    mmsi = int(v_msg[MMSI])
    if not (mmsi in list(Vs_train.keys())):
        Vs_train[mmsi] = np.empty((0,9))
    Vs_train[mmsi] = np.concatenate((Vs_train[mmsi], np.expand_dims(v_msg[:9],0)), axis = 0)
for key in tqdm(list(Vs_train.keys())):
    if CARGO_TANKER_ONLY and (not key in l_cargo_tanker):
        del Vs_train[key]
    else:
        Vs_train[key] = np.array(sorted(Vs_train[key], key=lambda m_entry: m_entry[TIMESTAMP]))

# Validation set
Vs_valid = dict()
for v_msg in tqdm(m_msg_valid):
    mmsi = int(v_msg[MMSI])
    if not (mmsi in list(Vs_valid.keys())):
        Vs_valid[mmsi] = np.empty((0,9))
    Vs_valid[mmsi] = np.concatenate((Vs_valid[mmsi], np.expand_dims(v_msg[:9],0)), axis = 0)
for key in tqdm(list(Vs_valid.keys())):
    if CARGO_TANKER_ONLY and (not key in l_cargo_tanker):
        del Vs_valid[key]
    else:
        Vs_valid[key] = np.array(sorted(Vs_valid[key], key=lambda m_entry: m_entry[TIMESTAMP]))

# Test set
Vs_test = dict()
for v_msg in tqdm(m_msg_test):
    mmsi = int(v_msg[MMSI])
    if not (mmsi in list(Vs_test.keys())):
        Vs_test[mmsi] = np.empty((0,9))
    Vs_test[mmsi] = np.concatenate((Vs_test[mmsi], np.expand_dims(v_msg[:9],0)), axis = 0)
for key in tqdm(list(Vs_test.keys())):
    if CARGO_TANKER_ONLY and (not key in l_cargo_tanker):
        del Vs_test[key]
    else:
        Vs_test[key] = np.array(sorted(Vs_test[key], key=lambda m_entry: m_entry[TIMESTAMP]))


## PICKLING
#======================================
for filename, filedict in zip([pkl_filename_train,pkl_filename_valid,pkl_filename_test],
                              [Vs_train,Vs_valid,Vs_test]
                             ):
    print("Writing to ", os.path.join(dataset_path,filename),"...")
    with open(os.path.join(dataset_path,filename),"wb") as f:
        pickle.dump(filedict,f)
    print("Total number of tracks: ", len(filedict))
