from odoo import models, fields, api


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    unverified_amount = fields.Float(string='Monto No Comprobado', readonly=True)

    def action_adjust_expense(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'expense.adjustment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_expense_id': self.id},
        }
