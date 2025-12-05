import re
from typing import List

def validate_config(config: str) -> List[str]:
    """Valida una configuración de Mikrotik y retorna lista de errores.
    
    Esta validación es flexible y solo verifica que haya consistencia
    en la configuración generada, no que tenga todos los elementos posibles.
    """
    issues = []
    
    # Si no hay ninguna configuración significativa, es un error
    if not config.strip() or len(config.strip()) < 50:
        issues.append("Configuración vacía o muy corta")
        return issues
    
    # Verificar que tenga al menos una configuración de interface o sistema
    has_any_config = any([
        "/system identity" in config,
        "/ip address" in config,
        "/interface" in config,
        "/ip dhcp-client" in config,
        "/ip firewall" in config
    ])
    
    if not has_any_config:
        issues.append("No se encontró ninguna configuración válida de Mikrotik")
    
    # Verificar sintaxis básica de IPs (solo si hay IPs definidas)
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
    
    # Validar IP WAN solo si está definida
    if 'wan_ip' in params and params['wan_ip']:
        if not _is_valid_ip(params['wan_ip']):
            issues.append("IP WAN inválida")
    
    # Validar Gateway solo si está definido
    if 'gateway' in params and params['gateway']:
        if not _is_valid_ip(params['gateway']):
            issues.append("Gateway inválido")
    
    # Validar máscara solo si está definida
    if 'wan_mask' in params and params['wan_mask']:
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
        if not ip or not ip.strip():
            return True  # Empty is valid (will be handled by template)
        octets = ip.split('.')
        if len(octets) != 4:
            return False
        for octet in octets:
            if int(octet) < 0 or int(octet) > 255:
                return False
        return True
    except:
        return False