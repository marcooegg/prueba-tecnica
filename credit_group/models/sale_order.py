from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    credit = fields.Selection(
        selection=[
            ("no_limit", "No Limit"),
            ("available_credit", "Available Credit"),
            ("credit_blocked", "Credit Blocked"),
        ],
        default="no_limit",
        compute="_compute_credit",
        store=True,
    )

    company_currency_id = fields.Many2one(
        related="company_id.currency_id",
        string="Company currency",
    )

    amount_company_currency = fields.Monetary(
        currency_field="company_currency_id",
        string="Total",
        store=True,
        readonly=True,
        compute="_amount_all_company_currency",
    )

    @api.depends("currency_id", "amount_total")
    def _amount_all_company_currency(self):
        for order in self:
            order.amount_company_currency = order.currency_id._convert(
                order.amount_total,
                order.company_id.currency_id,
                order.company_id,
                order.date_order or fields.Date.today(),
            )

    @api.depends("partner_id", "sale_channel_id", "amount_company_currency")
    def _compute_credit(self):
        matching_group_id = self.partner_id.credit_group_ids.filtered(
            lambda credit_group: credit_group.sale_channel_id == self.sale_channel_id
        )
        if matching_group_id:
            if matching_group_id.available_credit >= self.amount_total:
                self.credit = "available_credit"
            else:
                self.credit = "credit_blocked"
        else:
            self.credit = "no_limit"

    def action_confirm(self):
        for record in self:
            if record.credit == "credit_blocked":
                raise ValidationError("Credit Blocked")
        return super().action_confirm()
