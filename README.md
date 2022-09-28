# Sistema de control de personal para proyectos

## Introducción

Un problema muy común en las empresas que administran proyectos es que no todas cuentan con las herramientas para tener información actualizada.
Lo anterior ocasiona dos problemas graves.

1. El primero es que exista una asignación de recursos ineficiente, ya que la empresa tiene que destinar más recursos para ejecutar una tarea.
2. La segunda es que aumentan las probabilidades de cometer un error en la parte administrativa del personal

De ahí surge la necesidad de crear una herramienta capaz de capturar las aasistencias de los empleados dependiendo del proyecto en el que estén trabajando y juntar toda esa información para calcular los pagos correspondientes. 

## Alcance del proyecto

Así como todas las herramientas tienen un propósito y un límite de uso, esta no es la excepción. Esta herramienta está diseñada exclusivamente para llevar control de asistencias de personal en diferentes proyectos simultaneos, y calcular los pagos que corresponden a cada trabajador por proyecto.

Este sistema está diseñado principalmente para aquellas personas que se encargan de la gestión de nóminas y las personas que se encargan de capturar las asistencias.

## ¿Cómo funciona?

Muy sencillo. Hay una serie de pasos que se deben seguir para poder usarla y que funcione de manera correcta.

1. **Registro del proyecto**

    Obviamente para empezar a trabajar, necesitamos registrar el proyecto: nombre del proyecto, registro patronal, cliente, ubicación del proyecto y si el proyecto es de lunes a sábado o de lunes a domingo.
    
    Lo anterior es importante porque de no definir correctamente los días que se trabajarán en el proyecto va a afectar la lista de asistencia.
    
    <img width="824" alt="image" src="https://user-images.githubusercontent.com/73202205/192895711-5bf31e28-cde0-4896-a525-c17c12c7e031.png">
  
2. **Asignación de empleados**
  
    Después de la creación del proyecto, sigue asignar a los empleados que van a trabajar en el mismo y esto se puede lograr de dos maneras.
    
    a. **Registrar a un empleado que no existe**
    
    <img width="827" alt="image" src="https://user-images.githubusercontent.com/73202205/192896884-b06f0a50-7e43-48ec-8669-38d576678658.png">

    b. **Reasignar un empleado de otro proyecto al nuevo proyecto**
    
    <img width="825" alt="image" src="https://user-images.githubusercontent.com/73202205/192897028-3753b987-2fc6-43fc-b943-2efd41965c6f.png">

3. **Registro de asistencias**

    Para el registro de asistencias solo basta con elegir el proyecto y se desplegarán automáticamente todos los empleados que están involucrados en ese proyecto.
    Es muy importante que el registro de asistencias se llene **de lunes a sábado sin excepción.**
    
    Lo único que va a cambiar entre los proyectos que sean "L-S" y "L-D" es que en los proyectos "L-s" se va a tomar por default la asistencia del domingo. Puesto que el domingo es día de descanso por ley. 
    
    Por otro lado, los proyectos que sean de "L-D" te va a permitir el sistema hacer el registro del domingo el día lunes y posteriormente podrás registrar la asistencia del día lunes.

4. **Registro de pagos**

    Por último, cada jueves debes ingresar para hacer el registro de los pagos correspondientes a la semana.
    
    Lo único que debes hacer es seleccionar el proyecto al cual vas a generar los pagos y hacer los ajustes correspondientes a descuentos del gobierno o excepciones.
    
    
Con lo anterior se busca poder resolver el problema del cálculo de nóminas en empresas que llevan más de un proyecto en curso.
