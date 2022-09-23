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

db = SQLAlchemy(app)


class Proyecto(db.Model):
    id_proyecto = db.Column('id_proyecto', db.Integer, primary_key=True)
    nombre_proyecto = db.Column(db.String(255), unique=True)
    registro_patronal = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    ubicacion = db.Column(db.String(200))
    cliente = db.Column(db.String(200))
    trabajo_diario = db.Column(db.Boolean)
    salarios = db.relationship('Salario', backref='proyecto')
    asistencias = db.relationship('Asistencia', backref='proyecto')
    pagos = db.relationship('Pago', backref='proyecto')

    def __repr__(self):
        return f'<Proyecto "{self.nombre_proyecto}">'


class Empleado(db.Model):
    id_empleado = db.Column('id_empleado', db.Integer, primary_key=True)
    clave_banco = db.Column(db.Integer, unique=True)
    nombre_empleado = db.Column(db.String(255), unique=True)
    descuento_FONACOT = db.Column(db.Boolean)
    descuento_INFONAVIT = db.Column(db.Boolean)
    status = db.Column(db.Boolean)
    asistencias = db.relationship('Asistencia', backref='empleado')
    pagos = db.relationship('Pago', backref='empleado')
    salarios = db.relationship('Salario', backref='empleado')

    def __repr__(self):
        return f'<Nombre empleado "{self.nombre_empleado}">'


class Salario(db.Model):
    id_salario = db.Column('id_salario', db.Integer, primary_key=True)
    id_empleado = db.Column(db.Integer, db.ForeignKey('empleado.id_empleado'))
    id_proyecto = db.Column(db.Integer, db.ForeignKey('proyecto.id_proyecto'))
    salario_base = db.Column(db.Numeric)
    salario_base_IMSS = db.Column(db.Numeric)
    costo_he = db.Column(db.Numeric)
    status = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Id Salario "{self.id_salario}">'


class Asistencia(db.Model):
    id_asistencia = db.Column('id_asistencia', db.Integer, primary_key=True)
    id_empleado = db.Column(db.Integer, db.ForeignKey('empleado.id_empleado'))
    horas_extras = db.Column(db.Integer)
    attendance = db.Column(db.Integer)
    day = db.Column(db.DateTime)
    id_proyecto = db.Column(db.Integer, db.ForeignKey('proyecto.id_proyecto'))

    def __repr__(self):
        return f'<ID empleado "{self.id_empleado}">'


class Pago(db.Model):
    id = db.Column('id_operacion', db.Integer, primary_key=True)
    fecha_operacion = db.Column(db.DateTime)
    id_proyecto = db.Column(db.Integer, db.ForeignKey('proyecto.id_proyecto'))
    id_empleado = db.Column(db.Integer, db.ForeignKey('empleado.id_empleado'))
    s_base = db.Column(db.Numeric)
    s_imss = db.Column(db.Numeric)
    s_base_modificado = db.Column(db.Numeric)
    s_imss_modificado = db.Column(db.Numeric)
    descuento_fonacot_num = db.Column(db.Numeric)
    descuento_infonavit_num = db.Column(db.Numeric)
    descuento = db.Column(db.Numeric)
    asistencias_totales = db.Column(db.Integer)
    he_totales = db.Column(db.Integer)
    costo_he = db.Column(db.Numeric)
    pago_total = db.Column(db.Numeric)
    diferencia = db.Column(db.Numeric)
    notas = db.Column(db.String(255))

    def __repr__(self):
        return f'<Pago total "{self.pago_total}">'

# A partir de aquí empiezan las rutas

@app.route('/', methods=["GET", "POST"])
def home():
    return render_template('home.html')

@app.route('/proyectos', methods=["GET", "POST"])
def proyectos():
    if request.method == "POST":

        location = request.form["ubicacion"]
        customer = request.form["cliente"]
        project = request.form["nombre_proyecto"]
        registro_patronal = request.form["registro_patronal"]

        if request.form["trabajo_diario"] == "true":
            l = True
        else:
            l = False

        valida_proyecto = Proyecto.query.filter_by(
            nombre_proyecto=project).first()

        if valida_proyecto is not None:
            message = "Ya existe un proyecto con ese nombre de proyecto. Por favor, asigna otro nombre para tu proyecto"
            return render_template('proyectos.html', message=message)
        else:
            new_project = Proyecto(nombre_proyecto=project, registro_patronal=registro_patronal,
                                   status=True, ubicacion=location, cliente=customer, trabajo_diario=l)

            db.session.add(new_project)
            db.session.commit()
            info = Proyecto.query.filter_by(nombre_proyecto=project).all()
            return render_template('proyectos.html', info_proyectos=info)

    return render_template('proyectos.html')

@app.route('/empleados', methods=["GET", "POST"])
def empleados():
    proyectos = Proyecto.query.filter_by(status=True)

    requests = ["descuento_FONACOT", "descuento_INFONAVIT"]
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

        valida_empleado = Empleado.query.filter_by(
            clave_banco=clave_banco).first()
        valida_empleado2 = Empleado.query.filter_by(
            nombre_empleado=nombre_empleado).first()
        if valida_empleado is not None or valida_empleado2 is not None:
            message = "Ya existe un empleado con ese nombre o esa clave de banco. Favor de verificar los datos nuevamente"
            return render_template('empleados.html', proyectos=proyectos, message=message)
        else:
            # Agregamos un nuevo empleado a la tabla de empleados
            new_employee = Empleado(clave_banco=clave_banco, nombre_empleado=nombre_empleado,
                                    descuento_FONACOT=m[0], descuento_INFONAVIT=m[1], status=True)

            db.session.add(new_employee)
            db.session.commit()

            # Del nuevo empleado que agregamos tomamos la clave del banco que es única para asignarle un primer salario
            employee = Empleado.query.filter_by(
                clave_banco=clave_banco).first()
            new_salary = Salario(id_empleado=employee.id_empleado, id_proyecto=request.form["proyecto"], salario_base=request.form[
                                 "salario_base"], salario_base_IMSS=request.form["salario_base_IMSS"], costo_he=request.form["valor_he"], status=True)

            db.session.add(new_salary)
            db.session.commit()

            # En la línea siguiente no es necesario poner más filtros porque es la primera vez que se registra al empleado
            info_salario = Salario.query.filter_by(
                id_empleado=employee.id_empleado).first()
            # Pasamos la variable de empleado y salario para que el cliente vea los datos que se registraron

            return render_template('empleados.html', proyectos=proyectos, info_empleado=employee, info_salario=info_salario)

    return render_template('empleados.html', proyectos=proyectos)

@app.route('/asistencias', methods=["GET", "POST"])
def asistencias():
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    proyectos = Proyecto.query.filter_by(status=True)

    if request.method == "POST":
        if "id_proyecto" in request.form:
            p = request.form["id_proyecto"]
            checar_asistencia = Asistencia.query.filter_by(
                id_proyecto=p).filter_by(day=today).first()
            c = Asistencia.query.filter_by(
                id_proyecto=p).filter_by(day=yesterday).first()
            checar_proyecto = Proyecto.query.filter_by(id_proyecto=p).first()

            if checar_proyecto.trabajo_diario == True and today.weekday() == 0 and c is None:
                check_project = True
            else:
                check_project = False

            if checar_asistencia is not None:
                message = "No puedes checar asistencia dos veces el mismo día"
                return render_template('asistencias.html', message=message, proyectos=proyectos)
            elif c is not None:
                empleados = Salario.query.filter_by(id_proyecto=request.form["id_proyecto"], status=True).all()
                return render_template('asistencias.html', empleados=empleados, proyectos=proyectos, today=today, yesterday=yesterday, cp=check_project)
            else:
                empleados = Salario.query.filter_by(id_proyecto=request.form["id_proyecto"], status=True).all()
                return render_template('asistencias.html', empleados=empleados, proyectos=proyectos, today=today, yesterday=yesterday, cp=check_project)

        if "horas_extras" in request.form:
            e = request.form.getlist('empleado')
            he = request.form.getlist('horas_extras')
            fal = request.form.getlist('attendance')
            hoy = request.form.getlist('today')
            request_values = {"e": e, "he": he, "fal": fal, "hoy": hoy}
            s = 0
            for x in e:
                registro_asistencia = Asistencia(id_empleado=request_values["e"][s], horas_extras=request_values["he"][s], attendance=request_values["fal"][s], day=request_values["hoy"][s], id_proyecto=request.form["proyecto"])
                s = s+1

                db.session.add(registro_asistencia)
                db.session.commit()

            message = "Se han registrado exitosamente las asistencias"
            return render_template('asistencias.html', message=message, proyectos=proyectos)

    return render_template('asistencias.html', proyectos=proyectos)

@app.route('/pagos', methods=["GET", "POST"])
def pagos():
    today = datetime.now().date()+timedelta(days=1)
    num_semana = today.strftime("%U")
    proyectos = Proyecto.query.filter_by(status=True)

    if request.method == "POST":
        if today.isoweekday() != 4:
            message = "No puedes realizar pagos hasta que sea jueves"
            return render_template('pagos.html', message=message, proyectos=proyectos)
        else:
            if "id_proyecto" in request.form:
                project = request.form["id_proyecto"]
                buscar_pago = Pago.query.filter_by(
                    id_proyecto=project).filter_by(fecha_operacion=today).first()

                if buscar_pago is not None:
                    message = "No puedes realizar dos pagos al mismo proyecto el mismo día"
                    return render_template('pagos.html', message=message, proyectos=proyectos)
                else:
                    lun_arg = '2022 ' + str(num_semana) + ' 1'
                    lun = time.asctime(time.strptime(lun_arg, '%Y %W %w'))
                    mar_arg = '2022 ' + str(num_semana) + ' 2'
                    mar = time.asctime(time.strptime(mar_arg, '%Y %W %w'))
                    mier_arg = '2022 ' + str(num_semana) + ' 3'
                    mier = time.asctime(time.strptime(mier_arg, '%Y %W %w'))
                    jue_arg = '2022 ' + str(int(num_semana)-1) + ' 4'
                    jue = time.asctime(time.strptime(jue_arg, '%Y %W %w'))
                    vie_arg = '2022 ' + str(int(num_semana)-1) + ' 5'
                    vie = time.asctime(time.strptime(vie_arg, '%Y %W %w'))
                    sab_arg = '2022 ' + str(int(num_semana)-1) + ' 6'
                    sab = time.asctime(time.strptime(sab_arg, '%Y %W %w'))
                    dom_arg = '2022 ' + str(int(num_semana)-1) + ' 0'
                    dom = time.asctime(time.strptime(dom_arg, '%Y %W %w'))

                    dias_semana=[jue,vie,sab,dom,lun,mar,mier]

                    listado_ids = []
                    listado_nombres = []
                    listado_fonacot = []
                    listado_infonavit = []

                    for d in dias_semana:
                        asistencia = Asistencia.query.filter_by(id_proyecto=project,day=d)

                        if asistencia is not None:
                            if len(listado_nombres)==0:
                                for ids in asistencia:
                                    listado_ids.append(ids.id_empleado)
                                    listado_nombres.append(ids.empleado.nombre_empleado)
                                    listado_fonacot.append(ids.empleado.descuento_FONACOT)
                                    listado_infonavit.append(ids.empleado.descuento_INFONAVIT)
                            else:
                                for names in asistencia:
                                    s=False
                                    while s==False:
                                        for element in listado_ids:
                                            if element==names.id_empleado:
                                                s=True
                                                break
                                            else:
                                                s=False
                                        if s==False:
                                            listado_ids.append(names.id_empleado)
                                            listado_nombres.append(names.empleado.nombre_empleado)
                                            listado_fonacot.append(names.empleado.descuento_FONACOT)
                                            listado_infonavit.append(names.empleado.descuento_INFONAVIT)
                                            s=True

                    lista_pagos = {"ids":listado_ids,"Nombre":listado_nombres,"Asistencia":[],"Horas extras":[],"Salario base":[],"Salario IMSS":[],"Costo horas extras":[],"Descuento FONACOT":listado_fonacot,"Descuento INFONAVIT":listado_infonavit}
                    
                    for empleado in listado_ids:
                        contador_asistencias = 0
                        contador_horas_extras = 0
                        for m in dias_semana:
                            dia = Asistencia.query.filter_by(id_empleado=empleado,day=m,id_proyecto=project).first()
                            if dia is not None:
                                contador_asistencias = contador_asistencias + dia.attendance
                                contador_horas_extras = contador_horas_extras + dia.horas_extras
                            else:
                                contador_asistencias = contador_asistencias
                                contador_horas_extras = contador_horas_extras

                        # Va a considerar si el proyecto es de lunes a domingo 
                        pquery = Proyecto.query.filter_by(id_proyecto=project).first()
                        if pquery.trabajo_diario == False:
                            contador_asistencias = contador_asistencias + 1
                          
                        lista_pagos["Asistencia"].append(contador_asistencias)
                        lista_pagos["Horas extras"].append(contador_horas_extras)

                        empleado_info = Salario.query.filter_by(id_empleado=empleado,id_proyecto=project).first()
                        lista_pagos["Costo horas extras"].append(empleado_info.costo_he)
                        lista_pagos["Salario base"].append(empleado_info.salario_base)
                        lista_pagos["Salario IMSS"].append(empleado_info.salario_base_IMSS)
            
                    indice = list(range(0,len(listado_nombres)))

                    proj = Proyecto.query.filter_by(id_proyecto=project).first()
            
                    return render_template('pagos.html',indice=indice,lista_pagos=lista_pagos, proyectos=proyectos,project=proj,num_semana=num_semana)

            if "proyecto" in request.form:
                id_empleado = request.form.getlist('ids')
                s_base = request.form.getlist('salario_base')
                s_imss = request.form.getlist('salario_imss')
                s_base_mod = request.form.getlist('salario_base_mod')
                s_imss_mod = request.form.getlist('salario_imss_mod')
                d_FONACOT = request.form.getlist('descuento_FONACOT')
                d_INFONAVIT = request.form.getlist('descuento_INFONAVIT')
                discount = request.form.getlist('descuento')
                asistencias_totales = request.form.getlist('asistencia')
                he_totales = request.form.getlist('he')
                costo_he = request.form.getlist('costo_he')
                pago_total = request.form.getlist('pago_total')
                diferencia = request.form.getlist('diferencia')
                notas = request.form.getlist('notas')
                project = request.form["proyecto"]

                l = 0
                while l < len(id_empleado):
                    new_payment = Pago(fecha_operacion=today, id_proyecto=project, id_empleado=id_empleado[l], s_base=s_base[l], s_imss=s_imss[l], s_base_modificado=s_base_mod[l], s_imss_modificado=s_imss_mod[l], descuento_fonacot_num=d_FONACOT[l], descuento_infonavit_num=d_INFONAVIT[l],descuento=discount[l], asistencias_totales=asistencias_totales[l], he_totales=he_totales[l],costo_he=costo_he[l], pago_total=pago_total[l], diferencia=diferencia[l], notas=notas[l])
                    
                    db.session.add(new_payment)
                    db.session.commit()
                    l = l + 1

                message = "Se han registrado exitosamente los pagos"
                return render_template('pagos.html', message=message, proyectos=proyectos)
    return render_template('pagos.html', proyectos=proyectos)

@app.route('/consulta_proyectos', methods=["GET", "POST"])
def consulta_proyectos():
    page = request.args.get('page',1,type=int)
    pagination = Proyecto.query.order_by(Proyecto.id_proyecto.asc()).paginate(page,per_page=7)
    return render_template('consulta_proyectos.html', proyectos=proyectos,pagination=pagination)

@app.route('/consulta_empleados', methods=["GET", "POST"])
def consulta_empleados():
    
    page = request.args.get('page',1,type=int)
    
    empleados_activos = (db.session.query(Empleado.id_empleado,Empleado.clave_banco,Empleado.nombre_empleado,Salario.salario_base,Salario.salario_base_IMSS,Salario.costo_he,Empleado.descuento_FONACOT,Empleado.descuento_INFONAVIT,Proyecto.nombre_proyecto,Salario.status).join(Salario,Empleado.id_empleado == Salario.id_empleado,isouter=True).join(Proyecto,Salario.id_proyecto == Proyecto.id_proyecto).filter(Salario.status==True).order_by(Empleado.id_empleado.asc())).paginate(page,per_page=10)

    if request.method == "POST":
        nombre = request.form["nombre"]
        
        search_nombre = "%{}%".format(nombre)
        empleados_activos = (db.session.query(Empleado.id_empleado,Empleado.clave_banco,Empleado.nombre_empleado,Salario.salario_base,Salario.salario_base_IMSS,Salario.costo_he,Empleado.descuento_FONACOT,Empleado.descuento_INFONAVIT,Proyecto.nombre_proyecto,Salario.status).join(Salario,Empleado.id_empleado == Salario.id_empleado,isouter=True).join(Proyecto,Salario.id_proyecto == Proyecto.id_proyecto)).filter(Empleado.nombre_empleado.ilike(search_nombre)).paginate(page,per_page=10)

        return render_template('consulta_empleados.html',empleados_activos=empleados_activos)

    return render_template('consulta_empleados.html',empleados_activos=empleados_activos)

@app.route('/consulta_asistencias', methods=["GET", "POST"])
def consulta_asistencias():
    proyectos = Proyecto.query.filter_by(status=True)
    today = datetime.now()
    num_sem = today.strftime("%U")

    if request.method == "POST":
        semana = request.form["semana"]
        idproyecto = request.form["id_proyecto"]

        lun_arg = '2022 ' + str(semana) + ' 1'
        lun = time.asctime(time.strptime(lun_arg, '%Y %W %w'))
        mar_arg = '2022 ' + str(semana) + ' 2'
        mar = time.asctime(time.strptime(mar_arg, '%Y %W %w'))
        mier_arg = '2022 ' + str(semana) + ' 3'
        mier = time.asctime(time.strptime(mier_arg, '%Y %W %w'))
        jue_arg = '2022 ' + str(semana) + ' 4'
        jue = time.asctime(time.strptime(jue_arg, '%Y %W %w'))
        vie_arg = '2022 ' + str(semana) + ' 5'
        vie = time.asctime(time.strptime(vie_arg, '%Y %W %w'))
        sab_arg = '2022 ' + str(semana) + ' 6'
        sab = time.asctime(time.strptime(sab_arg, '%Y %W %w'))
        dom_arg = '2022 ' + str(semana) + ' 0'
        dom = time.asctime(time.strptime(dom_arg, '%Y %W %w'))

        dias_semana=[lun,mar,mier,jue,vie,sab,dom]

        listado_ids = []
        listado_nombres = []

        for d in dias_semana:
            asistencia = Asistencia.query.filter_by(id_proyecto=idproyecto,day=d)

            if asistencia is not None:
                if len(listado_nombres)==0:
                    for nombres in asistencia:
                        listado_ids.append(nombres.id_empleado)
                        listado_nombres.append(nombres.empleado.nombre_empleado)
                else:
                    for names in asistencia:
                        s=False
                        while s==False:
                            for element in listado_ids:
                                if element==names.id_empleado:
                                    s=True
                                    break
                                else:
                                    s=False
                            if s==False:
                                listado_ids.append(names.id_empleado)
                                listado_nombres.append(names.empleado.nombre_empleado)
                                s=True

        lista_asistencia = {"ids":listado_ids,"Nombre":listado_nombres,"Asistencia":[],"Horas extras":[]}
        
        for empleado in listado_ids:
            asistencias_semana = []
            horas_extras_semana = []
            for m in dias_semana:
                dia = Asistencia.query.filter_by(id_empleado=empleado,day=m,id_proyecto=idproyecto).first()
                if dia is not None:
                    asistencias_semana.append(dia.attendance)
                    horas_extras_semana.append(dia.horas_extras)
                else:
                    asistencias_semana.append(0)
                    horas_extras_semana.append(0)
                
            lista_asistencia["Asistencia"].append(asistencias_semana)
            lista_asistencia["Horas extras"].append(horas_extras_semana)
 
        indice = list(range(0,len(listado_nombres)))
        count_semana = list(range(0,7))

        return render_template('consulta_asistencias.html',lista_asistencia=lista_asistencia,week=dias_semana,indice=indice,count_semana=count_semana,proyectos=proyectos,week_number=num_sem)

    return render_template('consulta_asistencias.html', proyectos=proyectos, week_number=num_sem)

@app.route('/consulta_pagos', methods=["GET", "POST"])
def consulta_pagos():
    proyectos = Proyecto.query.filter_by(status=True)
    weeknumber = datetime.now().date().strftime("%U")
    if request.method == "POST":
        week = request.form["semana"]
        arg = '2022 ' + str(week) + ' 4'
        week_day = time.asctime(time.strptime(arg, '%Y %W %w'))
        project = request.form["id_proyecto"]

        pagos = Pago.query.filter_by(id_proyecto=project).filter_by(
            fecha_operacion=week_day).all()
        return render_template('consulta_pagos.html', proyectos=proyectos, week_number=weeknumber, pagos=pagos)

    return render_template('consulta_pagos.html', proyectos=proyectos, week_number=weeknumber)

@app.route('/editarEmpleado/<variable>', methods=["GET", "POST"])
def editarEmpleado(variable):

    t = Salario.query.filter_by(id_empleado=variable, status=True).first()

    if t is not None:
        trabajador = t
    else:
        trabajador = Salario.query.filter_by(id_empleado=variable).first()

    datos_trabajador = Salario.query.filter_by(id_empleado=variable).all()

    projects = Proyecto.query.filter_by(status=True).all()

    if request.method == "POST":

        desasignar_proyectos = Salario.query.filter_by(
            id_empleado=request.form["id_empleado"]).all()
        for e in desasignar_proyectos:
            e.status = False
            db.session.commit()

        asignar_datos = Salario(id_empleado=request.form["id_empleado"], id_proyecto=request.form["id_proyecto"], salario_base=request.form[
                                "salario_base"], salario_base_IMSS=request.form["salario_base_IMSS"], costo_he=request.form["valor_he"], status=True)
        db.session.add(asignar_datos)
        db.session.commit()

        requests = ["descuento_FONACOT", "descuento_INFONAVIT"]
        m = []
        if request.method == "POST":
            # Esto lo hice así porque no puedo enviar el valor directamente como True o False
            for element in requests:
                if request.form[element] == "true":
                    m.append(True)
                else:
                    m.append(False)

        modificacion_empleado = Empleado.query.filter_by(
            id_empleado=request.form["id_empleado"]).first()
        modificacion_empleado.nombre_empleado = request.form["nombre_empleado"]
        modificacion_empleado.descuento_FONACOT = m[0]
        modificacion_empleado.descuento_INFONAVIT = m[1]
        modificacion_empleado.status = True
        db.session.commit()

        return redirect(url_for('consulta_empleados'))

    return render_template('editarEmpleado.html', trabajador=trabajador, datos_trabajador=datos_trabajador, proyectos=projects)

@app.route('/reasignarEmpleado/<proyecto>/<empleado>', methods=["GET", "POST"])
def reasignarEmpleado(proyecto, empleado):
    print("se va a reasignar este empleado")

    proyectos = Salario.query.filter_by(id_empleado=empleado).all()
    for each in proyectos:
        each.status = False
        db.session.commit()

    asignacion = Salario.query.filter_by(id_empleado=empleado,id_proyecto=proyecto).first()
    asignacion.status = True
    db.session.commit()

    emp = Empleado.query.filter_by(id_empleado=empleado).first()
    emp.status = True
    db.session.commit()

    return redirect(url_for('consulta_empleados'))

@app.route('/eliminarEmpleado/<variable>', methods=["GET", "POST"])
def eliminarEmpleado(variable):
    # Cambiar el estatus del empleado a "False" en la tabla "Empleado"
    employee = Empleado.query.filter_by(id_empleado=variable).first()
    employee.status = False
    employee.id_proyecto = None
    db.session.commit()
    # Cambiar el estatus del empleado a "False" en la tabla "Salario"
    employee_salary = Salario.query.filter_by(
        id_empleado=variable, status=True).first()
    employee_salary.status = False
    db.session.commit()
    return redirect(url_for('consulta_empleados'))

@app.route('/eliminarProyecto/<variable>', methods=["GET", "POST"])
def eliminarProyecto(variable):
    project = Proyecto.query.filter_by(id_proyecto=variable).first()
    project.status = False
    db.session.commit()

    employees = Salario.query.filter_by(id_proyecto=variable)
    for employee in employees:
        employee.status = False
        employee.empleado.status = False
        db.session.commit()

    return redirect(url_for('consulta_proyectos'))


if __name__ == '__main__':
    db.create_all()
    app.run()
