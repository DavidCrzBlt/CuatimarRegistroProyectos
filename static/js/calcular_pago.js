function calcularPago(){
    const options = {style:'currency',currency:'MXN'};
    const numberFormat = new Intl.NumberFormat('es-MX', options);
    
    var rows = document.getElementsByTagName("tr");

    for(var i=1;i<rows.length;i++){
        var columns = rows[i].getElementsByTagName("td");
        var inputs = rows[i].getElementsByTagName("input");
        var ids = inputs[0].value;
        var asistencias = inputs[1].value;
        var horas_extras = inputs[2].value;
        var s_base = inputs[3].value;
        var s_base_imss = inputs[4].value;
        columns[1].textContent = ids;
        columns[4].textContent = asistencias;
        columns[6].textContent = horas_extras;
        var salario_base = numberFormat.format(s_base);
        columns[8].textContent = salario_base;
        var salario_imss = numberFormat.format(s_base_imss);
        columns[10].textContent = salario_imss;
        var costo_he = numberFormat.format(inputs[7].value);
        columns[16].textContent = costo_he;

            complemento_pago = s_base - s_base_imss;
            pago_dia = ((s_base/7)*(7-asistencias)).toFixed(2);
            if (pago_dia > complemento_pago){
                var s_imss_mod = (((s_base_imss/7)*(asistencias))-parseFloat(inputs[8].value)-parseFloat(inputs[9].value)).toFixed(2);
                var s_base_mod = ((s_base/7)*(asistencias)).toFixed(2);
                var salario_base_mod = numberFormat.format(s_base_mod);
                inputs[5].value = s_base_mod;
                columns[12].textContent = salario_base_mod;
                var salario_imss_mod = numberFormat.format(s_imss_mod);
                inputs[6].value =s_imss_mod;
                columns[14].textContent = salario_imss_mod;

                var pago = parseFloat(inputs[5].value)+parseFloat(parseFloat(inputs[7].value)*parseFloat(horas_extras))-parseFloat(inputs[10].value);

                if (pago < s_imss_mod){

                    inputs[6].value =pago.toFixed(2);
                    var pago_format = numberFormat.format(pago);
                    columns[14].textContent = pago_format;
                    inputs[11].value = pago.toFixed(2);
                    columns[21].textContent = pago_format;

                    var diferencia = parseFloat(0);
                    inputs[11].value = diferencia;
                    var diferencia_format = numberFormat.format(diferencia);
                    columns[23].textContent = diferencia_format;

                }
                else{
                    var pago_format = numberFormat.format(pago);
                    inputs[11].value = pago.toFixed(2);    
                    columns[21].textContent = pago_format;

                    var diferencia = parseFloat(pago-inputs[6].value);
                    inputs[11].value = diferencia.toFixed(2);
                    var diferencia_format = numberFormat.format(diferencia);
                    columns[23].textContent = diferencia_format;
                }

            }
            else{
                var s_imss_mod = (s_base_imss-parseFloat(inputs[8].value)-parseFloat(inputs[9].value)).toFixed(2);
                var s_base_mod = ((s_base/7)*(asistencias)).toFixed(2);
                var salario_base_mod = numberFormat.format(s_base_mod);
                inputs[5].value = s_base_mod;
                columns[12].textContent = salario_base_mod;
                var salario_imss_mod = numberFormat.format(s_imss_mod);
                inputs[6].value =s_imss_mod;
                columns[14].textContent = salario_imss_mod;

                var pago = parseFloat(inputs[5].value)+parseFloat(parseFloat(inputs[7].value)*parseFloat(horas_extras))-parseFloat(inputs[10].value);

                if (pago < s_imss_mod){

                    inputs[6].value =pago.toFixed(2);
                    var pago_format = numberFormat.format(pago);
                    columns[14].textContent = pago_format;
                    inputs[11].value = pago.toFixed(2);
                    columns[21].textContent = pago_format;

                    var diferencia = parseFloat(0);
                    inputs[11].value = diferencia;
                    var diferencia_format = numberFormat.format(diferencia);
                    columns[23].textContent = diferencia_format;

                }
                else{
                    var pago_format = numberFormat.format(pago);
                    inputs[11].value = pago.toFixed(2);    
                    columns[21].textContent = pago_format;

                    var diferencia = parseFloat(pago-inputs[6].value);
                    inputs[11].value = diferencia.toFixed(2);
                    var diferencia_format = numberFormat.format(diferencia);
                    columns[23].textContent = diferencia_format;
                }   
            }      
    }
}

calcularPago();

const descuentos = document.getElementsByClassName("descuento");

for(var x=0;x<descuentos.length;x++){
    descuentos[x].addEventListener('change',calcularPago);
}