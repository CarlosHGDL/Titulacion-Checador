# -*- coding: utf-8 -*-
import pytz
from odoo import http, fields
from odoo.http import request
from datetime import datetime
from werkzeug.utils import redirect
from odoo.exceptions import UserError, ValidationError

class get_teacher_record(http.Controller):

    def time_get(self):
        tz = pytz.timezone('America/Mexico_City')
        date_time=datetime.now(tz)
        date=datetime.now(tz).date()
        date_t=date_time.strftime('%d-%m-%Y %H:%M %p')
        date_t2=date_time.strftime('%Y-%m-%d %H:%M:%S')
        hora = date_time.hour
        return (date_t2,date,date_t,hora)
    #class name clasclass
    @http.route('/teacher/form', type='http', auth="public", website=True)
    def partner_form(self, **post):
        if 'clasclass' in request.params:
            classroom_class = request.params['clasclass']
            classroom_id = http.request.env['classroom.class'].sudo().search([('id','=', classroom_class )])
            return http.request.render("checker_clock.register_checker", {'classroom_class':classroom_id.name})
        else:
            return http.request.render("checker_clock.template_qr_error")

    @http.route('/teacher/form/submit',auth='public',type='http',website=True)
    def attendance_record(self,**post):
        values = {}
        for field_name, field_value in post.items():
            values[field_name] = field_value
        teacher_id = http.request.env['res.partner'].sudo().search([('tuition','=', values['tuition'] )])
        if not teacher_id:
            return http.request.render('checker_clock.tmp_customer_form_fail', {'mensage': 'La matricula no existe','flag':'no', 'aula':values['aula']})
            #raise UserError("Matricula incorecta")#http.request. FIXME
        tz = pytz.timezone('America/Mexico_City')
        date_time=datetime.now(tz)
        date=datetime.now(tz).date()
        date_t=date_time.strftime('%d-%m-%Y %H:%M %p')
        hora = date_time.hour
        schedule_class_id = http.request.env['schedule.class'].sudo().search([('date','=',date),('teacher_id','=',teacher_id.id),('hour_entry','<',hora+1),('hour_entry','>=',hora)])
        clock_checker_id = http.request.env['clock.checker']
        message = f'Asistencia de {schedule_class_id.subject_id.name} horario de {clock_checker_id.float_a_time(schedule_class_id.hour_entry)} a {clock_checker_id.float_a_time(schedule_class_id.hour_exit)}'
        if schedule_class_id:
            line = http.request.env['clock.checker'].create({
                'name' : f'Registro {teacher_id.name} [{date_t}]',
                'message' : message,
                'teacher_id' : teacher_id.id,
                'tuition' : teacher_id.tuition,
                'date_Time' : datetime.now(),
                'schedule_class_id' : schedule_class_id.id,
            })
            schedule_class_id.sudo().update({'clock_entry_id': line.id})
            return http.request.render("checker_clock.tmp_customer_form_success", {'line': line})
        else:
            return http.request.render('checker_clock.tmp_customer_form_fail', {'mensage': 'No se encontró horario','teacher_id':teacher_id,'aula':values['aula']})

    @http.route('/teacher/form/fail',auth='public',type='http',website=True)
    def error_step(self,**post):
        values = {}
        for field_name, field_value in post.items():
            values[field_name] = field_value
        if values['option'] == 'attempt':
            return http.request.render('checker_clock.register_checker', {'classroom_class':values['aula']})
        if values['option'] == 'create':
            if values['aula']:
                aula = values['aula']
            teacher_id = http.request.env['res.partner'].sudo().search([('tuition','=', values['tuition'] )])
            date_time,date,date_t,hora = self.time_get()
            line = http.request.env['clock.checker'].create({
                'name' : f'Registro {teacher_id.name} [{date_t}]',
                'message' : f'Registro sin horario favor de justificar aula {aula}',
                'teacher_id' : teacher_id.id,
                'tuition' : teacher_id.tuition,
                'date_Time' : datetime.now(),
            })

            return http.request.render("checker_clock.tmp_customer_form_success", {'line': line})