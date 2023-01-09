# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

#Registro de materias
class subject_class(models.Model):
	_name = 'subject.class'
	_inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
	_description = 'Materias'

	name = fields.Char(string='Nombre', tracking=True)
	code = fields.Char(string='Codigo', tracking=True)
	school_period_id = fields.Many2one(comodel_name='school.period', string='Periodo', required=True, tracking=True)

# periodos escolares
class school_period(models.Model):
	_name = 'school.period'
	_inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
	_description = 'Periodo escolar'

	name = fields.Char(string='Nombre', tracking=True)
