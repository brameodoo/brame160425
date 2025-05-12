from odoo import api, fields, models, _
from odoo.exceptions import UserError

class TallerSolicitud(models.Model):
    _name = 'taller.solicitud'
    _description = 'Solicitud de Ingreso al Taller'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    name = fields.Char(string='Número de Solicitud', required=True, copy=False, readonly=True, index=True, default='New')
    analista_id = fields.Many2one('res.users', string='Analista', default=lambda self: self.env.user, tracking=True, readonly=True)
    vehiculo_id = fields.Many2one('fleet.vehicle', string='Vehículo', required=True, tracking=True)
    descripcion_falla = fields.Text(string='Descripción de la Falla', tracking=True)
    telefono_analista = fields.Char(string='Teléfono del Analista', compute='_compute_telefono_analista', store=True)
    fecha_solicitud = fields.Date(string='Fecha de Solicitud', default=fields.Date.context_today, tracking=True)
    fecha_asignacion = fields.Date(string='Fecha de Asignación', tracking=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmado')
    ], string='Estado', default='draft', tracking=True)

    @api.depends('analista_id')
    def _compute_telefono_analista(self):
        for record in self:
            employee = self.env['hr.employee'].search([('user_id', '=', record.analista_id.id)], limit=1)
            record.telefono_analista = employee.work_phone if employee else ''

    def action_confirmar(self):
        for record in self:
            record.state = 'confirmed'

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('taller.solicitud') or 'New'
        return super(TallerSolicitud, self).create(vals)
