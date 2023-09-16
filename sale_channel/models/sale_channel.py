from odoo import models, fields, api, _


class SaleChannel(models.Model):
    _name = "sale.channel"
    _description = "Sale Channel"

    name = fields.Char(required=True)
    code = fields.Char(required=True, index=True)

    warehouse_id = fields.Many2one(comodel_name="stock.warehouse")
    journal_id = fields.Many2one(comodel_name="account.journal", domain=[("type", "=", "sale")])

    active = fields.Boolean(default=True)

    _sql_constraints = [
        ("code_uniq", "unique (code)", _("Code must be unique")),
    ]
