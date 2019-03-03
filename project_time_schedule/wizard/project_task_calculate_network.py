# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

# from lxml import etree
# import tools
# from openerp.tools.translate import _
from odoo import fields
from odoo.osv import osv


class project_task_calculate_network(osv.osv_memory):
    _name = 'project.task.calculate.network'
    _description = 'Schedule network'


    task_id= fields.Many2one('project.task', 'Target task')


    def default_get(self,  fields, context=None):
        """
        This function gets default values
        """
        res = super(project_task_calculate_network, self).default_get(
             fields, context=context)
        if context is None:
            context = {}
        record_id = context and context.get('active_id', False) or False

        res.update({'task_id': record_id})
        return res

    def calculate_network(self,  ids, context=None):
        if context is None:
            context = {}
        task_id = context.get('active_id', False)
        task_pool = self.pool.get('project.task')
        task_pool.calculate_network( [task_id], context=context)

        return {'type': 'ir.actions.act_window_close'}


