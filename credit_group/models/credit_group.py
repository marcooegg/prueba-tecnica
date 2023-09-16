from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

class CreditGroup(models.Model):
    _name = "credit.group"
    _description = "Credit Group"

    name = fields.Char(required=True)
    code = fields.Char(required=True, index=True)

    sale_channel_id = fields.Many2one(comodel_name="sale.channel", required=True)

    company_id = fields.Many2one(
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.company,
    )
    currency_id = fields.Many2one(comodel_name="res.currency", related="company_id.currency_id")
    global_credit = fields.Monetary(currency_field="currency_id", required=True)
    used_credit = fields.Monetary(currency_field="currency_id", compute="_compute_used_credit")
    available_credit = fields.Monetary(
        currency_field="currency_id",
        compute="_compute_available_credit",
    )

    partner_ids = fields.Many2many(
        comodel_name="res.partner",
        string="Partners",
        relation="credit_group_res_partner_rel",
    )

    def _get_computable_credit_lines(self):
        """Get Computable Credit Lines"""
        sale_order_ids = self.env["sale.order"].search(
            [
                ("partner_id", "in", self.partner_ids.ids),
                ("sale_channel_id","=",self.sale_channel_id.id),
                ("invoice_status", "in", ["to invoice"]),
            ]
        )
        invoice_ids = self.env["account.move"].search(
            [
                #FIXME: 
                # ("state","=","posted"), 
                # if we check for 'state' and an SO is confirmed, invoiced but invoiced remains in draft state, 
                # it will be considered as available credit
                # which is why we need to check the invoice_payment_state and account for draft invoices
                # this does not seem correct 
                ("invoice_payment_state", "=", "not_paid"),
                ("sale_channel_id","=",self.sale_channel_id.id),
                ("type", "=", "out_invoice"),
                ("partner_id", "in", self.partner_ids.ids),
            ]
        )
        return sale_order_ids, invoice_ids

    @api.depends("sale_channel_id")
    def _compute_used_credit(self):
        """Compute Used Credit"""
        for record in self:
            sale_order_ids, invoice_ids = record._get_computable_credit_lines()
            record.used_credit = sum(sale_order_ids.mapped("amount_company_currency")) + sum(
                invoice_ids.line_ids.mapped("amount_residual")
            )

    @api.depends("global_credit", "used_credit")
    def _compute_available_credit(self):
        """Compute Available Credit"""
        for record in self:
            record.available_credit = record.global_credit - record.used_credit

    active = fields.Boolean(default=True)

    _sql_constraints = [
        ("code_uniq", "unique (code)", _("Code must be unique")),
    ]
