import re
from typing import List

def validate_config(config: str) -> List[str]:
    """Valida una configuración de Mikrotik y retorna lista de errores"""
    issues = []
    
    # Verificar que tenga configuración IP básica
    if "/ip address" not in config:
        issues.append("Falta configuración de direcciones IP")
    
    # Verificar que tenga gateway
    if "/ip route" not in config and "gateway=" not in config:
        issues.append("Falta configuración de gateway/rutas")
    
    # Verificar que tenga DNS
    if "/ip dns" not in config:
        issues.append("Falta configuración de DNS")
    
    # Verificar sintaxis básica de IPs
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    ips_found = re.findall(ip_pattern, config)
    
    for ip in ips_found:
        octets = ip.split('.')
        for octet in octets:
            if int(octet) > 255:
                issues.append(f"IP inválida encontrada: {ip}")
                break
    
    return issues

def validate_params(params: dict) -> List[str]:
    """Valida los parámetros antes de generar la configuración"""
    issues = []
    
    # Validar IP WAN
    if 'wan_ip' in params:
        if not _is_valid_ip(params['wan_ip']):
            issues.append("IP WAN inválida")
    
    # Validar Gateway
    if 'gateway' in params:
        if not _is_valid_ip(params['gateway']):
            issues.append("Gateway inválido")
    
    # Validar máscara
    if 'wan_mask' in params:
        try:
            mask = int(params['wan_mask'])
            if mask < 1 or mask > 32:
                issues.append("Máscara de red inválida (debe ser 1-32)")
        except ValueError:
            issues.append("Máscara de red debe ser un número")
    
    return issues

def _is_valid_ip(ip: str) -> bool:
    """Valida formato de IP"""
    try:
        octets = ip.split('.')
        if len(octets) != 4:
            return False
        for octet in octets:
            if int(octet) < 0 or int(octet) > 255:
                return False
        return True
    except:
        return False