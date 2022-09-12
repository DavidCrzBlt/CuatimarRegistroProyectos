from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import *
import time
# import config
import os

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
# app.config['SECRET_KEY'] = config.SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

db=SQLAlchemy(app)

class Proyecto(db.Model):
   id_proyecto = db.Column('id_proyecto', db.Integer, primary_key=True)
   nombre_proyecto = db.Column(db.String(255), unique=True)
   status = db.Column(db.Boolean)
   ubicacion = db.Column(db.String(200))
   cliente = db.Column(db.String(200))
   trabajo_diario = db.Column(db.Boolean)
   empleados = db.relationship('Empleado',backref='proyecto')
   asistencias = db.relationship('Asistencia',backref='proyecto')
   pagos = db.relationship('Pago',backref='proyecto')
   
   def __repr__(self):
    return f'<Proyecto "{self.nombre_proyecto}">'

class Empleado(db.Model):
   id_empleado = db.Column('id_empleado', db.Integer, primary_key=True)
   clave_banco = db.Column(db.Integer,unique=True)
   nombre_empleado = db.Column(db.String(255),unique=True)
   salario_base = db.Column(db.Numeric)
   salario_base_IMSS = db.Column(db.Numeric)
   descuento_FONACOT = db.Column(db.Boolean)
   descuento_INFONAVIT = db.Column(db.Boolean)
   costo_he = db.Column(db.Numeric)
   status = db.Column(db.Boolean)
   id_proyecto = db.Column(db.Integer,db.ForeignKey('proyecto.id_proyecto'))
   asistencias = db.relationship('Asistencia',backref='empleado')
   pagos = db.relationship('Pago',backref='empleado')

   def __repr__(self):
    return f'<Nombre empleado "{self.nombre_empleado}">'

class Asistencia(db.Model):
   id_asistencia = db.Column('id_asistencia', db.Integer, primary_key=True)
   id_empleado = db.Column(db.Integer,db.ForeignKey('empleado.id_empleado'))
   horas_extras = db.Column(db.Integer)
   attendance = db.Column(db.Integer)
   day = db.Column(db.DateTime)
   id_proyecto = db.Column(db.Integer,db.ForeignKey('proyecto.id_proyecto'))

   def __repr__(self):
    return f'<ID empleado "{self.id_empleado}">'

class Pago(db.Model):
   id = db.Column('id_operacion', db.Integer, primary_key=True)
   fecha_operacion = db.Column(db.DateTime)
   id_movimiento = db.Column(db.Integer)
   id_proyecto = db.Column(db.Integer,db.ForeignKey('proyecto.id_proyecto'))
   id_empleado = db.Column(db.Integer,db.ForeignKey('empleado.id_empleado'))
   s_base = db.Column(db.Numeric)
   s_imss = db.Column(db.Numeric)
   s_base_modificado = db.Column(db.Numeric)
   s_imss_modificado = db.Column(db.Numeric)
   descuento_fonacot_num = db.Column(db.Numeric)
   descuento_infonavit_num = db.Column(db.Numeric)
   asistencias_totales = db.Column(db.Integer)
   he_totales = db.Column(db.Integer)
   pago_total = db.Column(db.Numeric)
   notas = db.Column(db.String(255))

   def __repr__(self):
    return f'<Pago total "{self.pago_total}">'

# A partir de aquí empiezan las rutas

@app.route('/',methods=["GET","POST"])
def home():
    return render_template('home.html')

@app.route('/consulta_proyectos',methods=["GET","POST"])
def consulta_proyectos():
    proyectos = Proyecto.query.order_by(Proyecto.status.desc()).all()
    return render_template('consulta_proyectos.html',proyectos=proyectos)

@app.route('/consulta_empleados',methods=["GET","POST"])
def consulta_empleados():
    empleados = Empleado.query.all()
    return render_template('consulta_empleados.html',empleados=empleados)

@app.route('/consulta_asistencias',methods=["GET","POST"])
def consulta_asistencias():
    proyectos = Proyecto.query.filter_by(status=True)
    today = datetime.now()
    num_sem = today.strftime("%U")
    if request.method == "POST":
        semana = request.form["semana"]
        idproyecto = request.form["id_proyecto"]

        lun_arg = '2022 ' + str(semana) + ' 1'
        lun = time.asctime(time.strptime(lun_arg,'%Y %W %w'))
        dom_arg = '2022 ' + str(semana) + ' 0'
        dom = time.asctime(time.strptime(dom_arg,'%Y %W %w'))

        empleados_asistencias = Asistencia.query.filter(Asistencia.id_proyecto == idproyecto).filter(lun<= Asistencia.day, Asistencia.day <= dom).with_entities(Asistencia.id_empleado).distinct()

        employees = []

        for z in empleados_asistencias:
            emp = Empleado.query.filter_by(id_empleado=z.id_empleado).first()
            employees.append(emp)

        rango = [1,2,3,4,5,6,0]
        
        empleados_dias = []
        
        for y in employees:
            dias = []
            week = []
            for x in rango:
                arg = '2022 ' + str(semana) + ' ' + str(x)
                dia_semana = time.asctime(time.strptime(arg,'%Y %W %w'))
                d = datetime.strptime(str(datetime.strptime(arg,'%Y %W %w')),'%Y-%m-%d %H:%M:%S').date()
                week.append(d)
                asistencias = Asistencia.query.filter_by(id_proyecto=idproyecto).filter_by(day=dia_semana).filter_by(id_empleado=y.id_empleado).first()
                dias.append(asistencias)
            empleados_dias.append(dias)

        return render_template('consulta_asistencias.html',proyectos=proyectos,week_number=num_sem,empleados_dias=empleados_dias,week=week)

    return render_template('consulta_asistencias.html',proyectos=proyectos,week_number=num_sem)

@app.route('/consulta_pagos',methods=["GET","POST"])
def consulta_pagos():
    proyectos = Proyecto.query.filter_by(status=True)
    weeknumber = datetime.now().date().strftime("%U")
    if request.method == "POST":
        week = request.form["semana"]
        arg = '2022 ' + str(week) + ' 4'
        week_day = time.asctime(time.strptime(arg,'%Y %W %w'))
        project = request.form["id_proyecto"]

        pagos = Pago.query.filter_by(id_proyecto=project).filter_by(fecha_operacion=week_day).all()
        return render_template('consulta_pagos.html',proyectos=proyectos,week_number=weeknumber,pagos=pagos)

    return render_template('consulta_pagos.html',proyectos=proyectos,week_number=weeknumber)

@app.route('/empleados',methods=["GET","POST"])
def empleados():
    proyectos = Proyecto.query.filter_by(status=True)

    requests = ["descuento_FONACOT","descuento_INFONAVIT"]
    m = []
    if request.method == "POST":
        # Esto lo hice así porque no puedo enviar el valor directamente como True o False
        for element in requests:
            if request.form[element] == "true":
                m.append(True)
            else:
                m.append(False)

        clave_banco = request.form["clave_banco"]
        nombre_empleado = request.form["nombre_empleado"]

        valida_empleado = Empleado.query.filter_by(clave_banco=clave_banco).first()
        valida_empleado2 = Empleado.query.filter_by(nombre_empleado=nombre_empleado).first()
        if valida_empleado is not None or valida_empleado2 is not None:
            message = "Ya existe un empleado con ese nombre o esa clave de banco. Favor de verificar los datos nuevamente"
            return render_template('empleados.html',proyectos=proyectos,message=message)
        else:
            new_employee = Empleado(clave_banco=clave_banco,nombre_empleado=nombre_empleado,salario_base=request.form["salario_base"],salario_base_IMSS=request.form["salario_base_IMSS"],descuento_FONACOT=m[0],descuento_INFONAVIT=m[1],costo_he=request.form["valor_he"],status=True,id_proyecto=request.form["proyecto"])

            db.session.add(new_employee)
            db.session.commit()
            info_empleado = Empleado.query.filter_by(nombre_empleado=request.form["nombre_empleado"]).all()
            return render_template('empleados.html',proyectos=proyectos,info_empleado=info_empleado)

    return render_template('empleados.html',proyectos=proyectos)

@app.route('/proyectos',methods=["GET","POST"])
def proyectos():
    if request.method == "POST":

        location = request.form["ubicacion"]
        customer = request.form["cliente"]
        project = request.form["nombre_proyecto"]

        if request.form["trabajo_diario"] == "true":
            l = True
        else:
            l = False

        valida_proyecto = Proyecto.query.filter_by(nombre_proyecto=project).first()

        if valida_proyecto is not None:
            message = "Ya existe un proyecto con ese nombre de proyecto. Por favor, asigna otro nombre para tu proyecto"
            return render_template('proyectos.html',message=message)
        else:
            new_project = Proyecto(nombre_proyecto=project,status=True,ubicacion=location,cliente=customer,trabajo_diario=l)

            db.session.add(new_project)
            db.session.commit()
            info = Proyecto.query.filter_by(nombre_proyecto=project).all()
            return render_template('proyectos.html',info_proyectos=info)
            
    return render_template('proyectos.html')

@app.route('/asistencias',methods=["GET","POST"])
def asistencias():
    # today = datetime.now().date() - timedelta(days=3)
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    proyectos = Proyecto.query.filter_by(status=True)

    if request.method == "POST":
        if "id_proyecto" in request.form:
            p = request.form["id_proyecto"]
            checar_asistencia = Asistencia.query.filter_by(id_proyecto=p).filter_by(day=today).first()
            c = Asistencia.query.filter_by(id_proyecto=p).filter_by(day=yesterday).first()
            checar_proyecto = Proyecto.query.filter_by(id_proyecto=p).first()
            if checar_proyecto.trabajo_diario == True and today.weekday() == 0 and c is None:
                check_project = True
            else:
                check_project = False

            if checar_asistencia is not None:
                message="No puedes checar asistencia dos veces el mismo día"
                return render_template('asistencias.html',message=message,proyectos=proyectos)
            elif c is not None:
                empleados = Empleado.query.filter_by(id_proyecto=request.form["id_proyecto"]).all()
                return render_template('asistencias.html',empleados=empleados,proyectos=proyectos,today=today,yesterday=yesterday,cp = check_project)
            else:
                empleados = Empleado.query.filter_by(id_proyecto=request.form["id_proyecto"]).all()
                return render_template('asistencias.html',empleados=empleados,proyectos=proyectos,today=today,yesterday=yesterday,cp = check_project)

        if "horas_extras" in request.form:
            e = request.form.getlist('empleado')
            he = request.form.getlist('horas_extras')
            fal = request.form.getlist('attendance')
            hoy = request.form.getlist('today')
            request_values = {"e":e,"he":he,"fal":fal,"hoy":hoy}
            s = 0
            for x in e:
                registro_asistencia = Asistencia(id_empleado=request_values["e"][s],horas_extras=request_values["he"][s],attendance=request_values["fal"][s],day=request_values["hoy"][s],id_proyecto=request.form["proyecto"])
                s = s+1

                db.session.add(registro_asistencia)
                db.session.commit()

            message = "Se han registrado exitosamente las asistencias"
            return render_template('asistencias.html',message=message,proyectos=proyectos)

    return render_template('asistencias.html',proyectos=proyectos)

@app.route('/pagos',methods=["GET","POST"])
def pagos():
    today = datetime.now().date()- timedelta(days=4)
    limit_day = today - timedelta(days=7)
    yesterday = today - timedelta(days=1)
    proyectos = Proyecto.query.filter_by(status=True)

    if request.method == "POST":
        if today.isoweekday() != 4:
            message = "No puedes realizar pagos hasta que sea jueves"
            return render_template('pagos.html',message=message,proyectos=proyectos)
        else:
            if "id_proyecto" in request.form:
                project = request.form["id_proyecto"]
                buscar_pago = Pago.query.filter_by(id_proyecto=project).filter_by(fecha_operacion=today).first()

                if buscar_pago is not None:
                    message="No puedes realizar dos pagos al mismo proyecto el mismo día"
                        
                    return render_template('pagos.html',message=message,proyectos=proyectos)
                else:
                    empleados = Empleado.query.filter_by(id_proyecto=project).all()
                    return render_template('pagos.html',empleados=empleados,proyectos=proyectos)

            if ("descuento_FONACOT" or "descuento_INFONAVIT") and "proyecto" in request.form:
                d_FONACOT = request.form.getlist('descuento_FONACOT')
                d_INFONAVIT = request.form.getlist('descuento_INFONAVIT')
                notas = request.form.getlist('notas')

                project = request.form["proyecto"]
                empleados = Empleado.query.filter_by(id_proyecto=project).all()

                indice = 0
                for empleado in empleados:
                    lista_asistencias = Asistencia.query.filter_by(id_proyecto=project,id_empleado=empleado.id_empleado).all()

                    asis = 0
                    horas_extras = 0
                    for asistencia in lista_asistencias:
                        d = asistencia.day
                        if (d.date() >= limit_day) and (d.date() <= yesterday):
                            asis = asis + asistencia.attendance
                            horas_extras = horas_extras + asistencia.horas_extras

                    pquery = Proyecto.query.filter_by(id_proyecto=project).first()
                    # for p in pquery:
                    if pquery.trabajo_diario == False:
                        asis = asis + 1

                    salario_base_modificado = (empleado.salario_base/7)*(asis)
                    salario_imss_modificado = (empleado.salario_base_IMSS/7)*(asis)

                    desc_F = float(d_FONACOT[indice])
                    desc_I = float(d_INFONAVIT[indice])  
                    nota = notas[indice]                

                    pago_total = float(salario_base_modificado)+ float(horas_extras*empleado.costo_he) - desc_F - desc_I
                    
                    new_payment = Pago(fecha_operacion=today,id_movimiento=9,id_proyecto=empleado.id_proyecto,id_empleado=empleado.id_empleado,s_base=empleado.salario_base,s_imss=empleado.salario_base_IMSS,s_base_modificado=round(salario_base_modificado,2),s_imss_modificado=round(salario_imss_modificado,2),descuento_fonacot_num=desc_F,descuento_infonavit_num=desc_I,asistencias_totales=asis,he_totales=horas_extras,pago_total=round(pago_total,2),notas=nota)

                    db.session.add(new_payment)
                    db.session.commit()
                    indice = indice + 1
                    

                message = "Se han registrado exitosamente los pagos"
                return render_template('pagos.html',message=message,proyectos=proyectos)
                # Falta agregar que si ya se hizo un registro no se puede hacer otro
    return render_template('pagos.html',proyectos=proyectos)

@app.route('/editarEmpleado/<variable>',methods=["GET","POST"])
def editarEmpleado(variable):
    employee = Empleado.query.filter_by(id_empleado=variable).first()
    proyectos = Proyecto.query.filter_by(status=True).all()

    if request.method == "POST":

        requests = ["descuento_FONACOT","descuento_INFONAVIT"]
        m = []
        # Esto lo hice así porque no puedo enviar el valor directamente como True o False
        for element in requests:
            if request.form[element] == "true":
                m.append(True)
            else:
                m.append(False)

        employee.salario_base = request.form["salario_base"]
        employee.salario_base_IMSS = request.form["salario_base_IMSS"]
        employee.descuento_FONACOT = m[0]
        employee.descuento_INFONAVIT = m[1]
        employee.costo_he = request.form["valor_he"]
        employee.id_proyecto = request.form["proyecto"]
        employee.status=True

        db.session.commit()

        employee = Empleado.query.filter_by(id_empleado=request.form["id_empleado"]).first()

        return redirect(url_for('consulta_empleados',employee=employee))

    return render_template('editarEmpleado.html',proyectos=proyectos,info_empleado = employee)

@app.route('/eliminarEmpleado/<variable>',methods=["GET","POST"])
def eliminarEmpleado(variable):
    employee = Empleado.query.filter_by(id_empleado=variable).first()
    employee.status = False
    employee.id_proyecto = None
    db.session.commit()
    return redirect(url_for('consulta_empleados'))

@app.route('/eliminarProyecto/<variable>',methods=["GET","POST"])
def eliminarProyecto(variable):
    project = Proyecto.query.filter_by(id_proyecto=variable).first()
    project.status = False
    db.session.commit()

    employees = Empleado.query.filter_by(id_proyecto=variable)
    for employee in employees:
        employee.status = False
        employee.id_proyecto = None
        db.session.commit()

    return redirect(url_for('consulta_proyectos'))

if __name__ == '__main__':
    db.create_all()
    app.run()