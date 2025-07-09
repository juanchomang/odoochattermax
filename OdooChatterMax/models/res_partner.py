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

from odoo import models
from odoo.osv import expression


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _message_fetch_domain(self, domain=None):
        """
        Extend the default chatter domain so that, for companies,
        messages on all linked individuals (child contacts) are included.
        """
        base_domain = super()._message_fetch_domain(domain)

        company_partners = self.filtered(lambda p: p.company_type == "company")
        if not company_partners:
            return base_domain

        child_ids = company_partners.mapped("child_ids").ids
        if not child_ids:
            return base_domain

        child_domain = [
            ("model", "=", "res.partner"),
            ("res_id", "in", child_ids),
        ]

        return expression.OR([base_domain, child_domain])
