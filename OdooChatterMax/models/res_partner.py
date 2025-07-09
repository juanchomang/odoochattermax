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
        Extend the default chatter domain so that, for company-type contacts,
        messages from their related child contacts (e.g., employees, branches)
        are also included in the chatter thread.
        """
        base_domain = super()._message_fetch_domain(domain)

        # Only apply this logic to company-type records
        companies = self.filtered(lambda p: p.is_company)
        if not companies:
            return base_domain

        # Fetch all child_ids from company partners
        related_contact_ids = companies.mapped("child_ids").ids
        if not related_contact_ids:
            return base_domain

        # Add child partner messages to the domain
        related_domain = [
            ("model", "=", "res.partner"),
            ("res_id", "in", related_contact_ids),
        ]

        return expression.OR([base_domain, related_domain])

