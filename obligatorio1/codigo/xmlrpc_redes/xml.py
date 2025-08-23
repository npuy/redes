import xml.etree.ElementTree as ET
import datetime as dt

"""
Módulo de helpers XML-RPC.

Proporciona funciones para:
- Parsear y construir requests y responses XML-RPC.
- Convertir entre tipos de datos de Python y elementos XML-RPC.
- Generar respuestas de error (faults) de XML-RPC.

Usado por el cliente y servidor para enviar y recibir mensajes XML-RPC sobre HTTP/TCP.
"""

def parse_value(elem):
    if elem.find('int') is not None:
        return int(elem.find('int').text)
    if elem.find('i4') is not None:
        return int(elem.find('i4').text)
    if elem.find('boolean') is not None:
        return bool(int(elem.find('boolean').text))
    if elem.find('double') is not None:
        return float(elem.find('double').text)
    if elem.find('string') is not None:
        return elem.find('string').text or ''
    if elem.find('dateTime.iso8601') is not None:
        return dt.datetime.fromisoformat(elem.find('dateTime.iso8601').text)
    if elem.find('array') is not None:
        data = elem.find('array').find('data')
        ret = []
        for val in data:
            if val.tag != 'value':
                raise Exception('Error parseo de XML')
            ret.append(parse_value(val))
        return ret
    if elem.find('struct') is not None:
        data = elem.find('struct')
        ret = {}
        for val in data:
            if val.tag != 'member':
                raise Exception('Error parseo de XML')
            ret[val.find('name').text] = parse_value(val.find('value'))
        return ret
    if elem.find('base64') is not None:
        return elem.find('base64').text.encode()
    if elem.text and elem.text.strip():
        return elem.text.strip()
    return ''

def build_value_element(pyval):
    v = ET.Element('value')
    if isinstance(pyval, bool):
        ET.SubElement(v, 'boolean').text = '1' if pyval else '0'
    elif isinstance(pyval, int):
        ET.SubElement(v, 'int').text = str(pyval)
    elif isinstance(pyval, float):
        ET.SubElement(v, 'double').text = repr(pyval)
    elif isinstance(pyval, dt.datetime):
        ET.SubElement(v, 'dateTime.iso8601').text = str(pyval.isoformat())
    elif isinstance(pyval, list):
        arr = ET.SubElement(v, 'array')
        data = ET.SubElement(arr, 'data')
        for ele in pyval:
            data.append(build_value_element(ele))
    elif isinstance(pyval, dict):
        struct = ET.SubElement(v, 'struct')
        for k, val in pyval.items():
            mem = ET.SubElement(struct, 'member')
            ET.SubElement(mem, 'name').text = k
            mem.append(build_value_element(val))
    elif isinstance(pyval, (bytes, bytearray)):
        ET.SubElement(v, 'base64').text = pyval.decode()
    else:
        ET.SubElement(v, 'string').text = str(pyval)
    return v

def parse_xmlrpc_request(body_bytes):
    root = ET.fromstring(body_bytes.decode('utf-8'))
    method = root.find('methodName').text
    params = []
    params_root = root.find('params')
    if params_root is not None:
        for p in params_root.findall('param'):
            value_elem = p.find('value')
            params.append(parse_value(value_elem))
    return method, params

def build_xmlrpc_request(method_name, params):
    methodCall = ET.Element('methodCall')
    mn = ET.SubElement(methodCall, 'methodName')
    mn.text = method_name
    params_el = ET.SubElement(methodCall, 'params')
    for p in params:
        param = ET.SubElement(params_el, 'param')
        param.append(build_value_element(p))
    return ET.tostring(methodCall, encoding='utf-8', xml_declaration=True)

def parse_xmlrpc_response(body_bytes):
    root = ET.fromstring(body_bytes.decode('utf-8'))
    fault = root.find('fault')
    if fault is not None:
        struct = fault.find('value').find('struct')
        code, msg = None, None
        for member in struct.findall('member'):
            name = member.find('name').text
            val = member.find('value')
            if name == 'faultCode':
                code = int(val.find('int').text)
            elif name == 'faultString':
                msg = val.find('string').text
        raise Exception(f'Error XML-RPC {code}: {msg}')

    params = root.find('params')
    if params is None:
        return None
    return parse_value(params.find('param').find('value'))

def build_xmlrpc_response(result):
    methodResponse = ET.Element('methodResponse')
    params = ET.SubElement(methodResponse, 'params')
    param = ET.SubElement(params, 'param')
    param.append(build_value_element(result))
    return ET.tostring(methodResponse, encoding='utf-8', xml_declaration=True)

def build_xmlrpc_fault(code, message):
    methodResponse = ET.Element('methodResponse')
    fault = ET.SubElement(methodResponse, 'fault')
    value = ET.SubElement(fault, 'value')
    struct = ET.SubElement(value, 'struct')

    member_code = ET.SubElement(struct, 'member')
    ET.SubElement(member_code, 'name').text = 'faultCode'
    vcode = ET.SubElement(member_code, 'value')
    ET.SubElement(vcode, 'int').text = str(code)

    member_msg = ET.SubElement(struct, 'member')
    ET.SubElement(member_msg, 'name').text = 'faultString'
    vmsg = ET.SubElement(member_msg, 'value')
    ET.SubElement(vmsg, 'string').text = message

    return ET.tostring(methodResponse, encoding='utf-8', xml_declaration=True)

