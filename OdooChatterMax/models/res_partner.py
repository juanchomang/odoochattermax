# Copyright 2025 Juanchomang
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from odoo import models
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _message_get_domain(self):
        """
        Extend the domain for mail.messages to include chatter from related contacts
        (child_ids) when the current partner is a company.
        """
        self.ensure_one()

        _logger.debug("[OdooChatterMax] Entered _message_get_domain() for partner ID %s", self.id)

        base_domain = super()._message_get_domain()

        if self.is_company and self.child_ids:
            child_ids = self.child_ids.ids
            _logger.debug(
                "[OdooChatterMax] Extending chatter for company partner ID %s to include child_ids: %s",
                self.id, child_ids
            )

            child_domain = [
                ("model", "=", "res.partner"),
                ("res_id", "in", child_ids),
            ]

            return expression.OR([base_domain, child_domain])

        return base_domain
