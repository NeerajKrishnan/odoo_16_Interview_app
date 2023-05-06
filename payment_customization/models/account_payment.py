from odoo import models, fields, api, _
from odoo.exceptions import MissingError, UserError, ValidationError, AccessError


class AccountPaymentDuePayment(models.Model):
    _name = 'account.payment.due.payment.line'
    payment_id = fields.Many2one('account.payment',
                                 string='Payment')
    invoice_id = fields.Many2one('account.move',string="Bill")
    currency_id = fields.Many2one('res.currency', related='invoice_id.currency_id')
    due_amount = fields.Monetary(string="due_amount",compute='_compute_due_total')
    amount_payment = fields.Monetary(string="Amount")
    payment_status = fields.Selection(related='invoice_id.payment_state')
    checked = fields.Boolean()

    @api.depends('invoice_id')
    def _compute_due_total(self):
        for rec in self:
            rec.due_amount = rec.invoice_id.amount_residual


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    due_payment_ids = fields.One2many(
        'account.payment.due.payment.line',
        'payment_id',
        string="Due Payment")

    due_difference = fields.Monetary(compute ='_compute_due_fields',store=True)

    def _compute_due_fields(self):
        for rec in self:
            rec.due_difference= rec.amount




    def action_due_payment_line(self):
            create_value =[(5,0,0)]
            invoices =  self.env['account.move'].search([('payment_state', 'in', ['not_paid','partial']),
                                                        ('partner_id', '=', self.partner_id.id)])

            for rec in invoices:
                create_value.append((0,0,{'invoice_id':rec.id}))
            self.write({'due_payment_ids':create_value})


    def action_to_makepayment(self):
        total_amount = 0
        if self.due_difference >= 0:
            for rec in self.due_payment_ids.filtered(lambda line: line.checked == True and
                                                                  line.invoice_id.payment_state in ['not_paid','partial'] ):
                total_amount = total_amount+rec.amount_payment


                if self.amount > total_amount:
                    payments = self.env['account.payment.register'].with_context(active_model='account.move',
                                                                                 active_ids=rec.invoice_id.id).create({
                        'amount': rec.amount_payment,
                        'group_payment': True,
                        'payment_difference_handling': 'open',
                        'currency_id': rec.currency_id.id,
                    })._create_payments()
                    self.due_difference = self.due_difference - total_amount
                else:
                    raise UserError(_("Please check the Amount has been Exceeded"))
        else:
            raise UserError(_("Please check the Amount has been Exceeded "))




