# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


#Catalogo de justificaciones
class justification_catalog(models.Model):
	_name = 'justification.catalog'
	_description = 'Catálogo de colonias'

	name = fields.Char(string='justificación')