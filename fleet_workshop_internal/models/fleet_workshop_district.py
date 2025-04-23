from odoo import models, fields

class FleetWorkshopDistrict(models.Model):
    _name = 'fleet.workshop.district'
    _description = 'Distritos para Taller de Flota'
    _order = 'name'

    name = fields.Char(string='Nombre del Distrito', required=True, index=True)
    code = fields.Char(string='Código del Distrito', index=True)