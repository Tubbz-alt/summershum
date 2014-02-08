import summershum.utils

import fedmsg
import logging
log = logging.getLogger("summershum")

def ingest(session, msg, config):
        log.info("Ingesting %r" % msg.get('filename'))
        fedmsg.publish(
            topic='ingest.start',
            msg=dict(original=msg),
        )

        lookaside_url = config['summershum.lookaside']

        try:
            summershum.utils.download_lookaside(msg, lookaside_url)
            summershum.utils.get_sha1sum(session, msg)
        except Exception as e:
            log.error("Failed to ingest %r %r" % (msg.get('filename'), e))
            fedmsg.publish(
                topic='ingest.fail',
                msg=dict(
                    original=msg,
                    error=str(e),
                ),
            )
        else:
            log.info("Done ingesting %r" % msg.get('filename'))
            fedmsg.publish(
                topic='ingest.complete',
                msg=dict(original=msg),
            )
