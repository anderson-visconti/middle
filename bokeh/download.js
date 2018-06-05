var data = source.data;
var filetext = 'cenario,ena_se_p,ena_s_p,ena_ne_p,ena_n_p,preco_se\n';
for (i=0; i < data['cenario'].length; i++) {
    var currRow = [
        data['cenario'][i].toString(),
        data['ena_se_p'][i].toString(),
        data['ena_s_p'][i].toString(),
        data['ena_ne_p'][i].toString(),
        data['ena_n_p'][i].toString(),
        data['preco_se'][i].toString().concat('\n')
    ];

    var joined = currRow.join();
    filetext = filetext.concat(joined);
}

var filename = 'data_result.csv';
var blob = new Blob([filetext], { type: 'text/csv;charset=utf-8;' });

//addresses IE
if (navigator.msSaveBlob) {
    navigator.msSaveBlob(blob, filename);
}

else {
    var link = document.createElement("a");
    link = document.createElement('a')
    link.href = URL.createObjectURL(blob);
    link.download = filename
    link.target = "_blank";
    link.style.visibility = 'hidden';
    link.dispatchEvent(new MouseEvent('click'))
}