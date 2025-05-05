from odoo import models, fields, api

class WorkshopRequest(models.Model):
    _name = 'fleet.car.workshop.request'
    _description = 'Workshop Request'

    name = fields.Char(string='Request Reference', required=True, copy=False, readonly=True,
                       default=lambda self: ('New'))
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle', required=True)
    employee_id = fields.Many2one('hr.employee', string='Requested By', required=True)
    request_date = fields.Date(string='Request Date', default=fields.Date.context_today)
    description = fields.Text(string='Description of Issue')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('fleet.car.workshop.request') or 'New'
        return super(WorkshopRequest, self).create(vals)