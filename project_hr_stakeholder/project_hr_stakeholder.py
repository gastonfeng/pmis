# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from openerp import tools
from openerp.osv import fields, orm

from odoo import api


class ProjectHrStakeholder(orm.Model):

    _name = "project.hr.stakeholder"
    _description = 'Project Stakeholder'

    def _roles_name_calc(self,  ids, name, args, context=None):
        if not ids:
            return []
        res = []

        stakeholders_br = self.browse( ids, context=context)

        for stakeholder in stakeholders_br:
            data = []
            stk_roles = stakeholder.role_ids
            if stk_roles:
                for stk_role in stk_roles:
                    data.insert(0, stk_role.name)
                data.sort(cmp=None, key=None, reverse=False)
                data_str = ', '.join(map(tools.ustr, data))

            else:
                data_str = ''

            res.append((stakeholder.id, data_str))

        return dict(res)

    def _responsibilities_name_calc(
            self,  ids, name, args, context=None):

        if not ids:
            return []
        res = []

        stakeholders_br = self.browse( ids, context=context)

        for stakeholder in stakeholders_br:
            data = []
            responsibilities = stakeholder.responsibility_ids
            if responsibilities:
                for responsibility in responsibilities:
                    data.insert(0, responsibility.name)
                data.sort(cmp=None, key=None, reverse=False)
                data_str = ', '.join(map(tools.ustr, data))

            else:
                data_str = ''

            res.append((stakeholder.id, data_str))

        return dict(res)

    name = fields.Char('Description', required=False, size=64)
    partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    project_id = fields.Many2one('project.project', 'Project', ondelete='cascade')
    role_ids = fields.Many2many('project.hr.role', 'stakeholder_role_rel', 'stakeholder_id', 'role_id', 'Roles',
            help="The assignment of the roles and responsibilities determines "
                 "what actions the project manager, project team member, or "
                 "individual contributor will have in the project. Roles and "
                 "responsibilities generally support the project scope since "
                 "this is the required work for the project."
        ),
    responsibility_ids = fields.Many2many('project.hr.responsibility', 'stakeholder_responsibility_rel',
                                          'stakeholder_id', 'responsibility_id', 'Responsibilities',
                                          help="The assignment of the roles and responsibilities determines "
                 "what actions the project manager, project team member, or "
                 "individual contributor will have in the project. Roles and "
                 "responsibilities generally support the project scope since "
                 "this is the required work for the project."
                                          ),
    roles_name_str = fields.Text(compute='_roles_name_calc', string='Roles', help='Project Stakeholder roles')
    responsibilities_name_str = fields.Text(compute='_responsibilities_name_calc', string='Responsibilities',
                                            help='Project Stakeholder responsibilities')

    influence = fields.Text('Influence')

    @api.multi
    def name_get(self):
        res = []
        for stakeholder in self:
            stakeholder_name = ""
            if stakeholder.partner_id:
                stakeholder_name = stakeholder.partner_id.name
            res.append((stakeholder.id, stakeholder_name))
        return res
