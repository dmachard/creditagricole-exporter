import asyncio
import logging
import sys
import os

from creditagricole_particuliers import Authenticator, Accounts

import prometheus_client

logger = logging.getLogger("monitor")


async def monitor(every, username, password, department, prometheus_prefix):

    # metrics
    gauge_comptes = prometheus_client.Gauge('%s_comptes_total' % prometheus_prefix, 'Comptes solde total')
    gauge_epargne_disponible = prometheus_client.Gauge('%s_epargne_disponible_total' % prometheus_prefix, 'Epargne disponible solde total')
    gauge_epargne_autre = prometheus_client.Gauge('%s_epargne_autre_total' % prometheus_prefix, 'Epargne autre solde total')

    while True:
        session = Authenticator(username=username, password=password, department=department)

        try:
            # get soldes
            soldes = Accounts(session=session).get_solde_per_products()

            # update metrics
            gauge_comptes.set(soldes["COMPTES"])
            gauge_epargne_disponible.set(soldes["EPARGNE_DISPONIBLE"])
            gauge_epargne_autre.set(soldes["EPARGNE_AUTRE"])
        except Exception as e:
            logger.error("%s" % e)

        logger.debug("re-checking in %s seconds" % every)
        await asyncio.sleep(every)

def setup_logger(debug):
    loglevel = logging.DEBUG if debug else logging.INFO
    logfmt = '%(asctime)s %(levelname)s %(message)s'

    logger.setLevel(loglevel)
    logger.propagate = False

    lh = logging.StreamHandler(stream=sys.stdout )
    lh.setLevel(loglevel)
    lh.setFormatter(logging.Formatter(logfmt))

    logger.addHandler(lh)

def start_monitor():
    delay_every = 3600
    listen_port = 8080
    prom_prefix = "creditagricole"
    debug = False

    # read environment variables
    debug_env = os.getenv('CREDITAGRICOLE_EXPORTER_DEBUG')
    if debug_env is not None:
        debug = bool( int(debug_env) )

    setup_logger(debug=debug)

    listen_port_env = os.getenv('CREDITAGRICOLE_EXPORTER_PORT')
    if listen_port_env is not None:
        listen_port = int(listen_port_env)

    delay_env = os.getenv('CREDITAGRICOLE_EXPORTER_DELAY')
    if delay_env is not None:
        delay_every = int(delay_env)

    prom_env = os.getenv('CREDITAGRICOLE_EXPORTER_PROMETHEUS_PREFIX')
    if prom_env is not None:
        prom_prefix = prom_env

    username = os.getenv('CREDITAGRICOLE_EXPORTER_USERNAME')
    if username is None:
        logger.error("missing env variable CREDITAGRICOLE_EXPORTER_USERNAME")
        sys.exit(1)

    password = os.getenv('CREDITAGRICOLE_EXPORTER_PASSWORD')
    if password is None:
        logger.error("missing env variable CREDITAGRICOLE_EXPORTER_PASSWORD")
        sys.exit(1)
    # convert string to list of int
    password = [int(x) for x in password]
    
    department = os.getenv('CREDITAGRICOLE_EXPORTER_DEPARTMENT')
    if department is None:
        logger.error("missing env variable CREDITAGRICOLE_EXPORTER_DEPARTMENT")
        sys.exit(1)
    department = int(department)
    
    try:
        prometheus_client.start_http_server(listen_port)
        asyncio.run(monitor(every=delay_every,
                            username=username,
                            password=password,
                            department=department,
                            prometheus_prefix=prom_prefix))
    except KeyboardInterrupt:
        logger.debug("exit called")
