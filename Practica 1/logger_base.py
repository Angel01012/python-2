import logging as log
log.basicConfig(level=log.DEBUG,
                format="%(asctime)s: %(levelname)s [%(filename)s] :%(lineno)s %(message)s",
                datefmt='%I:%M:%S:%p',
                handlers=[log.FileHandler('log_datos.log'), log.StreamHandler()
                ])

if __name__ == "__main__":
    log.debug("Mensaje Debug")
    log.warning("Mesaje Warning")
    log.error("Mensaje Error")
    log.critical("Mensaje Critico")