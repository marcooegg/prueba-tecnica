# pylint: disable=missing-module-docstring,pointless-statement
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Credit Groups",
    "summary": """
        Manage partners debt through credit groups  
    """,
    "author": "Marco Gabriel Oegg",
    "maintainers": ["marcooegg"],
    "website": "https://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Sale",
    "version": "13.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "depends": ["base", "sale_channel"],
    ### XML Data files
    "data": [
        "security/ir.model.access.csv",
        "views/credit_group.xml",
        "views/res_partner.xml",
        "views/sale_order.xml",
        "report/credit_group_report_pdf.xml",
        "report/report_data.xml",
    ],
}
