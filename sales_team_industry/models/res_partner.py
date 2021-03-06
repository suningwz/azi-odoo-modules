# -*- coding: utf-8 -*-
# Copyright 2014-2017 Scott Saunders
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class Partner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def write(self, vals):
        for record in self:
            require_industry = self.env['ir.config_parameter'].sudo().\
                get_param('sales_team_industry.require_industry')
            if (require_industry and not (
                    vals.get('parent_id') or
                    record.parent_id and
                    'parent_id' not in vals)):
                current_customer = 'customer' not in vals and \
                                   record.customer or vals.get('customer')
                if ((vals.get('customer') and not vals.get('industry_id')) or
                    (record.customer and 'customer' not in vals and not
                     record.industry_id and 'industry_id' not in vals)) or (
                        'industry_id' in vals and not
                        vals['industry_id'] and current_customer):
                    raise ValidationError(
                        _("Customers require a valid Industry."))
        return super(Partner, self).write(vals)

    @api.model
    def create(self, vals):
        if (self.env['ir.config_parameter'].sudo().get_param(
                'sales_team_industry.require_industry')
                and not vals.get('parent_id')):
            if vals.get('customer') and not vals.get('industry_id'):
                raise ValidationError(_("Customers require a valid Industry."))
        return super(Partner, self).create(vals)
