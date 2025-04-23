from odoo import models, fields

class FleetWorkshopRepairImage(models.Model):
    _name = 'fleet.workshop.repair.image'
    _description = 'Imágenes de Reparación de Taller'

    order_id = fields.Many2one('fleet.workshop.order', string='Orden de Trabajo', ondelete='cascade', required=True)
    image = fields.Image(string='Imagen')
    description = fields.Char(string='Descripción de la Imagen')
