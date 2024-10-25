// Función para obtener el token CSRF de las cookies
function getCSRFToken() {
  const cookies = document.cookie.split(';'); // Divide las cookies en un array
  for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim(); // Elimina espacios en blanco
      if (cookie.startsWith('csrftoken=')) { // Busca la cookie csrftoken
          return cookie.substring('csrftoken='.length); // Devuelve el valor del token
      }
  }
  return null; // Si no se encuentra el token, retorna null
}

// Seleccionar todos los elementos de la lista de navegación
let list = document.querySelectorAll(".navigation li");

// Función para agregar la clase 'hovered' al elemento seleccionado
function activeLink() {
  list.forEach((item) => {
    item.classList.remove("hovered"); // Elimina la clase 'hovered' de todos los elementos
  });
  this.classList.add("hovered"); // Agrega la clase 'hovered' al elemento actual
}

// Agregar un evento de 'mouseover' a cada elemento de la lista
list.forEach((item) => item.addEventListener("mouseover", activeLink));

// Menú Toggle: permite mostrar y ocultar el menú de navegación
let toggle = document.querySelector(".toggle");
let navigation = document.querySelector(".navigation");
let main = document.querySelector(".main");

// Al hacer clic en el botón de toggle, alterna las clases 'active'
toggle.onclick = function () {
  navigation.classList.toggle("active"); // Activa o desactiva el menú
  main.classList.toggle("active"); // Activa o desactiva el contenido principal
};

// Cierra el menú si se hace clic fuera de él
document.addEventListener("click", function (event) {
  // Verifica si el clic está fuera del menú y del botón de toggle
  if (!navigation.contains(event.target) && !toggle.contains(event.target)) {
    navigation.classList.remove("active"); // Cierra el menú
    main.classList.remove("active"); // Restaura el contenido principal
  }
});

// Permitir arrastrar y soltar en las columnas
function allowDrop(event) {
  event.preventDefault(); // Prevenir el comportamiento por defecto
}

// Función que se ejecuta cuando se inicia el arrastre
function drag(event) {
  event.dataTransfer.setData("text", event.target.id); // Establece el ID del elemento arrastrado
}

// Función para manejar el evento de 'drop'
function drop(event) {
  event.preventDefault(); // Prevenir el comportamiento por defecto
  var data = event.dataTransfer.getData("text/plain"); // Obtiene los datos del elemento arrastrado
  var card = document.getElementById(data); // Obtiene el elemento arrastrado

  // Asegúrate de que el destino sea una columna
  var column = event.target.closest('.kanban-column'); // Busca el ancestro más cercano con la clase "kanban-column"

  if (column) {
      var columnId = column.id; // Obtiene el ID de la columna destino

      // Verifica si el destino es la columna "OT en Proceso"
      if (columnId === "ot_en_proceso") {
          // Obtener el número de solicitud desde la tarjeta
          var numeroSolicitud = card.id.split('-')[1]; // Asumiendo que el ID de la tarjeta tiene el formato "tarjeta-1"
          var solicitud = { numero: numeroSolicitud }; // Puedes agregar más datos si es necesario

          // Abre el modal con los datos de la solicitud
          openModal(solicitud); // Llama a la función que abre el modal
          return; // No muevas la tarjeta todavía, espera a que se envíe el formulario
      }

      // Si no es la columna "OT en Proceso", mueve la tarjeta
      column.appendChild(card); // Mueve la tarjeta a la columna destino

      // Actualiza el estado de la solicitud
      updateSolicitudState(card, columnId); // Llama a la función que actualiza el estado en el backend
  }
}

// Actualiza el estado de la solicitud en el backend
// Añadir esta función para actualizar el estado de la solicitud en el backend
function updateSolicitudState(card, columnId) {
  var numeroSolicitud = card.id.split('-')[1];

  var nuevoEstado = "";
  if (columnId === "solicitudes") {
    nuevoEstado = "Solicitudes";
  } else if (columnId === "ot_en_proceso") {
    nuevoEstado = "OT en Proceso";
  } else if (columnId === "ot_en_revision") {
    nuevoEstado = "OT en Revisión";
  } else if (columnId === "ot_finalizada") {
    nuevoEstado = "OT Finalizada";
  }

  fetch('/solicitudes/actualizar_estado_solicitud/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRFToken()
    },
    body: JSON.stringify({
        numero: numeroSolicitud,
        estado: nuevoEstado,
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'ok') {
      console.log('Estado actualizado exitosamente');
    } else {
      console.log('Error al actualizar el estado:', data.message);
    }
  })
  .catch(error => console.log('Error:', error));
}


// Cerrar el modal
// Función para cerrar el modal
function closeModal() {
  document.getElementById("tecnicoModal").style.display = "none"; // Oculta el modal
}

// Enviar el formulario del modal al servidor
document.getElementById("OrdenTrabajoForm").addEventListener("submit", function(event) {
  event.preventDefault();

  var nombreTecnico = document.getElementById("tecnico_asignado").value;
  var fechaActividad = document.getElementById("fecha_actividad").value;
  var numeroSolicitud = document.getElementById("numero_activo").value;

  if (!fechaActividad) {
    alert("La fecha de actividad es obligatoria.");
    return;
  }

  fetch('/solicitudes/actualizar_estado_solicitud/', {  
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken()
      },
      body: JSON.stringify({
          numero: numeroSolicitud,
          estado: "OT en Proceso",
          tecnico: nombreTecnico,
          fecha: fechaActividad
      })
  })
  .then(response => {
    if (!response.ok) {
        throw new Error('Error en la actualización');
    }
    return response.json();
  })
  .then(data => {
      console.log('Actualización exitosa:', data);
      var targetColumn = document.getElementById("ot_en_proceso");
      var card = document.getElementById("card-" + numeroSolicitud);
      targetColumn.appendChild(card);
      closeModal();
  })
  .catch((error) => {
      console.error('Error:', error);
  });
});


// Función para abrir el modal y establecer los valores
// Función para abrir el modal y establecer los valores
function openModal(solicitud) {
  var numeroActivoInput = document.getElementById("numero_activo");
  var fechaActividadInput = document.getElementById("fecha_actividad");
  var tecnicoAsignadoInput = document.getElementById("tecnico_asignado");

  // Verificar que los elementos existen antes de establecer sus valores
  if (numeroActivoInput && fechaActividadInput && tecnicoAsignadoInput) {
    numeroActivoInput.value = solicitud.numero; // Establece el número de solicitud en el campo del modal
    fechaActividadInput.value = "";  // Limpia el campo de fecha
    tecnicoAsignadoInput.value = "";  // Limpia el campo de técnico asignado
    document.getElementById("tecnicoModal").style.display = "block"; // Muestra el modal
  } else {
    console.error("No se encontraron los elementos del modal.");
  }
}


// Manejar la creación de Región
$('#region-form').on('submit', function(event) {
  event.preventDefault();
  $.ajax({
      url: "/activos/crear_region/",
      type: "POST",
      data: $(this).serialize(),
      success: function(response) {
          if (response.status === 'ok') {
              $('#region-table tbody').append(
                  `<tr>
                      <td>${response.region.nombre}</td>
                  </tr>`
              );
              $('#region-form')[0].reset();
          } else {
              alert('Error al crear Región');
          }
      }
  });
});

// Manejar la creación de PDV
$('#pdv-form').on('submit', function(event) {
  event.preventDefault();
  $.ajax({
      url: "/activos/crear_pdv/",
      type: "POST",
      data: $(this).serialize(),
      success: function(response) {
          if (response.status === 'ok') {
              $('#pdv-table tbody').append(
                  `<tr>
                      <td>${response.pdv.nombre}</td>
                      <td>${response.pdv.codigo}</td>
                      <td>${response.pdv.region}</td>
                  </tr>`
              );
              $('#pdv-form')[0].reset();
          } else {
              alert('Error al crear PDV');
          }
      }
  });
});

// Manejar la creación de Activo
$('#activo-form').on('submit', function(event) {
  event.preventDefault();
  $.ajax({
      url: "/activos/crear_activo/",
      type: "POST",
      data: $(this).serialize(),
      success: function(response) {
          if (response.status === 'ok') {
              $('#activo-table tbody').append(
                  `<tr>
                      <td>${response.activo.punto_de_venta}</td>
                      <td>${response.activo.tipo_equipo}</td>
                      <td>${response.activo.nombre_equipo}</td>
                      <td>${response.activo.tipo_maquinaria}</td>
                      <td>${response.activo.tipo_locativo}</td>
                  </tr>`
              );
              $('#activo-form')[0].reset();
          } else {
              alert('Error al crear Activo');
          }
      }
  });
});

// Manejar la lógica de mostrar/ocultar campos basados en la selección del tipo de subconjunto
$('#tipo_subconjunto').on('change', function() {
  const selectedType = $(this).val();
  if (selectedType === 'maquinaria') {
      $('#maquinaria-fields').show();
      $('#locativo-fields').hide();
  } else if (selectedType === 'locativo') {
      $('#locativo-fields').show();
      $('#maquinaria-fields').hide();
  } else {
      $('#maquinaria-fields').hide();
      $('#locativo-fields').hide();
  }
});
