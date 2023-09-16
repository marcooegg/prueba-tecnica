from odoo import models, fields


class AccountMove(models.Model):
    _inherit = "account.move"

    sale_channel_id = fields.Many2one(comodel_name="sale.channel")
    #TODO: this allows creation of invoices without a sale channel and/or skipping sale workflow
    # readonly=True?
