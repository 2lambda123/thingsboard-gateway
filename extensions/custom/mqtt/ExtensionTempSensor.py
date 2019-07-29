from time import time

from . import ExtensionInterface


class Extension(ExtensionInterface.ExtensionInterface):
    def convert_message_to_atr_request(self, topic, payload):
        id = payload["id"]
        device = payload["device"]
        shared = payload["shared"]
        item = [{"device_name": device, "shared_keys": shared}]
        print(item)
        return item, id

    def convert_message_to_json_for_storage(self, topic, payload):
        ts = int(round(time() * 1000))
        try:
            # result = [
            #     {
            #         "device_name": topic.split("/")[-1],
            #         # todo remove "#" after implementing device_type!
            #         # "device_type": payload["type"],
            #         "attributes": {
            #             "model": payload["model"],
            #             "serial_number": payload["serial"],
            #             # todo what is integration?
            #         },
            #         "telemetry": [
            #             {
            #                 "ts": ts,
            #                 "values": {
            #                     "temperature": payload["temperature1"],
            #                     "humidity": payload["humidity1"]
            #                 }
            #             },
            #             {
            #                 "ts": ts,
            #                 "values": {
            #                     "humidity": payload["humidity2"]
            #                 }
            #             }
            #         ]
            #     }
            # ]
            result = [
                {
                    "device_name": topic.split("/")[-1],
                    # todo remove "#" after implementing device_type!
                    # "device_type": payload["type"],
                    "telemetry": [
                        {
                            "ts": ts,
                            "values": {
                                "temperature": payload["temperature"],
                            }
                        }
                    ]
                }
            ]
            return result
        except:
            pass
