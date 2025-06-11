from odoo import models, fields, api

class RepairLine(models.Model):
    _inherit = 'repair.line'

    discount = fields.Float(string='Discount (%)', default=0.0)

    @api.depends('product_id', 'quantity', 'discount', 'price_unit', 'tax_id')
    def _compute_price_subtotal(self):
        for line in self:
            # Use price_unit instead of product_id.lst_price for correct pricing
            price_subtotal = line.price_unit * line.quantity
            discount_amount = (line.discount or 0.0) / 100.0
            discounted_subtotal = price_subtotal * (1 - discount_amount)
            taxes = line.tax_id.compute_all(discounted_subtotal, line.order_id.pricelist_id.currency_id, 1, product=line.product_id, partner=line.order_id.partner_id) if line.tax_id else {'total_included': discounted_subtotal}
            line.price_subtotal = discounted_subtotal
            line.price_total = taxes['total_included']