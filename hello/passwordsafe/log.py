import logging


log = logging.getLogger('org.xux')
sh = logging.StreamHandler()
sh.setFormatter( logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s') )
log.addHandler(sh)
log.setLevel(logging.DEBUG)

log.info(__name__)

