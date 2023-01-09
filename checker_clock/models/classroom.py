# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import urllib.parse

#Clase Aula 
class classroom_class(models.Model):
	_name = 'classroom.class'
	_inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
	_description = 'Aula'

	name = fields.Char()
	code = fields.Char()
	url = fields.Char()
	campuses_id = fields.Many2one(comodel_name='campuses.class', string='Plantel')
	
	@api.model
	def create(self, vals):
		res =  super(classroom_class, self).create(vals)
		res.generate_url()
		return res

	def generate_url(self):
		base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
		base_url = base_url+"/teacher/form?clasclass=%s"%(self.id) #'/web?db=titulacion#cids=1&menu_id=105&action=146&model=clock.checker&view_type=form'
		self.url = base_url