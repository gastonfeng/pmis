# -*- coding: utf-8 -*-
#    Copyright 2016 MATMOZ, Slovenia (Matjaž Mozetič)
#    Copyright 2018 EFICENT (Jordi Ballester Alomar)
#    Copyright 2018 LUXIM, Slovenia (Matjaž Mozetič)
#    Together as the Project Expert Team
#    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.exceptions import Warning
from odoo.tools.translate import _


class AnalyticDeliverablePlanCopyVersion(models.TransientModel):
    """
    For copying all the planned deliverables to a separate planning version
    """
    _name = "analytic.deliverable.plan.copy.version"
    _description = "Analytic Deliverable Plan copy versions"

    source_version_id = fields.Many2one(
        comodel_name='account.analytic.plan.version',
        string='Source Planning Version',
        required=True
    )
    dest_version_id = fields.Many2one(
        comodel_name='account.analytic.plan.version',
        string='Destination Planning Version',
        required=True
    )
    include_child = fields.Boolean(
        string='Include child accounts',
        default=True
    )

    @api.multi
    def analytic_deliverable_plan_copy_version_open_window(self):
        new_line_plan_ids = []
        analytic_obj = self.env['account.analytic.account']
        line_plan_obj = self.env['analytic.deliverable.plan.line']

        data = self[0]
        record_ids = self._context and self._context.get(
            'active_ids', False
        )
        active_model = self._context and self._context.get(
            'active_model', False
        )
        assert active_model == (
            'account.analytic.account',
            'Bad context propagation'
        )
        record = analytic_obj.browse(record_ids)
        include_child = (
            data.include_child if data and
            data.include_child else False
        )
        source_version = (
            data.source_version_id if data and
            data.source_version_id else False
        )
        dest_version = (
            data.dest_version_id if data and
            data.dest_version_id else False
        )
        if dest_version.default_plan:
            raise Warning(_('''It is prohibited to copy to the default
                planning version.'''))

        if source_version == dest_version:
            raise Warning(_('''Choose different source and destination
                planning versions.'''))
        if include_child:
            account_ids = record.get_child_accounts().keys()
        else:
            account_ids = record_ids

        line_plans = line_plan_obj.search(
            [
                ('account_id', 'in', account_ids),
                ('version_id', '=', source_version.id)
            ]
        )
        new_line_plan_rec = line_plan_obj
        for line_plan in line_plans:
            new_line_plan = line_plan.copy()
            new_line_plan_rec += new_line_plan
            new_line_plan_ids.append(new_line_plan.id)
        if new_line_plan_rec:
            new_line_plan_rec.write({'version_id': dest_version[0]})
        return {
            'domain': "[('id','in', [" + ','.join(
                map(str, new_line_plan_ids)
            ) + "])]",
            'name': _('Deliverable Plan Lines'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'analytic.deliverable.plan.line',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }
