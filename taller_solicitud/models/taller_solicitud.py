from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class TallerSolicitud(models.Model):
    _name = 'taller.solicitud'
    _description = 'Solicitud de Taller'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha_solicitud desc'

    name = fields.Char(string='Folio', required=True, copy=False, readonly=True, default='Nuevo')
    analista_id = fields.Many2one('hr.employee', string='Analista', required=True, default=lambda self: self.env.user.employee_id)
    vehiculo_id = fields.Many2one('fleet.vehicle', string='Vehículo', required=True)
    descripcion_falla = fields.Text(string='Descripción de la Falla', required=True)
    telefono_analista = fields.Char(string='Teléfono del Analista', related='analista_id.work_phone', readonly=True)
    fecha_solicitud = fields.Datetime(string='Fecha de Solicitud', default=fields.Datetime.now, readonly=True)
    fecha_asignacion = fields.Datetime(string='Fecha de Asignación')
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmado')
    ], string='Estado', default='draft', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('taller.solicitud') or 'Nuevo'
        return super().create(vals)

    def action_confirmar(self):
        for record in self:
            record.state = 'confirmed'
