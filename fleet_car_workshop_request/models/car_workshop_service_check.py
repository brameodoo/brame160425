# -*- coding: utf-8 -*-
from odoo import models, fields

class CarWorkshopServiceCheck(models.Model):
    _name = 'car.workshop.service.check'
    _description = 'Verificación de Servicios en Orden de Taller'

    workshop_id = fields.Many2one('car.workshop', string='Orden de Taller')
    service_id = fields.Many2one('product.product', string='Servicio')
    completed = fields.Boolean(string='Realizado')
