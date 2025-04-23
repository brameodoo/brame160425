from odoo import models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    workshop_order_id = fields.Many2one('fleet.workshop.order', string='Orden de Trabajo del Taller', readonly=True, copy=False)
