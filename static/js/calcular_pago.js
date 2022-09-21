function calcularPago(){
    const options = {style:'currency',currency:'MXN'};
    const numberFormat = new Intl.NumberFormat('es-MX', options);
    
    var rows = document.getElementsByTagName("tr");

    for(var i=1;i<rows.length;i++){
        var columns = rows[i].getElementsByTagName("td");
        var inputs = rows[i].getElementsByTagName("input");
        columns[1].textContent = inputs[0].value;
        columns[4].textContent = inputs[1].value;
        columns[6].textContent = inputs[2].value;
        var salario_base = numberFormat.format(inputs[3].value);
        columns[8].textContent = salario_base;
        var salario_imss = numberFormat.format(inputs[4].value);
        columns[10].textContent = salario_imss;
        var salario_base_mod = numberFormat.format(inputs[5].value);
        columns[12].textContent = salario_base_mod;
        var salario_imss_mod = numberFormat.format(inputs[6].value);
        columns[14].textContent = salario_imss_mod;
        var costo_he = numberFormat.format(inputs[7].value);
        columns[16].textContent = costo_he;

        var pago = parseFloat(inputs[5].value)+parseFloat(parseFloat(inputs[7].value)*parseFloat(inputs[2].value))-parseFloat(inputs[8].value)-parseFloat(inputs[9].value);
        inputs[10].value = pago.toFixed(2);
        var pago_format = numberFormat.format(pago);
        columns[20].textContent = pago_format;

        var diferencia = parseFloat(pago-inputs[6].value);
        inputs[11].value = diferencia.toFixed(2);
        var diferencia_format = numberFormat.format(diferencia);
        columns[22].textContent = diferencia_format;

    }
}

calcularPago();

const descuentos = document.getElementsByClassName("descuento");

for(var x=0;x<descuentos.length;x++){
    descuentos[x].addEventListener('change',calcularPago);
}