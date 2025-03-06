from odoo import models, fields, api, _
import datetime
from odoo.exceptions import ValidationError, UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_end_customer = fields.Boolean('End Customer', default=False)
    middle_rate_applicable = fields.Boolean('Middle Rate Applicable', default=False)
    br_number = fields.Char(string="BR Number", required=False)
    svat_no = fields.Char(string="SVAT #")

    # # Customer name validation to eliminating create a duplicates
    # @api.constrains('name', 'br_number')
    # def _check_customer_uniqueness(self):
    #     """
    #     Ensure that no duplicate customers exist based on name and BR number within the same company.
    #
    #     This method checks for uniqueness of the customer based on the following criteria:
    #     - For companies: uniqueness of BR number or name within the same company.
    #     - For individuals: uniqueness of name under the same parent and company.
    #
    #     Raises:
    #         UserError: If a duplicate company is found based on BR number or name.
    #         ValidationError: If a duplicate person is found based on name.
    #     """
    #     for rec in self:
    #         if rec.company_type == 'company':
    #             # Check for duplicate BR number within the same company
    #             if rec.br_number:
    #                 br_number_count = self.env['res.partner'].search_count([
    #                     ('br_number', '=', rec.br_number),
    #                     ('company_id', '=', rec.company_id.id)
    #                 ])
    #                 if br_number_count > 1:
    #                     raise UserError(_("A company with this BR number already exists under this company!"))
    #
    #             # Check for duplicate name within the same company
    #             elif rec.name:
    #                 name_count = self.env['res.partner'].search_count([
    #                     ('name', '=', rec.name),
    #                     ('company_id', '=', rec.company_id.id)
    #                 ])
    #                 if name_count > 1:
    #                     raise UserError(_("A company with this name already exists under this company!"))
    #
    #         else:
    #             # Check for duplicate name under the same parent and company for individuals
    #             if rec.name:
    #                 name_count = self.env['res.partner'].search_count([
    #                     ('name', '=', rec.name),
    #                     ('parent_id', '=', rec.parent_id.id),
    #                     ('company_id', '=', rec.company_id.id)
    #                 ])
    #                 if name_count > 1:
    #                     raise ValidationError(_("This person already exists under this company!"))