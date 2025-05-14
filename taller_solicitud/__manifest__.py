{
    "name": "Solicitudes Taller Vehicular",
    "version": "1.0",
    "category": "Fleet Management",
    "summary": "Gestión de solicitudes de ingreso a taller mecánico de la flota vehicular",
    "description": "Módulo para registrar y gestionar solicitudes de ingreso al taller mecánico.",
    "author": "Tu Nombre o Empresa",
    "depends": ["base", "fleet", "hr", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "views/taller_solicitud_views.xml",
        "data/ir_sequence_data.xml"
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3"
}
