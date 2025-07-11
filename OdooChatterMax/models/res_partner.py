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

MORE TESTING
============
odoo-bin shell

partner = env['res.partner'].search([('is_company', '=', True)], limit=1)
domain = partner._message_fetch_domain()
env['mail.message'].search(domain).mapped('body')

env['mail.message'].search(domain).mapped('subject')
[(m.model, m.res_id, m.subject) for m in env['mail.message'].search(domain)]


AND MORE TESTING
================
odoo-bin shell

partner = env['res.partner'].search([('id', '=', 15)], limit=1)
partner.has_message

TEST2
domain = partner._message_fetch_domain()
env['mail.message'].search(domain).mapped('body')


"""

from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
# from odoo.addons.mail.models.mail_thread import MailThread
# from odoo.addons.mail.models.mail_thread import MailThread
from odoo.addons.mail.models.mail_thread import MailThread

# from odoo.addons.mail.models.mail_thread import MailThreadMixin
from ..utils.logging import log_debug_message

class ResPartner(models.Model):
    _inherit = 'res.partner'

    #message_ids = fields.One2many(
    #    comodel_name='mail.message',
    #    inverse_name='res_id',
    #    string='Messages',
    #    compute='_compute_message_ids',
    #    store=False,  # keep it transient
    #    recursive=True,
    #    domain="[('model', '=', 'res.partner')]"
    #)
    message_ids = fields.One2many(
        'mail.message', 'res_id',
        string='Messages',
        compute='_compute_custom_message_ids',
        store=False,
        help="Messages and communication history",
    )

    @api.depends()
    def _compute_custom_message_ids(self):
        for record in self:
            domain = record._message_fetch_domain()
            record.message_ids = self.env['mail.message'].search(domain)

    has_message = fields.Boolean(
        string='Has Message',
        compute='_compute_has_message',
        store=True,
        recursive=True,  # Resolves the warning you saw earlier
    )

    #@api.depends('message_ids')  # You could add more deps as needed
    #def _compute_has_message(self):
    #    for partner in self:
    #        message_domain = partner._message_fetch_domain()
    #        partner.has_message = bool(self.env['mail.message'].search_count(message_domain))

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

    def _message_fetch_domain(self, domain=None):
        self.ensure_one()
        log_debug_message(
            self.env,
            message=f"[OdooChatterMax] _message_fetch_domain triggered for partner ID {self.id}",
            path='res.partner',
            func='_message_fetch_domain',
        )
        partner_ids = [self.id]
        if self.is_company and self.child_ids:
            partner_ids += self.child_ids.ids
        return expression.AND([
            domain or [],
            [('model', '=', self._name), ('res_id', 'in', partner_ids)]
        ])

        # Walk MRO to get the *next* method (i.e. skip ResPartner)
        # for base in type(self).__mro__[1:]:
        #     method = base.__dict__.get('_message_fetch_domain')
        #     if method:
        #         base_domain = method(self, domain)
        #         break
        # else:
        #     raise AttributeError("_message_fetch_domain not found in MRO")


"""
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

        # Call the base method explicitly to avoid recursion
        # base_domain = MailThreadMixin._message_fetch_domain(self, domain)
        # base_domain = MailThread._message_fetch_domain(self, domain)


        if self.is_company and self.child_ids:
            child_ids = self.child_ids.ids

            log_debug_message(
                self.env,
                message=f"[OdooChatterMax] Adding children {child_ids} to domain",
                path='res.partner',
                func='_message_fetch_domain',
            )

            child_domain = [
                ("model", "=", "res.partner"),
                ("res_id", "in", child_ids),
            ]
            return expression.OR([base_domain, child_domain])

        return base_domain
"""
