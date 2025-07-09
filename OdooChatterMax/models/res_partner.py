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

def _message_get_domain(self):
    """
    Extend the domain for mail.messages to include child contact messages
    when viewing a company contact.
    """
    self.ensure_one()
    domain = super()._message_get_domain()

    if self.is_company and self.child_ids:
        domain = expression.OR([
            domain,
            [('model', '=', 'res.partner'), ('res_id', 'in', self.child_ids.ids)],
        ])

    return domain

    def _message_fetch_domain(self, domain=None):
        """
        Extend the default chatter domain to include messages from related child contacts
        for company-type records in the chatter thread.
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

        # Combine the company's own messages with messages from child contacts
        combined_ids = companies.ids + related_contact_ids
        related_domain = [
            ("model", "=", "res.partner"),
            ("res_id", "in", combined_ids),
        ]

        # Use OR to include both the company's messages and child messages
        return expression.OR([base_domain, related_domain])

    def message_fetch(self, domain=None, limit=None, offset=0):
        """
        Override message_fetch to ensure messages from child_ids are included
        and sorted correctly in the chatter.
        """
        if self.is_company:
            # Fetch messages for the company and its child contacts
            combined_ids = self.ids + self.child_ids.ids
            extended_domain = expression.OR([
                domain or [],
                [("model", "=", "res.partner"), ("res_id", "in", combined_ids)]
            ])
            return self.env["mail.message"].search(
                extended_domain, limit=limit, offset=offset, order="date desc"
            )
        return super().message_fetch(domain=domain, limit=limit, offset=offset)