from odoo import api, fields, models

class Payment(models.Model):
    _name = 'dessert.payment'
    _description = 'Every order will be pay with this model'

    # name = fields.Char(string='Payment')
    name = fields.Char(compute='_compute_name', string='Customer Name')
    order_id = fields.Many2one(comodel_name='dessert.order', string='Order Id', required=True)
    
    @api.depends('order_id')
    def _compute_name(self):
        for record in self:
            record.name = self.env['dessert.order'].search([('id', '=', record.order_id.id)]).mapped('cust').name
    
    date_pay = fields.Date(string='Date Payment',default=fields.Date.today())
        
    bill = fields.Char(compute='_compute_bill', string='Bill')
    
    @api.depends('order_id')
    def _compute_bill(self):
        for record in self:
            record.bill = record.order_id.total
            
            
    @api.model
    def create(self,vals):
        record = super(Payment, self).create(vals)
        if record.date_pay:
            self.env['dessert.order'].search([('id', '=', record.order_id.id)]).write({'already_paid':True})
            self.env['dessert.accounting'].create({'credit': record.bill, 'name': record.name})
            return record
        
    def unlink(self):
        for unchecklist in self:
            self.env['dessert.order'].search([('id', '=', unchecklist.order_id.id)]).write({'already_paid':False})
        record = super(Payment, self).unlink()
    
    
