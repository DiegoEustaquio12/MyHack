document.getElementById("btn").addEventListener("click", async () => {
    const cultivo = document.getElementById("cultivo").value;
    const hectareas = document.getElementById("hectareas").value;
    const tiempo = document.getElementById("tiempo").value;

    if (!hectareas) {
        alert("Ingresa el numero de Hectareas");
        return;

    }

    try {
        
        const respuesta = await fetch("/receta", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ tiempo: tiempo, cultivo: cultivo, hectareas: hectareas })
        });

        
        const datos = await respuesta.json();
        document.getElementById("resultado").innerHTML = `
            <p>🌱 Fertilizante: ${datos.fertilizante}</p>
            <p>⚖️ Cantidad: ${datos.cantidad}</p>
            <p>💰 Costo estimado: ${datos.costo}</p>
        `;
    } catch (error) {
        console.error("Hubo un error con el servidor:", error);
        document.getElementById("resultado").innerHTML = "<p>Hubo un error al calcular la receta.</p>";
    }
    
});
