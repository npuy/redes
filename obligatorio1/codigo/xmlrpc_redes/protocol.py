import xml.etree.ElementTree as ET

# ---------- XML-RPC helpers ----------

def parse_value(elem):
    if elem.find('int') is not None or elem.find('i4') is not None:
        t = elem.find('int') or elem.find('i4')
        return int(t.text)
    if elem.find('boolean') is not None:
        return bool(int(elem.find('boolean').text))
    if elem.find('double') is not None:
        return float(elem.find('double').text)
    if elem.find('string') is not None:
        return elem.find('string').text or ''
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
        raise Exception(f'XML-RPC Fault {code}: {msg}')

    params = root.find('params')
    if params is None:
        return None
    return parse_value(params.find('param').find('value'))

# ---------- HTTP helpers ----------

def parse_http_request(raw):
    sep = b'\r\n\r\n'
    head, body = raw.split(sep, 1) if sep in raw else (raw, b'')
    lines = head.decode('iso-8859-1').split('\r\n')
    request_line = lines[0]
    method, path, proto = request_line.split(' ', 2)
    headers = {}
    for line in lines[1:]:
        if not line: continue
        k, v = line.split(':', 1)
        headers[k.strip().lower()] = v.strip()
    return method, path, proto, headers, body

def build_http_request(host, port, body_bytes):
    req = f"POST /RPC2 HTTP/1.1\r\nHost: {host}:{port}\r\nContent-Type: text/xml\r\nContent-Length: {len(body_bytes)}\r\n\r\n".encode()
    return req + body_bytes

def build_http_response(body_bytes, status=200, status_text='OK'):
    h = f'HTTP/1.1 {status} {status_text}\r\nContent-Length: {len(body_bytes)}\r\nContent-Type: text/xml; charset=utf-8\r\n\r\n'
    return h.encode('iso-8859-1') + body_bytes
