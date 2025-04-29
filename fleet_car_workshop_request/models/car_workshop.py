# -*- coding: utf-8 -*-
from odoo import models, fields, api, _ # Asegúrate de importar api y _

class CarWorkshop(models.Model):
    _name = 'car.workshop'
    _description = 'Orden de Trabajo Taller Interno'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Añadir herencia si no estaba

    name = fields.Char(
        string='Referencia',
        required=True,
        copy=False,
        readonly=True,
        index=True, # Buen índice para búsquedas
        default=lambda self: _('Nuevo') # Mantener 'Nuevo' como valor temporal
    )
    license_plate = fields.Char(string='Matrícula')
    workshop_district_id = fields.Many2one('workshop.district', string='Distrito Taller')
    vehicle_description = fields.Text(string='Descripción del Vehículo/Equipo')
    customer_notes = fields.Text(string='Notas del Cliente/Solicitante')
    technician_notes = fields.Text(string='Notas del Técnico')
    entry_date = fields.Datetime(string='Fecha de Entrada', default=fields.Datetime.now)
    departure_date = fields.Datetime(string='Fecha de Salida')
    responsible_id = fields.Many2one('res.users', string='Responsable', default=lambda self: self.env.user)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('in_progress', 'En Progreso'),
        ('ready', 'Listo para Entrega'),
        ('done', 'Realizado'),
        ('cancelled', 'Cancelado'),
    ], string='Estado', default='draft', tracking=True) # Tracking para el chatter
    image_ids = fields.One2many('car.workshop.image', 'workshop_id', string='Imágenes')
    service_check_ids = fields.One2many('car.workshop.service.check', 'workshop_id', string='Verificación de Servicios')

    # ---- INICIO: Código para la secuencia ----
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('Nuevo')) == _('Nuevo'):
                # Usamos el código que definimos en el XML
                vals['name'] = self.env['ir.sequence'].next_by_code('car.workshop.order.sequence') or _('Nuevo')
        return super(CarWorkshop, self).create(vals_list)
    # ---- FIN: Código para la secuencia ----

    # Aquí puedes añadir los métodos para los botones de estado si los necesitas
    # def action_confirm(self): ...
    # def action_start_progress(self): ...
    # ... etc ...

# Resto de tus clases (CarWorkshopImage, CarWorkshopServiceCheck, WorkshopDistrict)
# ... (Asegúrate de que estén aquí o importadas correctamente en __init__.py)