{
    'name': 'Taller Interno de Flota',
    'version': '1.0',
    'summary': 'Gestión de solicitudes y órdenes de trabajo para el taller interno de la flota vehicular.',
    'description': """
    Módulo para la gestión integral del taller interno de la flota vehicular,
    permitiendo la creación de solicitudes de servicio, la asignación de trabajo
    y el seguimiento de las reparaciones.
    """,
    'author': 'Brame telecom',
    'website': 'www.grupobrame.com',
    'license': 'LGPL-3',
    'depends': ['base', 'fleet', 'hr', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/fleet_workshop_request_views.xml',
        'views/fleet_workshop_order_views.xml',  # Agregamos las vistas de la orden
        'views/fleet_vehicle_views.xml',
        'data/fleet_workshop_request_sequence.xml',
        'data/fleet_workshop_order_sequence.xml',
        'data/mail_template_request_assigned.xml',  # Agrega la plantilla de solicitud asignada
        'data/mail_template_order_repaired.xml',    # Agrega la plantilla de orden reparada
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
