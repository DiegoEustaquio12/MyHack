console.log("JS listo");
console.log('Equipo Listo')
console.log("prueba1")

document.getElementById("btn").addEventListener("click", async () => {
    const cultivo = document.getElementById("cultivo").value;
    const hectareas = document.getElementById("hectareas").value;

    const respuesta = await fetch("/receta", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cultivo, hectareas })
    });

    const datos = await respuesta.json();
    document.getElementById("resultado").innerHTML = `
        <p>🌱 Fertilizante: ${datos.fertilizante}</p>
        <p>⚖️ Cantidad: ${datos.cantidad}</p>
        <p>💰 Costo estimado: ${datos.costo}</p>
    `;
});