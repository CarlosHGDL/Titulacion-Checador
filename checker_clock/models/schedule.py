# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
from babel.dates import format_datetime, format_date

#Clase de horarios
class schedule_class(models.Model):
	_name = 'schedule.class'
	_inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
	_description = 'Horario'

	name = fields.Char(string='Horario', copy=False, compute='_compute_schedule_name')
	date = fields.Date(string='Fecha', help="Fecha del horario", required=True, tracking=True)
	date_tex = fields.Char(copy=False)
	hour_entry = fields.Float(string="Hora de entrada", help="Formato en 24 horas", tracking=True)#time
	hour_exit = fields.Float(string="Hora de salida", help="Formato en 24 horas", tracking=True)
	teacher_id = fields.Many2one(comodel_name='res.partner', string='Docente', domain="[('is_teacher', '=', True)]", required=True, tracking=True)
	subject_id = fields.Many2one(comodel_name='subject.class', string='Materia', required=True, tracking=True)
	clock_entry_id = fields.Many2one(comodel_name='clock.checker', string='Registro', tracking=True)
	clock_exit_id = fields.Many2one(comodel_name='clock.checker', string='Salida',  tracking=True)
	classroom_class_id = fields.Many2one(comodel_name='classroom.class', string='Salon',  tracking=True)
	observations = fields.Char(string='Observaciones', copy=False)
	justification_catalog_id = fields.Many2one(comodel_name='justification.catalog', string='Estado',  tracking=True)
	
	@api.model
	def create(self, vals):
		vals['date_tex'] = self.get_date_tex(vals['date'])
		return super(schedule_class, self).create(vals)

	def write(self, vals):
		if 'date' in vals:
			vals['date_tex'] = self.get_date_tex(vals['date'])
		return super(schedule_class, self).write(vals)

	def get_date_tex(self,fecha):
		days = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
		mes = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
		date = fields.Date.from_string(fecha),
		return f"{days[date[0].weekday()]} {date[0].day} de {mes[date[0].month-1]} del {date[0].year}"

	@api.depends('teacher_id','subject_id','date')
	def _compute_schedule_name(self):
		for record in self:
			record.name = f'{record.teacher_id.name} [{record.subject_id.name} {record.date}]'

	@api.onchange('hour_entry','hour_exit')
	@api.constrains('hour_entry','hour_exit')
	def date_onchange_entry_exit(self):
		for record in self:
			if record.hour_entry > 24.99 or record.hour_exit > 24.99:
				raise UserError('El valor maximo aceptado es de 24:59')
			if record.hour_entry < 0 or record.hour_exit < 0:
				raise UserError('No se aceptan valores negativos')

	@api.onchange('clock_entry_id')
	@api.depends('clock_entry_id','hour_entry')
	def sttate_onchange_clock_entry_id(self):
		for line in self:
			if line.clock_entry_id:
				minutos = line.hour_entry * 60

				schedule_hora = minutos // 60
				schedule_minutos = minutos % 60
				clock_hora = line.clock_entry_id.date_Time.hour
				clock_minutos = line.clock_entry_id.date_Time.minute
				
				diferencia_hora = clock_hora - schedule_hora
				diferencia_minutos = clock_minutos - schedule_minutos
				if diferencia_hora > 0:
					diferencia_minutos += diferencia_hora*60
				print('diferencia_hora ',diferencia_hora)
				print('diferencia_minutos ',diferencia_minutos)
				# estado_ids = self.env['justification.catalog'].search([('tolerance', '!=', 60.00)])
				# estado_id = estado_ids.search([('tolerance', '<=', diferencia_minutos)])
				# if len(estado_id) !=1:
				# 	estado = 0.00
				# 	for reg in estado_id:
				# 		if reg.tolerance > estado:
				# 			estado = reg.tolerance
				# 	print (estado)
				# 	line.justification_catalog_id = estado_id.search([('tolerance', '=', estado)],limit =1).id
				# else:
				# 	line.justification_catalog_id = estado_id.id

			