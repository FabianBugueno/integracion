$.validator.addMethod("terminaPor", function(value, element, parametro){
    if(value.endsWith(parametro)){
        return true;
    }
    return false;
}, "Debe terminar en {0}")
 
$("#formulario_contacto").validate({
    rules: {
        nombre: {
            required: true,
            minlength: 3,
            maxlength: 30
        },
        rut: {
            required: true,
            minlength: 7,
            maxlength: 10,
            digits: true
        },
        email: {
            required: true,
            email: true,
            terminaPor: "duoc.cl"
        }, 
        tipo_solicitud: {
            required: true
        },
        mensaje: {
            required: true,
            minlength: 5,
            maxlength: 200
        }
    }
});
$("#rut").on("keypress", function(event) {
    let keyCode = event.which ? event.which : event.keyCode;
    if (keyCode < 48 || keyCode > 57) {
        event.preventDefault();
    }
});

$("#guardar").click(function() {
    if($("#formulario_contacto").valid() == false){
        return;
    }
        
    let nombre = $("#nombre").val();
    let rut = $("#rut").val();
    let email = $("#email").val();
    let tipoSolicitud = $("#tipo_solicitud").val();
    let mensaje = $("#mensaje").val();
    let aviso = $("avisos").is(":checked");

    console.log(nombre);
});
