from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    credit_control = fields.Boolean()

    credit_group_ids = fields.Many2many(
        comodel_name="credit.group",
        string="Credit Groups",
        relation="credit_group_res_partner_rel",
    )
