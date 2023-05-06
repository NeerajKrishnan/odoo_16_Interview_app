from odoo import models, fields, api, _


class AccountPaymentDuePayment(models.Model):
    _name = 'account.payment.due.payment.line'
    payment_id = fields.Many2one('account.payment',
                                 string='Payment')
    invoice_id = fields.Many2one('account.move',string="Bill")
    payment_status = fields.Selection(related='invoice_id.payment_state')
    checked = fields.Boolean()



class AccountPayment(models.Model):
    _inherit = 'account.payment'
    due_payment_ids = fields.One2many(
        'account.payment.due.payment.line',
        'payment_id',
        string="Due Payment")
