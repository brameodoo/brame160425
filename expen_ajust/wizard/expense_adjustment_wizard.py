from odoo import models, fields, api

class ExpenseAdjustmentWizard(models.TransientModel):
    _name = 'expense.adjustment.wizard'
    _description = 'Asistente de Ajuste de Gastos'

    expense_id = fields.Many2one('hr.expense', string='Gasto')
    unverified_amount = fields.Float(string='Monto No Comprobado')

    def adjust_expense(self):
        self.ensure_one()
        if self.unverified_amount > 0:
            self.expense_id.write({
                'amount_total': self.expense_id.amount_total - self.unverified_amount,
                'unverified_amount': self.unverified_amount,
            })
