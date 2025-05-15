from odoo import models, fields, api
from odoo.exceptions import ValidationError

class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    ubicacion = fields.Selection([
        ('PANTITLAN', 'Pantitlan'),
        ('OTRO', 'Otro'),
    ], string='Ubicación')

    distrito = fields.Selection([
        ('NEZA', 'Neza'),
        ('AEROPUERTO', 'Aeropuerto'),
        ('LOS_REYES', 'Los Reyes'),
        ('CONDESA', 'Condesa'),
    ], string='Distrito')

    @api.onchange('ubicacion')
    def _onchange_ubicacion(self):
        if self.ubicacion == 'PANTITLAN':
            return {
                'domain': {'distrito': [('distrito', 'in', ['NEZA', 'AEROPUERTO', 'LOS_REYES'])]}
            }
        else:
            return {
                'domain': {'distrito': [('distrito', 'in', ['NEZA', 'AEROPUERTO', 'LOS_REYES', 'CONDESA'])]}
            }

    @api.constrains('ubicacion', 'distrito')
    def _check_distrito_valido(self):
        for record in self:
            if record.ubicacion == 'PANTITLAN' and record.distrito not in ['NEZA', 'AEROPUERTO', 'LOS_REYES']:
                raise ValidationError("El distrito seleccionado no es válido para la ubicación 'PANTITLAN'.")
