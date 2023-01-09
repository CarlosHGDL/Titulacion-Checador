# -*- coding: utf-8 -*-

import pytz
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

#Clase Regisro de asistencia 
class clock_checker(models.Model):
	_name = 'clock.checker'
	_inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
	_description = 'Reloj Checador'

	name = fields.Char()
	message = fields.Char()
	teacher_id = fields.Many2one(comodel_name='res.partner', string='Docente', domain="[('is_teacher', '=', True)]", tracking=True)
	date_Time = fields.Datetime(string='Fecha y hora')
	tuition = fields.Char(string='Matrícula')
	schedule_class_id = fields.Many2one(comodel_name='schedule.class', string='Horario')
	
	def float_a_time(self,dato):
		dato = dato*60
		hora = int(dato // 60)
		minutos = int(dato - (hora * 60))
		if minutos < 10:
			return f'{hora}:0{minutos}'
		return f'{hora}:{minutos}'