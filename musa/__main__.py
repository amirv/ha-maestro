import src.cfg as cfg
import src.mqtt
import src.ws


if __name__ == '__main__':
    src.mqtt.connect()
    if cfg.INFO_INTERVAL:
        src.ws.get_stove_info()
    src.ws.connect()
