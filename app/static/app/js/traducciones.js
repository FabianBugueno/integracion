jQuery.extend(jQuery.validator.messages, {
    required: "Este campo es obligatorio.",
    remote: "Rellena este campo.",
    email: "Escribe una dirección de correo válida",
    url: "Escribe una URL válida.",
    date: "Ingresa una fecha válida.",
    dateISO: "Ingresa una fecha ISO válida.",
    number: "Escribe un número entero válido.",
    digits: "Ingresa sólo dígitos.",
    creditcard: "Ingresa un número de tarjeta válido.",
    equalTo: "Ingresa el mismo valor de nuevo.",
    accept: "Ingresa un valor con una extensión aceptada.",
    maxlength: jQuery.validator.format("No escribas más de {0} caracteres."),
    minlength: jQuery.validator.format("No escribas menos de {0} caracteres."),
    rangelength: jQuery.validator.format("Ingresa un valor entre {0} y {1} caracteres."),
    range: jQuery.validator.format("Ingresa un valor entre {0} y {1}."),
    max: jQuery.validator.format("Ingresa un valor menor o igual a {0}."),
    min: jQuery.validator.format("Ingresa escribe un valor mayor o igual a {0}.")
  });