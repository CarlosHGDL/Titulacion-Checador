# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

#Clase Plantel
class campuses_class(models.Model):
	_name = 'campuses.class'
	_inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
	_description = 'Plantel'

	name = fields.Char()
	code = fields.Char()
	classroom_id = fields.One2many(comodel_name='classroom.class', inverse_name='campuses_id', string='Aula', track_visibility='always')
