from odoo import api, fields, models

class Accounting(models.Model):
    _name = 'dessert.accounting'
    _description = 'New Description'
    _order = 'id asc'

    name = fields.Char(string='Name')
    id_acc = fields.Char(string='Accounting Code')
    date = fields.Datetime(string='Date', default=fields.datetime.now())
    debit = fields.Integer(string='Debit')
    credit = fields.Integer(string='Credit')
    balance = fields.Float(compute='_compute_balance', string='Balance')
    
    @api.depends('debit', 'credit')
    def _compute_balance(self):
        for record in self:
            prev = self.search_read([('id', '<', record.id)],limit=1,order='date desc')
            prev_balance = prev[0]['balance'] if prev else 0
            record.balance = prev_balance + record.credit - record.debit