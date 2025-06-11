from odoo import models, fields, api

class RepairLine(models.Model):
    _inherit = 'repair.line'

    discount = fields.Float(string='Discount (%)', digits='Discount', default=0.0)

    @api.depends('price_unit', 'product_uom_qty', 'discount', 'tax_id')
    def _compute_price_subtotal(self):
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(
                price,
                line.repair_id.pricelist_id.currency_id,
                line.product_uom_qty,
                line.product_id,
                line.repair_id.partner_id
            )
            line.price_subtotal = taxes['total_excluded']

    @api.depends('price_unit', 'product_uom_qty', 'discount', 'tax_id')
    def _compute_price_total(self):
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(
                price,
                line.repair_id.pricelist_id.currency_id,
                line.product_uom_qty,
                line.product_id,
                line.repair_id.partner_id
            )
            line.price_total = taxes['total_included']

class RepairFee(models.Model):
    _inherit = 'repair.fee'

    discount = fields.Float(string='Discount (%)', digits='Discount', default=0.0)

    @api.depends('price_unit', 'product_uom_qty', 'discount', 'tax_id')
    def _compute_price_subtotal(self):
        for fee in self:
            price = fee.price_unit * (1 - (fee.discount or 0.0) / 100.0)
            taxes = fee.tax_id.compute_all(
                price,
                fee.repair_id.pricelist_id.currency_id,
                fee.product_uom_qty,
                fee.product_id,
                fee.repair_id.partner_id
            )
            fee.price_subtotal = taxes['total_excluded']

    @api.depends('price_unit', 'product_uom_qty', 'discount', 'tax_id')
    def _compute_price_total(self):
        for fee in self:
            price = fee.price_unit * (1 - (fee.discount or 0.0) / 100.0)
            taxes = fee.tax_id.compute_all(
                price,
                fee.repair_id.pricelist_id.currency_id,
                fee.product_uom_qty,
                fee.product_id,
                fee.repair_id.partner_id
            )
            fee.price_total = taxes['total_included']

class RepairOrder(models.Model):
    _inherit = 'repair.order'

    @api.depends('operations.price_unit', 'operations.product_uom_qty', 'operations.product_id', 'operations.discount',
                 'fees_lines.price_unit', 'fees_lines.product_uom_qty', 'fees_lines.product_id', 'fees_lines.discount',
                 'pricelist_id.currency_id', 'partner_id')
    def _amount_tax(self):
        for order in self:
            val = 0.0
            # Parts (operations)
            for operation in order.operations:
                if operation.tax_id:
                    price = operation.price_unit * (1 - (operation.discount or 0.0) / 100.0)
                    tax_calculate = operation.tax_id.compute_all(
                        price,
                        order.pricelist_id.currency_id,
                        operation.product_uom_qty,
                        operation.product_id,
                        order.partner_id
                    )
                    for c in tax_calculate['taxes']:
                        val += c['amount']
            # Operations (fees_lines)
            for fee in order.fees_lines:
                if fee.tax_id:
                    price = fee.price_unit * (1 - (fee.discount or 0.0) / 100.0)
                    tax_calculate = fee.tax_id.compute_all(
                        price,
                        order.pricelist_id.currency_id,
                        fee.product_uom_qty,
                        fee.product_id,
                        order.partner_id
                    )
                    for c in tax_calculate['taxes']:
                        val += c['amount']
            order.amount_tax = val