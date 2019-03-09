# -*- encoding: utf-8 -*-

from openerp.osv import orm, fields


class EventEvent(orm.Model):
    _inherit = 'event.event'

    def _task_count(
        self,  ids, field_name, arg, context=None
    ):
        res = {}
        for event in self.browse(
             ids, context=context
        ):
            res[event.id] = len(event.task_ids)
        return res

    project_id = fields.Many2one('project.project', 'Project')
    task_count = fields.Integer(compute='_task_count', string='Tasks')
    task_ids = fields.Many2many('project.task', 'rel_task_event', 'event_id', 'task_id', 'Tasks')

    def agenda_description(
        self,  ids, context=None
    ):
        if context is None:
            context = {}

        for event in self.browse(
             ids, context=context
        ):
            if event.task_count > 0:
                agenda = "<p><strong>Agenda:</strong></p>\n<ul>\n"
                for task in event.task_ids:
                    agenda += "<li>" + task.name + "</li>\n"
                agenda += "</ul>\n"

                self.write( event.id,
                           {'description': (event.description or '') + agenda},
                           context=context)
        return True
