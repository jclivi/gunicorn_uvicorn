
import logging
 
logging.basicConfig(level=logging.DEBUG,
                    filename='./logs/service.log')
log = logging.getLogger(__name__)
 
log.info('info')
log.debug('debug')
log.warning('warning')
log.info('info')