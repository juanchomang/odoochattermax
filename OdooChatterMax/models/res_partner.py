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
odoo-bin shell

TEST 1
======
partner = env['res.partner'].search([('id', '=', 15)], limit=1)
partner.has_message

TEST 2
======
domain = partner._message_fetch_domain()
env['mail.message'].search(domain).mapped('body')




<sheet>
    ...
    <div class="oe_chatter">
        <field name="message_ids" widget="mail_thread"/>
    </div>
</sheet>


"""

from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
# from odoo.addons.mail.models.mail_thread import MailThread
# from odoo.addons.mail.models.mail_thread import MailThread

# from odoo.addons.mail.models.mail_thread import MailThreadMixin
from ..utils.logging import log_debug_message

class ResPartner(models.Model):
    # _inherit = 'res.partner'
    _inherit = ['res.partner', 'mail.thread']


    # message_ids = fields.One2many(
    #    comodel_name='mail.message',
    #    inverse_name='res_id',
    #    string='Messages',
    #    compute='_compute_message_ids',
    #    store=False,  # keep it transient
    #    recursive=True,
    #    domain="[('model', '=', 'res.partner')]"
    #)

    # message_ids = fields.One2many(
    #    'mail.message', 'res_id',
    #    string='Messages',
    #    compute='_compute_custom_message_ids',
    #    store=False,
    #    help="Messages and communication history",
    #)

    #@api.depends()
    #def _compute_custom_message_ids(self):
    #    for record in self:
    #        domain = record._message_fetch_domain()
    #        record.message_ids = self.env['mail.message'].search(domain)

    has_message = fields.Boolean(
        string='Has Message',
        compute='_compute_has_message',
        store=True,
        recursive=True,  # Resolves the warning you saw earlier
    )

    @api.depends('message_ids')  # You could add more deps as needed
    def _compute_has_message(self):
        for partner in self:
            message_domain = partner._message_fetch_domain()
            partner.has_message = bool(self.env['mail.message'].search_count(message_domain))

    @api.depends('child_ids.message_ids')
    def _compute_message_ids(self):
        for partner in self:
            if partner.is_company:
                child_ids = partner.child_ids.ids
                domain = [('model', '=', 'res.partner'), ('res_id', 'in', child_ids + [partner.id])]
                partner.message_ids = self.env['mail.message'].search(domain)
            else:
                partner.message_ids = self.env['mail.message'].search([
                    ('model', '=', 'res.partner'),
                    ('res_id', '=', partner.id)
                ])    


    def message_fetch(self, domain=None, limit=None):
        log_debug_message(self.env, f"message_fetch called on partner {self.id}", path='res.partner', func='message_fetch')
        return super().message_fetch(domain=domain, limit=limit)


    def _message_fetch_domain(self, domain=None):
        self.ensure_one()
        _logger.info("Custom _message_fetch_domain triggered for partner ID %s", self.id)
        partner_ids = [self.id]
        if self.is_company:
            partner_ids += self.child_ids.ids
        return expression.AND([
            domain or [],
            [('model', '=', self._name), ('res_id', 'in', partner_ids)]
        ])