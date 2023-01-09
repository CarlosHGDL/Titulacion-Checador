# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


#Catálogo de colonias
class colony_catalog(models.Model):
	_name = 'colony.catalog'
	_description = 'Catálogo de colonias'

	name = fields.Char(string='Colonia')
	c_colony = fields.Char(string='codigo')
	c_postal_code = fields.Char(string='Codigo postal')