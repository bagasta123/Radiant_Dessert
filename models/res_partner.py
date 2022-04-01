from odoo import api, fields, models

class Partner(models.Model):
    _inherit = 'res.partner'

    radiant_employee = fields.Boolean(string='Employee')
    radiant_customer = fields.Boolean(string='Customer')
    
