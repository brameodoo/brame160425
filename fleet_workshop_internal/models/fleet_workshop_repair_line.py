from odoo import models, fields

class FleetWorkshopRepairLine(models.Model):
    _name = 'fleet.workshop.repair.line'
    _description = 'Líneas de Verificación de Servicio de Taller'

    order_id = fields.Many2one('fleet.workshop.order', string='Orden de Trabajo', ondelete='cascade', required=True)
    service_id = fields.Many2one('product.template', string='Servicio', readonly=True)
    name = fields.Char(string='Descripción del Servicio', readonly=True)
    is_done = fields.Boolean(string='Realizado')
