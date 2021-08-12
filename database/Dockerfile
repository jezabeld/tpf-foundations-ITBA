FROM postgres:12.7

COPY create_tables.sql ./
COPY init_db.sh ./
COPY wrapper.sh ./

RUN chmod +x ./init_db.sh
RUN chmod +x ./wrapper.sh

ENTRYPOINT ["./wrapper.sh"]