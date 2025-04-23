from odoo import models, fields

class FleetWorkshopTag(models.Model):
    _name = 'fleet.workshop.tag'
    _description = 'Etiquetas para Solicitudes de Taller'
    _order = 'name'

    name = fields.Char(string='Etiqueta', required=True)
    color = fields.Integer(string='Color')

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'La etiqueta debe ser única.'),
    ]