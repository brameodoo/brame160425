# -*- coding: utf-8 -*-
from odoo import models, fields

class WorkshopDistrict(models.Model):
    _name = 'workshop.district'
    _description = 'Distrito de Taller'

    name = fields.Char(string='Nombre del Distrito', required=True)
