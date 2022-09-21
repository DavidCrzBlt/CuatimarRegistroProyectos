function validateForm() {
    var salario_base = document.getElementById("salario_base");
    var salario_base_IMSS = document.getElementById("salario_base_IMSS");

    if (salario_base_IMSS.value > salario_base.value) {
        alert("El salario base no puede ser menor que el salario que se registre en el IMSS");
        return false;
    }

    var id_proyecto = document.getElementById("proyecto");

    if (id_proyecto.value == "Selecciona el proyecto") {
        alert("Debes escoger al menos un proyecto");
        return false;
    }
}

function validateFormAsistencias() {
    var id_proyecto = document.getElementById("id_proyecto");

    if (id_proyecto.value == "Selecciona el proyecto") {
        alert("Debes escoger al menos un proyecto");
        return false;
    }
}

function validateTrabajoProyecto() {
    var trabajo_diario = document.getElementById("trabajo_diario");

    if (trabajo_diario.value == "Trabajo de lunes a sábado") {
        alert("Debes escoger la forma de trabajo del proyecto. Trabajo de lunes a sábado sí o no.");
        return false;
    }
}

function exportTableToExcel(tableID, filename = '') {
    var downloadLink;
    var dataType = 'application/vnd.ms-excel';
    var tableSelect = document.getElementById(tableID);
    var tableHTML = tableSelect.outerHTML.replace(/ /g, '%20');

    // Specify file name
    filename = filename ? filename + '.xls' : tableID + '.xls';

    // Create download link element
    downloadLink = document.createElement("a");

    document.body.appendChild(downloadLink);

    if (navigator.msSaveOrOpenBlob) {
        var blob = new Blob(['ufeff', tableHTML], {
            type: dataType
        });
        navigator.msSaveOrOpenBlob(blob, filename);
    } else {
        // Create a link to the file
        downloadLink.href = 'data:' + dataType + ', ' + tableHTML;

        // Setting the file name
        downloadLink.download = filename;

        //triggering the function
        downloadLink.click();
    }
}

function deleteEmployee(id_empleado, nombre_empleado) {
   
    let text;
    if (confirm("¿Quieres dar de baja a " + nombre_empleado + "?") == true) {
        window.location.href = "/eliminarEmpleado/"+id_empleado;
    } else {
        text = "Cancelaste la operación";
    }
}

function deleteProject(id_proyecto, nombre_proyecto) {
   
    let text;
    if (confirm("¿Quieres dar de baja a " + nombre_proyecto + "?") == true) {
        window.location.href = "/eliminarProyecto/"+id_proyecto;
    } else {
        text = "Cancelaste la operación";
    }
}
