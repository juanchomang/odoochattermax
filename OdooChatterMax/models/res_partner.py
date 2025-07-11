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
"""
FAILED
======
odoo-bin shell
partner = env['res.partner'].search([('is_company', '=', True)], limit=1)
domain = partner._message_get_domain()

TESTING
=======
odoo-bin shell
partner = env['res.partner'].search([('is_company', '=', True)], limit=1)
domain = partner._message_fetch_domain()


sorted(set(dir(env['res.partner'])))

sorted(set(dir(env['odoo.addons.mail.models.mail_thread'])))


"""

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression
from odoo.addons.mail.models.mail_thread import MailThread
from ..utils.logging import log_debug_message

class ResPartner(models.Model):
    _inherit = "res.partner"

    def _message_fetch_domain(self, domain=None):
        self.ensure_one()

        log_debug_message(
            self.env,
            message=f"[OdooChatterMax] _message_fetch_domain triggered for partner ID {self.id}",
            path='res.partner',
            func='_message_fetch_domain',
        )

        # Call mixin's method explicitly since super() fails
        base_domain = MailThread._message_fetch_domain(self, domain)

        if self.is_company and self.child_ids:
            child_ids = self.child_ids.ids

            log_debug_message(
                self.env,
                message=f"[OdooChatterMax] Including child_ids in chatter: {child_ids}",
                path='res.partner',
                func='_message_fetch_domain',
            )

            child_domain = [
                ("model", "=", "res.partner"),
                ("res_id", "in", child_ids),
            ]

            return expression.OR([base_domain, child_domain])

        return base_domain