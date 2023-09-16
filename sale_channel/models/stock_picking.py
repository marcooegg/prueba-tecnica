from odoo import models, fields, api, _


class StockPicking(models.Model):
    _inherit = "stock.picking"

    sale_channel_id = fields.Many2one(
        comodel_name="sale.channel",
        related="sale_id.sale_channel_id",
        store=True,
    )

