# -*- coding: utf-8 -*-
"""
Created on Wed May 17 00:20:42 2017

@author: Brian Confessor e Débora Pina
"""

from ..common.mail import send_email
from ..models import  AdministradorSistema
import os.path
from . import db
import json

def get_chart_data(chart_type, start_date, end_date, lab_id):
    data = []
    if (chart_type == "temperatura"):
        data = db.fetchall("""
            SELECT data, temp
            FROM Log_Lab
            WHERE lab_id = ?
            AND data > ?
            AND data < ?
            ORDER BY data ASC;""", (lab_id, start_date, end_date))
    elif (chart_type == "umidade"):
        data = db.fetchall("""
            SELECT data, umid
            FROM Log_Lab
            WHERE lab_id = ?
            AND data > ?
            AND data < ?
            ORDER BY data ASC;""", (lab_id, start_date, end_date))
    # print("Data: {}".format(data))
    return data

def get_environment_data(start_date, end_date, lab_id):
    data = db.fetchall("""
            SELECT data, temp, umid
            FROM Log_Lab
            WHERE lab_id = ?
            AND data > ?
            AND data < ?
            ORDER BY data ASC;""", (lab_id, start_date, end_date))
    return data


def get_equip_chart_data(chart_type, chart_target, start_date, end_date, lab_id):
    data = []
    if (chart_type == "temperatura"):
        data = db.fetchall("""
            SELECT data, temp
            FROM Log_Equip
            WHERE equip_id = ?
            AND data > ?
            AND data < ?
            ORDER BY data ASC;""", (chart_target, start_date, end_date))
    # print("Data: {}".format(data))
    return data
