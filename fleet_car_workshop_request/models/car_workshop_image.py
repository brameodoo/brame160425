# -*- coding: utf-8 -*-
from odoo import models, fields

class CarWorkshopImage(models.Model):
    _name = 'car.workshop.image'
    _description = 'Imágenes de Servicio de Taller'

    workshop_id = fields.Many2one('car.workshop', string='Orden de Taller')
    image = fields.Image(string='Imagen')
    description = fields.Char(string='Descripción')
