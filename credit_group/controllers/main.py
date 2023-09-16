from odoo.http import Controller, route, request
from odoo.exceptions import UserError
from odoo import SUPERUSER_ID, _
import logging
_logger = logging.getLogger(__name__)

mock_data = {
    "params": {
        "grupo_creditos": [
            {
                "name": "Grupo de Creditos 1",
                "codigo": "GC1",
                "canal": "Canal 1",
                "credito_global": 150000,
            },
            {
                "name": "Grupo de Creditos 2",
                "codigo": "GC2",
                "canal": "Canal 2",
                "credito_global": 150000,
            },
        ]
    }
}


class CreditGroupController(Controller):
    _name = "credit.group.controller"

    @route("/credit_group", auth="none", methods=["POST"], type="json")
    def create_credit_group(self, **kwargs):
        ctx = request.env.context.copy()
        ctx.update({"lang": "es_AR"})
        request.env.context = ctx
        try:
            for credit_group_info in kwargs.get("grupo_creditos"):
                credit_group_id = self.handle_credit_group(credit_group_info)
                _logger.info(f"{credit_group_id} succesfully created/updated")
        except Exception as ex:
            _logger.error(f"[API] Error creating/updating credit group: {ex}")
            return {"status": "400", "message": str(ex)}

        return {"status": "200", "message": "OK"}

    def handle_credit_group(self, credit_group_info):
        try:
            credit_group_code = credit_group_info["codigo"]
            credit_group_id = self._get_credit_group(credit_group_code)
            if credit_group_id:
                credit_group_id.update(
                    {
                        "name": credit_group_info["name"],
                        "sale_channel_id": self._find_sale_channel(credit_group_info["canal"]),
                        "global_credit": credit_group_info["credito_global"],
                    }
                )
            else:
                credit_group_id = (
                    request.env["credit.group"]
                    .with_user(SUPERUSER_ID)
                    .create(
                        {
                            "name": credit_group_info["name"],
                            "code": credit_group_info["codigo"],
                            "sale_channel_id": self._find_sale_channel(credit_group_info["canal"]),
                            "global_credit": credit_group_info["credito_global"],
                        }
                    )
                )
            return credit_group_id
        except KeyError as key_error:
            raise UserError(_("Missing info in request: %s") % key_error)
        except Exception as ex:
            raise ex

    def _get_credit_group(self, code):
        return request.env["credit.group"].with_user(SUPERUSER_ID).search([("code", "=", code)])

    def _find_sale_channel(self, code):
        sale_channel_id = (
            request.env["sale.channel"].with_user(SUPERUSER_ID).search([("code", "=", code)])
        )
        if not sale_channel_id:
            raise UserError(_("Sale Channel with code %s not found") % code)
