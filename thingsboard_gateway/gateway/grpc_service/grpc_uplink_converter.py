#      Copyright 2021. ThingsBoard
#  #
#      Licensed under the Apache License, Version 2.0 (the "License");
#      you may not use this file except in compliance with the License.
#      You may obtain a copy of the License at
#  #
#          http://www.apache.org/licenses/LICENSE-2.0
#  #
#      Unless required by applicable law or agreed to in writing, software
#      distributed under the License is distributed on an "AS IS" BASIS,
#      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#      See the License for the specific language governing permissions and
#      limitations under the License.

from thingsboard_gateway.connectors.converter import Converter, log
from thingsboard_gateway.gateway.constant_enums import UplinkMessageType
from thingsboard_gateway.gateway.proto.messages_pb2 import ConnectMsg, DisconnectMsg, GatewayAttributesMsg, GatewayAttributesRequestMsg, GatewayClaimMsg, \
    GatewayRpcResponseMsg, GatewayTelemetryMsg, RegisterConnectorMsg, Response, UnregisterConnectorMsg, KeyValueProto, KeyValueType


class GrpcUplinkConverter(Converter):
    def __init__(self):
        self.__conversion_methods = {
            UplinkMessageType.Response: self.__convert_response_msg,
            UplinkMessageType.GatewayTelemetryMsg: self.__convert_gateway_telemetry_msg,
            UplinkMessageType.GatewayAttributesMsg: self.__convert_gateway_attributes_msg,
            UplinkMessageType.GatewayClaimMsg: self.__convert_gateway_claim_msg,
            # UplinkMessageType.RegisterConnectorMsg: self.__convert_register_connector_msg,
            # UplinkMessageType.UnregisterConnectorMsg: self.__convert_unregister_connector_msg,
            UplinkMessageType.ConnectMsg: self.__convert_connect_msg,
            UplinkMessageType.DisconnectMsg: self.__convert_disconnect_msg,
            UplinkMessageType.GatewayRpcResponseMsg: self.__convert_gateway_rpc_response_msg,
            UplinkMessageType.GatewayAttributesRequestMsg: self.__convert_gateway_attributes_request_msg
            }

    def convert(self, config, data):
        try:
            if self.__conversion_methods.get(config) is not None:
                return self.__conversion_methods[config](data)
            else:
                log.error("[GRPC] unknown uplink message type: %r", config)
                return {}
        except Exception as e:
            log.exception("[GRPC] ", e)
            return {}

    @staticmethod
    def __convert_response_msg(self, msg: Response):
        log.debug("Converted response: %r", msg.response)

    @staticmethod
    def __convert_gateway_telemetry_msg(msg: GatewayTelemetryMsg):
        result = []
        for telemetry_msg in msg.msg:
            device_dict = {"deviceName": telemetry_msg.deviceName, "telemetry": []}
            for post_telemetry_msg in telemetry_msg.msg:
                for ts_kv_list in post_telemetry_msg.tsKvList:
                    ts_kv_list_dict = {"ts": ts_kv_list.ts, "values": {}}
                    for kv in ts_kv_list.kv:
                        ts_kv_list_dict['values'][kv.key] = GrpcUplinkConverter.get_value(kv)
                    device_dict['telemetry'].append(ts_kv_list_dict)
            result.append(device_dict)
        return result

    @staticmethod
    def __convert_gateway_attributes_msg(msg: GatewayAttributesMsg):
        result = []
        for attributes_msg in msg.msg:
            device_dict = {"deviceName": attributes_msg.deviceName, "attributes": {}}
            for post_attribute_msg in attributes_msg.msg:
                for kv in post_attribute_msg.kv:
                    device_dict['attributes'][kv.key] = GrpcUplinkConverter.get_value(kv)
            result.append(device_dict)
        return result

    def __convert_gateway_claim_msg(self, msg: GatewayClaimMsg):
        pass

    # def __convert_register_connector_msg(self, msg: RegisterConnectorMsg):
    #     pass
    #
    # def __convert_unregister_connector_msg(self, msg: UnregisterConnectorMsg):
    #     pass

    @staticmethod
    def __convert_connect_msg(msg: ConnectMsg) -> dict:
        result_dict = {'deviceName': msg.deviceName, 'deviceType': msg.deviceType}
        return result_dict

    @staticmethod
    def __convert_disconnect_msg(msg: DisconnectMsg):
        return {"deviceName": msg.deviceName}

    def __convert_gateway_rpc_response_msg(self, msg: GatewayRpcResponseMsg):
        pass

    def __convert_gateway_attributes_request_msg(self, msg: GatewayAttributesRequestMsg):
        pass

    @staticmethod
    def get_value(msg: KeyValueProto):
        if msg.type == KeyValueProto.BOOLEAN_V:
            return msg.bool_v
        if msg.type == KeyValueProto.LONG_V:
            return msg.long_v
        if msg.type == KeyValueProto.DOUBLE_V:
            return msg.double_v
        if msg.type == KeyValueProto.STRING_V:
            return msg.string_v
        if msg.type == KeyValueProto.JSON_V:
            return msg.json_v