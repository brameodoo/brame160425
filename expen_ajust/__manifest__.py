{
    'name': 'Expense Adjustment',
    'version': '1.0',
    'summary': 'Module to adjust unverified expenses',
    'description': 'Allows users to adjust unverified expenses directly in the expense report.',
    'category': 'Accounting',
    'author': 'Tu Nombre',
    'depends': ['hr_expense'],
    'data': [
        'views/hr_expense_views.xml',
        'wizard/expense_adjustment_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
