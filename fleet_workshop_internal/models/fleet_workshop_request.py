from odoo import models, fields, api
from odoo.exceptions import ValidationError

class FleetWorkshopRequest(models.Model):
    _name = 'fleet.workshop.request'
    _description = 'Solicitud de Taller para Flota Vehicular'
    _inherit = ['mail.thread', 'mail.activity_mixin']

    name = fields.Char(string='Número de Solicitud', required=True, copy=False, default='Nuevo')
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehículo', required=True, ondelete='cascade', index=True)
    license_plate = fields.Char(related='vehicle_id.license_plate', string='Matrícula', readonly=True, store=True)
    vin_sn = fields.Char(related='vehicle_id.vin_sn', string='Número de Chasis', readonly=True, store=True)
    model_id = fields.Many2one(related='vehicle_id.model_id', string='Modelo', readonly=True, store=True)
    driver_id = fields.Many2one(related='vehicle_id.driver_id', string='Conductor', readonly=True, store=True)
    location = fields.Char(related='vehicle_id.location', string='Ubicación', readonly=True, store=True)
    district_id = fields.Many2one('fleet.workshop.district', string='Distrito', required=True)
    analyst_id = fields.Many2one('hr.employee', string='Analista', default=lambda self: self.env.user.employee_id, readonly=True)
    analyst_phone = fields.Char(related='analyst_id.mobile_phone', string='Teléfono Analista', readonly=True)
    analyst_email = fields.Char(related='analyst_id.work_email', string='Correo Analista', readonly=True)
    contact_phone = fields.Char(string='Teléfono de Contacto')
    request_date = fields.Date(string='Fecha de Solicitud', default=fields.Date.context_today)
    failure_description = fields.Text(string='Descripción de la Falla', required=True)
    state = fields.Selection([
        ('generated', 'Generado'),
        ('waiting_assignment', 'Espera de Asignación'),
        ('assignment_rejected', 'Asignación Rechazada'),
        ('assigned', 'Asignado'),
    ], string='Estado', default='generated', tracking=True)
    assignment_date = fields.Date(string='Fecha de Asignación', tracking=True)
    reception_date = fields.Date(string='Fecha de Recepción en Taller', tracking=True)
    rejection_reason = fields.Text(string='Motivo de Rechazo')
    whatsapp_notification = fields.Boolean(string='Enviar notificación por WhatsApp')
    tag_ids = fields.Many2many('fleet.workshop.tag', string='Etiquetas')

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('fleet.workshop.request') or 'Nuevo'
        return super(FleetWorkshopRequest, self).create(vals)

    @api.onchange('reception_date')
    def _onchange_reception_date(self):
        if self.reception_date:
            template_id = self.env.ref('fleet_workshop_internal.mail_template_fleet_workshop_request_assigned')
            template_id.send_mail(self.id, force_send=True)

    @api.constrains('vehicle_id', 'state')
    def _check_duplicate_request(self):
        for rec in self:
            if rec.state in ('generated', 'waiting_assignment', 'assigned'):
                existing_request = self.search([
                    ('vehicle_id', '=', rec.vehicle_id.id),
                    ('state', 'in', ('generated', 'waiting_assignment', 'assigned')),
                    ('id', '!=', rec.id)
                ], limit=1)
                if existing_request:
                    raise ValidationError(f"Ya existe una solicitud activa para el vehículo {rec.vehicle_id.license_plate}.")
