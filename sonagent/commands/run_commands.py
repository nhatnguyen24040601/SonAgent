import logging
import signal
from typing import Any, Dict


logger = logging.getLogger(__name__)


def start_sonagent(args: Dict[str, Any]) -> int:
    """
    Main entry point for running mode
    """
    # Import here to avoid loading worker module when it's not used
    from sonagent.worker import Worker

    def term_handler(signum, frame):
        # Raise KeyboardInterrupt - so we can handle it in the same way as Ctrl-C
        raise KeyboardInterrupt()

    # Create and run worker
    worker = None
    try:
        signal.signal(signal.SIGTERM, term_handler)
        config = {
            'internals': {
                'sd_notify': True
            }
        }
        worker = Worker(args, config=config)
        worker.run()
    except Exception as e:
        logger.error(str(e))
        logger.exception("Fatal exception!")
    except (KeyboardInterrupt):
        logger.info('SIGINT received, aborting ...')
    finally:
        if worker:
            logger.info("worker found ... calling exit")
            worker.exit()
    return 0
