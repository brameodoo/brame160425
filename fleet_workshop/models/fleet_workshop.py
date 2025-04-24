from odoo import models, fields, api

class FleetWorkshopRequest(models.Model):
    _name = 'fleet.workshop.request'
    _description = 'Workshop Request'

    name = fields.Char(string='Request Number', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle', required=True)
    license_plate = fields.Char(related='vehicle_id.license_plate', string='License Plate', readonly=True)
    vin_sn = fields.Char(related='vehicle_id.vin_sn', string='Chassis Number', readonly=True)
    model_id = fields.Many2one(related='vehicle_id.model_id', string='Model', readonly=True)
    driver_id = fields.Many2one('hr.employee', string='Driver', required=True)
    district_id = fields.Many2one('fleet.district', string='District', required=True)
    analyst_id = fields.Many2one('hr.employee', string='Analyst', default=lambda self: self.env.user.employee_id.id, readonly=True)
    analyst_phone = fields.Char(related='analyst_id.mobile_phone', string='Analyst Phone', readonly=True)
    analyst_email = fields.Char(related='analyst_id.work_email', string='Analyst Email', readonly=True)
    contact_phone = fields.Char(string='Contact Phone')
    request_date = fields.Date(string='Request Date', default=fields.Date.context_today)
    fault_description = fields.Text(string='Fault Description', required=True)
    state = fields.Selection([
        ('generated', 'Generated'),
        ('waiting_assignment', 'Waiting Assignment'),
        ('assignment_rejected', 'Assignment Rejected'),
        ('assigned', 'Assigned')
    ], string='Status', default='generated')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('fleet.workshop.request') or _('New')
        result = super(FleetWorkshopRequest, self).create(vals)
        return result

class FleetWorkshopOrder(models.Model):
    _name = 'fleet.workshop.order'
    _description = 'Workshop Order'

    name = fields.Char(string='Order Number', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    request_id = fields.Many2one('fleet.workshop.request', string='Workshop Request', required=True)
    fields.Many2one(related='request_id.vehicle_id', string='Vehicle', readonly=True)
    license_plate = fields.Char(related='vehicle_id.license_plate', string='License Plate', readonly=True)
    vin_sn = fields.Char(related='vehicle_id.vin_sn', string='Chassis Number', readonly=True)
    model_id = fields.Many2one(related='vehicle_id.model_id', string='Model', readonly=True)
    driver_id = fields.Many2one(related='request_id.driver_id', string='Driver', readonly=True)
    district_id = fields.Many2one(related='request_id.district_id', string='District', readonly=True)
    analyst_id = fields.Many2one(related='request_id.analyst_id', string='Analyst', readonly=True)
    analyst_phone = fields.Char(related='analyst_id.mobile_phone', string='Analyst Phone', readonly=True)
    analyst_email = fields.Char(related='analyst_id.work_email', string='Analyst Email', readonly=True)
    request_date = fields.Date(related='request_id.request_date', string='Request Date', readonly=True)
    assignment_date = fields.Date(string='Assignment Date')
    reception_date = fields.Date(string='Reception Date', default=fields.Date.context_today)
    state = fields.Selection([
        ('entry', 'Entry to Workshop'),
        ('inspection', 'Inspection'),
        ('assign_mechanic', 'Assign Mechanic'),
        ('in_repair', 'In Repair'),
        ('repaired', 'Repaired')
    ], string='Status', default='entry')

    fault_description = fields.Text(string='Fault Description', related='request_id.fault_description', readonly=True)
    mechanic_id = fields.Many2one('hr.employee', string='Mechanic')
    odometer = fields.Float(string='Odometer')
    fuel_level = fields.Float(string='Fuel Level')
    diagnosis = fields.Text(string='Diagnosis')
    service_ids = fields.Many2many('product.product', string='Services')
    image_ids = fields.One2many('ir.attachment', 'res_id', domain=[('res_model', '=', 'fleet.workshop.order')], string='Service Images')
    verification_notes = fields.Text(string='Verification Notes')
    picking_ids = fields.Many2many('stock.picking', string='Pickings')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('fleet.workshop.order') or _('New')
        result = super(FleetWorkshopOrder, self).create(vals)
        return result
