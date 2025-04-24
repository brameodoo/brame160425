{
    'name': 'Fleet Workshop Management',
    'version': '1.0',
    'summary': 'Manage internal workshop for vehicle fleet',
    'description': 'Module to manage workshop requests and work orders for a vehicle fleet.',
    'category': 'Fleet',
    'author': 'Grupo Brame',
    'depends': ['fleet', 'hr', 'stock'],
    'data': [
        'views/fleet_workshop_views.xml',
        'views/fleet_workshop_templates.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}
