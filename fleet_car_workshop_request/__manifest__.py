# -*- coding: utf-8 -*-
{
    'name': "Taller Mecánico Interno",

    'summary': """
        Gestión de órdenes de trabajo para taller mecánico interno de flota.""",

    'description': """
        Módulo para registrar y seguir las reparaciones y mantenimientos
        realizados a la flota interna de vehículos.
        - Registro de Órdenes de Trabajo
        - Seguimiento de Estados
        - Registro de Servicios Realizados
        - Almacenamiento de Imágenes
        - Gestión de Distritos/Zonas de Taller
    """,

    'author': "Tu Nombre/Empresa",
    'website': "https://www.tuwebsite.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services/Fleet', # O una categoría más apropiada
    'version': '17.0.0', # Ajusta a tu versión de Odoo

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'mail'], # Añadido 'mail' para chatter, 'product' para service_check

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/workshop_district_views.xml',
        'views/car_workshop_views.xml',
        'views/taller_menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml', # Si creas datos de demostración
    ],
    'installable': True,
    'application': True, # Marcar como aplicación si es una app principal
    'auto_install': False,
    'license': 'LGPL-3', # O la licencia que prefieras
}
