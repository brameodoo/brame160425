from odoo import models, fields, api

class FleetWorkshopOrder(models.Model):
    _name = 'fleet.workshop.order'
    _description = 'Orden de Trabajo de Taller para Flota'
    _inherit = ['mail.thread', 'mail.activity_mixin']

    name = fields.Char(string='Número de Orden', required=True, copy=False, default='Nuevo')
    request_id = fields.Many2one('fleet.workshop.request', string='Solicitud de Taller', ondelete='restrict', required=True)
    vehicle_id = fields.Many2one(related='request_id.vehicle_id', string='Vehículo', readonly=True, store=True)
    license_plate = fields.Char(related='vehicle_id.license_plate', string='Matrícula', readonly=True, store=True)
    vin_sn = fields.Char(related='vehicle_id.vin_sn', string='Número de Chasis', readonly=True, store=True)
    model_id = fields.Many2one(related='vehicle_id.model_id', string='Modelo', readonly=True, store=True)
    driver_id = fields.Many2one(related='vehicle_id.driver_id', string='Conductor', readonly=True, store=True)
    district_id = fields.Many2one(related='request_id.district_id', string='Distrito', readonly=True, store=True)
    analyst_id = fields.Many2one(related='request_id.analyst_id', string='Analista', readonly=True, store=True)
    analyst_phone = fields.Char(related='request_id.analyst_phone', string='Teléfono Analista', readonly=True, store=True)
    analyst_email = fields.Char(related='request_id.analyst_email', string='Correo Analista', readonly=True, store=True)
    contact_phone = fields.Char(related='request_id.contact_phone', string='Teléfono de Contacto', readonly=True, store=True)
    request_date = fields.Date(related='request_id.request_date', string='Fecha de Solicitud', readonly=True, store=True)
    assignment_date = fields.Date(related='request_id.assignment_date', string='Fecha de Asignación', readonly=True, store=True)
    reception_date = fields.Date(string='Fecha de Recepción en Taller', default=fields.Date.context_today, tracking=True)
    failure_description = fields.Text(related='request_id.failure_description', string='Descripción de la Falla (Solicitud)', readonly=True, store=True)
    mechanic_id = fields.Many2one('hr.employee', string='Mecánico Asignado', domain=[('job_id.name', 'ilike', 'mecánico')], tracking=True)
    odometer = fields.Integer(string='Odómetro (al Ingreso)')
    fuel_level = fields.Float(string='Nivel de Gasolina (al Ingreso)')
    diagnosis = fields.Text(string='Diagnóstico del Mecánico')
    service_ids = fields.Many2many('product.template', 'fleet_workshop_order_service_rel', 'order_id', 'service_id', string='Servicios a Realizar')
    picking_ids = fields.One2many('stock.picking', 'workshop_order_id', string='Transferencias de Almacén')
    repair_image_ids = fields.One2many('fleet.workshop.repair.image', 'order_id', string='Imágenes de Reparación')
    repair_line_ids = fields.One2many('fleet.workshop.repair.line', 'order_id', string='Verificación de Servicios')
    notes = fields.Text(string='Notas de Reparación')
    state = fields.Selection([
        ('entry', 'Entrada a Taller'),
        ('inspection', 'Inspección de Unidad'),
        ('assign_mechanic', 'Asignar Mecánico'),
        ('in_repair', 'En Reparación'),
        ('repaired', 'Reparado'),
    ], string='Estado de la Orden', default='entry', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('fleet.workshop.order') or 'Nuevo'
        return super(FleetWorkshopOrder, self).create(vals)

    def action_assign_mechanic(self):
        self.write({'state': 'assign_mechanic'})

    def action_start_repair(self):
        self.write({'state': 'in_repair'})

    def action_mark_repaired(self):
        self.write({'state': 'repaired'})
        # Aquí iría la lógica para enviar el correo al analista

    def create_stock_picking(self):
        # Aquí iría la lógica para crear la solicitud de picking
        pass

    def action_view_pickings(self):
        action = self.env['ir.actions.act_window']._for_model('stock.picking')
        action['domain'] = [('workshop_order_id', '=', self.id)]
        action['context'] = {
            'default_origin': self.name,
            'default_workshop_order_id': self.id,
            'default_picking_type_id': self.env.ref('stock.picking_type_internal').id, # Ajustar según tu tipo de picking interno
            'default_location_id': self.env.user.company_id.stock_location.id, # Ajustar ubicación de origen
            'default_location_dest_id': self.env.ref('stock.stock_location_stock').id, # Ajustar ubicación de destino (taller)
        }
        return action

    def _create_repair_lines(self):
        for service in self.service_ids:
            self.env['fleet.workshop.repair.line'].create({
                'order_id': self.id,
                'service_id': service.id,
                'name': service.name,
            })
        self.write({'state': 'inspection'}) # Cambiamos el estado después de crear las líneas

    @api.onchange('service_ids')
    def _onchange_service_ids(self):
        existing_lines = self.repair_line_ids.mapped('service_id')
        new_services = self.service_ids - existing_lines
        lines_to_create = []
        for service in new_services:
            lines_to_create.append((0, 0, {
                'service_id': service.id,
                'name': service.name,
                'order_id': self.id, # Asegurarse de tener el ID de la orden
            }))
        if lines_to_create:
            self.repair_line_ids = [(0, 0, line) for line in lines_to_create]
        lines_to_unlink = self.repair_line_ids.filtered(lambda l: l.service_id not in self.service_ids)
        if lines_to_unlink:
            self.repair_line_ids = [(2, line.id, False) for line in lines_to_unlink]

    @api.depends('picking_ids')
    def _compute_picking_count(self):
        for order in self:
            order.picking_count = len(order.picking_ids)

    picking_count = fields.Integer(string='Número de Transferencias', compute='_compute_picking_count')
