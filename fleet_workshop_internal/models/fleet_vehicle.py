from odoo import models, fields, api

class FleetVehicleWorkshop(models.Model):
    _inherit = 'fleet.vehicle'

    workshop_order_ids = fields.One2many('fleet.workshop.order', 'vehicle_id', string='Órdenes de Trabajo del Taller')
    workshop_order_count = fields.Integer(string='Número de Reparaciones', compute='_compute_workshop_order_count')

    def action_view_workshop_orders(self):
        self.ensure_one()
        return {
            'name': 'Historial de Reparaciones',
            'type': 'ir.actions.act_window',
            'res_model': 'fleet.workshop.order',
            'view_mode': 'tree,form',
            'domain': [('vehicle_id', '=', self.id)],
            'context': {'default_vehicle_id': self.id},
        }

    @api.depends('workshop_order_ids')
    def _compute_workshop_order_count(self):
        for record in self:
            record.workshop_order_count = len(record.workshop_order_ids)
