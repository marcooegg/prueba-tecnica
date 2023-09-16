# pylint: disable=missing-module-docstring,pointless-statement
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Channel",
    "summary": """
        Manage Sales by channels
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
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": ["base", "sale_stock", "account"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_channel.xml",
        "views/sale_order.xml",
        "views/stock_picking.xml",
        "views/account_move.xml",
    ],
    # only loaded in demo mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
