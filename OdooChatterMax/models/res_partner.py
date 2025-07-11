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

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression
from ..utils.logging import log_debug_message

class ResPartner(models.Model):
    _inherit = "res.partner"

    def _message_get_domain(self):

        self.ensure_one()

        log_debug_message(self.env, "Reached stage 2 logic for ticket #123")

        raise UserError(f"Entered _message_get_domain for partner ID {self.env}")

        base_domain = super()._message_get_domain()

        if self.is_company and self.child_ids:
            child_ids = self.child_ids.ids

            log_debug_message(env, "Reached stage 2 logic for ticket #123")

            child_domain = [
                ("model", "=", "res.partner"),
                ("res_id", "in", child_ids),
            ]

            return expression.OR([base_domain, child_domain])

        return base_domain