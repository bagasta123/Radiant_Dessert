from odoo import http, fields, models
from odoo.http import request
import json

class WafflesCon(http.Controller):
    @http.route(['/waffles','/waffles/<int:theid>'], auth='public', methods=['GET'], csrf=True)
    def getWaffles(self, theid=None, **kwargs):
        result = []
        if not theid:
            waffles = request.env['dessert.waffles'].search([])
            for w in waffles:
                result.append({"id" : w.id,
                            "Waffles Name" : w.name,
                            "Type" : w.type,
                            "Stock" : w.stock, 
                            "Price" : w.price})
        
            return json.dumps(result)
        else:
            wafflesid = request.env['dessert.waffles'].search([('id','=',theid)])
            for w in wafflesid:
                result.append({"id" : w.id,
                            "Waffles Name" : w.name,
                            "Type" : w.type,
                            "Stock" : w.stock, 
                            "Price" : w.price})
            return json.dumps(result)
        
    @http.route('/createwaffles',auth='user', type='json', methods=['POST'])
    def createWaffles(self, **kw):    
        if request.jsonrequest:    
            if kw['name']:
                vals={
                    'name': kw['name'], 
                    'type' : kw['type'],
                    'stock' : kw['stock'],
                    'price' : kw['price'],
                }
                newwaffle = request.env['dessert.waffles'].create(vals)
                args = {'success': True, 'ID':newwaffle.id}
                return args