echo "[INFO] Chequeando instalación de docker..."

command -v docker >/dev/null 2>&1 || { echo >&2 "Se necesita docker pero no parece estar instalado.";exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo >&2 "Se necesita docker-compose pero no parece estar instalado."; exit 1;}

echo "[INFO] Chequeando que docker se encuentre corriendo..."

docker_state=$(docker info >/dev/null 2>&1)
if [[ $? -ne 0 ]]; then
    echo "Parece que el engine de Docker no está corriendo.";
    exit 1;
else
    echo "[INFO] Docker engine corriendo.";
fi

echo "[INFO] Creando directorio para la base de datos..."
mkdir -p ./pgdata

echo "[INFO] Levantando los microservicios..."
docker-compose run load_data 1> /dev/null 2> /dev/null && docker-compose up --quiet-pull  -d &

sleep 15
while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' localhost:5000)" != "200" ]]; do
    echo "Esperando que la API esté lista...";
    sleep 15;
done

echo "[INFO] Consultando reportes..."

echo "\n*****************************************************"
echo "Reporte diario de total de casos Covid Argentina:\n"
curl localhost:5000/dailyreport/ARG
echo "*****************************************************\n"

echo "\n*****************************************************"
echo "Reporte diario de total de casos Covid Sudamerica:\n"
curl localhost:5000/dailyreport/South_America
echo "*****************************************************\n"

echo "\n*****************************************************"
echo "Reporte diario de total de casos Covid Mundial:\n"
curl localhost:5000/dailyreport/global
echo "*****************************************************\n"

echo "\n*****************************************************"
echo "5 países con más casos confirmados por millón de habitantes:\n"
curl localhost:5000/top5/casespermillon
echo "*****************************************************\n"

echo "\n*****************************************************"
echo "5 paises con mayor porcentaje de habitantes vacunados contra el COVID-19 con alguna dosis:\n"
curl localhost:5000/top5/peoplevaccinated
echo "*****************************************************\n"

echo "\n*****************************************************"
echo "5 vacunas más aplicadas a nivel mundial:\n"
curl localhost:5000/top5/vaccines
echo "*****************************************************\n"

echo "\n*****************************************************"
echo "5 paises con mejor estado de inmunidad por vacunación:\n"
curl localhost:5000/top5/inmunity
echo "Nota: A menor valor de KPI (casos/vacunaciones) mayor inmunidad."
echo "*****************************************************\n"
echo "[INFO] Finalizando..."
docker-compose down