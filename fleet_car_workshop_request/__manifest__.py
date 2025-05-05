{
    'name': 'Fleet Car Workshop Request',
    'version': '1.0',
    'category': 'Fleet',
    'summary': 'Internal Fleet Workshop Management',
    'depends': ['fleet', 'hr', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/workshop_views.xml',
        'report/workshop_reports.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}