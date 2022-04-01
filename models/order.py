from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Order(models.Model):
    _name = 'dessert.order'
    _description = 'Order List'

    orderpackagedetail_ids = fields.One2many(
        comodel_name='dessert.order_packagedetail',
        inverse_name='order_id',
        string='Order Package Detail')
    
    orderwafflesdetail_ids = fields.One2many(
        comodel_name='dessert.order_wafflesdetail',
        inverse_name='orderw_id',
        string='Order Waffles Detail')

    
    name = fields.Char(string='Order Code', required=True)
    order_date = fields.Datetime(string='Order Date', default=fields.Datetime.now())
    cust = fields.Many2one(
        comodel_name='res.partner', 
        string='Customer Name', 
        domain=[('radiant_customer', '=', True)],
        store=True)
    
    
    
    total = fields.Integer(compute='_compute_total', string='Total Price', store=True)
    
    @api.depends('orderpackagedetail_ids', 'orderwafflesdetail_ids')
    def _compute_total(self):
        for record in self:
           a = sum(self.env['dessert.order_packagedetail'].search([('order_id', '=', record.id)]).mapped('total_price'))
           b = sum(self.env['dessert.order_wafflesdetail'].search([('orderw_id', '=', record.id)]).mapped('total_price'))
           record.total = a + b

    already_paid = fields.Boolean(string='Already Paid', default=False)
    
    def invoice(self):
        invoices = self.env['account.move'].create({
            'move_type': 'out_invoice',  
            'partner_id': self.cust,
            'invoice_date': self.order_date,
            'date': fields.Datetime.now(),
            'invoice_line_ids': [(0, 0, {
                'product_id': 0,
                'name' :'xxx' ,
                'quantity': 1,
                'name': 'product test 1',
                'discount': 0,
                'price_unit': self.total,
                'price_subtotal': self.total,
            })]            
        })
        self.already_paid=True
        return invoices  
    
    

class OrderPackageDetail(models.Model):
    _name = 'dessert.order_packagedetail'
    _description = 'New Description'
    
    order_id = fields.Many2one(comodel_name='dessert.order', string='Package Order')
    package_id = fields.Many2one(comodel_name='dessert.package', string='Package')
    
    name = fields.Selection(string='Name', selection=[('package', 'Package'),('waffles', 'Waffles'),('icecream', 'Ice Cream')])
    price_pcs = fields.Integer(compute='_compute_price_pcs', string='Price / Pcs')
    
    @api.depends('package_id')
    def _compute_price_pcs(self):
        for record in (self):
            record.price_pcs = record.package_id.price 
    
    qty = fields.Integer(string='Quantity')
    
    total_price = fields.Integer(compute='_compute_total_price', string='Total Price')
    
    @api.depends('qty', 'price_pcs')
    def _compute_total_price(self):
        for record in self:
            record.total_price= record.price_pcs * record.qty 


    @api.model
    def create(self,vals):
        record = super(OrderPackageDetail, self).create(vals)
        if record.qty:
            self.env['dessert.package'].search([('id', '=', record.package_id.id)]).write({'stock':record.package_id.stock - record.qty})
            return record


class OrderWafflesDetail(models.Model):
    _name = 'dessert.order_wafflesdetail'
    _description = 'New Description'
    
    orderw_id = fields.Many2one(comodel_name='dessert.order', string='Order Waffles')
    waffles_id = fields.Many2one(
        comodel_name='dessert.waffles',
        string='waffles',
        domain=[('stock', '>', 100)])
    
    
    name = fields.Selection(string='Name', selection=[('package', 'Package'),('waffles', 'Waffles'),('icecream', 'Ice Cream')]) 
    price_pcs = fields.Integer(compute='_compute_price_pcs', string='Price / Pcs')
    
    @api.depends('waffles_id')
    def _compute_price_pcs(self):
        for record in (self):
            record.price_pcs = record.waffles_id.price 
    
    qty = fields.Integer(string='Quantity')
    
    @api.constrains('qty')
    def _check_qty(self):
        for record in self:
            stock = self.env['dessert.waffles'].search([('stock', '<', record.qty), ('id', '!=',record.id)])
            if stock:
                raise ValidationError("Sorry, only %s pieces left in Stock. Please order less than the Stock." % record.waffles_id.stock)
            
    total_price = fields.Integer(compute='_compute_total_price', string='Total Price')
    
    @api.depends('qty', 'price_pcs')
    def _compute_total_price(self):
        for record in self:
            record.total_price= record.price_pcs * record.qty 


    @api.model
    def create(self,vals):
        record = super(OrderWafflesDetail, self).create(vals)
        if record.qty:
            self.env['dessert.waffles'].search([('id', '=', record.waffles_id.id)]).write({'stock':record.waffles_id.stock - record.qty})
            return record

