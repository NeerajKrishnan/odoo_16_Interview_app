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

    def action_due_payment_line(self):
        create_value =[(5,0,0)]
        invoices =  self.env['account.move'].search([('payment_state', 'in', ['not_paid','partial']),
                                                    ('partner_id', '=', self.partner_id.id)])

        for rec in invoices:
            create_value.append((0,0,{'invoice_id':rec.id}))
        print(create_value)
        # print(((0,0,create_value)))
        self.write({'due_payment_ids':create_value})
