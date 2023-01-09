# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


#Registro de maestros teacher
class teacher_class(models.Model):
	_name = 'res.partner'
	_inherit = 'res.partner'

	is_teacher = fields.Boolean(string='Docente', default=True)
	colony_id = fields.Many2one(comodel_name='colony.catalog', string='Colonia', required=True)
	city = fields.Char(related='colony_id.name')
	tuition = fields.Char(string='Matrícula')