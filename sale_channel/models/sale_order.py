from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sale_channel_id = fields.Many2one(comodel_name="sale.channel", required=True)

    warehouse_id = fields.Many2one(
        comodel_name="stock.warehouse", related="sale_channel_id.warehouse_id"
    )
    # if channel warehouse is not required this will fail

    def _prepare_invoice(self):
        res = super()._prepare_invoice()
        if self.sale_channel_id.journal_id:
            res["journal_id"] = self.sale_channel_id.journal_id.id
            res["sale_channel_id"] = self.sale_channel_id.id
        return res
