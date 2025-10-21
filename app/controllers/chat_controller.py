from flask import Blueprint, render_template, request, jsonify
from models.chat_model import ChatMessage, Notification
from models.mantenimiento_model import Mantenimiento
from flask_login import login_required, current_user
from utils.decorators import role_required # Importar el decorador de roles

chat_bp = Blueprint("chat", __name__, url_prefix="/comunicacion") # Añadido url_prefix para limpieza

@chat_bp.route("/chat")
@login_required # Solo usuarios logueados
def chat_general():
    """Chat general del sistema"""
    # Pasar el nombre del usuario logueado
    username = current_user.first_name if current_user.is_authenticated else 'Anónimo'
    return render_template(
        "chat.html", 
        title="Chat General",
        # Nombre del usuario autenticado para usar en el frontend de Socket.IO
        current_username=username 
    )

@chat_bp.route("/chat/ticket/<int:ticket_id>")
@login_required # Solo usuarios logueados
def chat_ticket(ticket_id):
    """Chat específico de un ticket"""
    ticket = Mantenimiento.get_by_id(ticket_id)
    if not ticket:
        return "Ticket no encontrado", 404
    
    # Pasar el nombre del usuario logueado
    username = current_user.first_name if current_user.is_authenticated else 'Anónimo'
    
    # En un entorno real, podrías querer cargar los mensajes aquí, pero Socket.IO ya lo hace.
    return render_template(
        "chat_ticket.html", 
        title=f"Chat - Ticket #{ticket_id}",
        ticket=ticket,
        current_username=username 
    )

@chat_bp.route("/notificaciones")
@role_required('admin') # Solo administradores pueden ver todas las notificaciones
def notificaciones():
    """Ver todas las notificaciones"""
    notificaciones = Notification.get_all()
    return render_template(
        "notificaciones.html",
        title="Notificaciones",
        notificaciones=notificaciones
    )

@chat_bp.route("/api/notificaciones/no-leidas")
@login_required # Requerido para acceder a la API de no leídas
def notificaciones_no_leidas():
    """API: Obtener notificaciones no leídas"""
    # En un sistema real, esto debería filtrar por usuario o rol
    if current_user.has_role('admin'):
        notificaciones = Notification.get_no_leidas()
        return jsonify({
            'count': len(notificaciones),
            'notificaciones': [n.to_dict() for n in notificaciones]
        })
    return jsonify({'count': 0, 'notificaciones': []})


@chat_bp.route("/api/notificaciones/<int:id>/marcar-leida", methods=["POST"])
@login_required # Requerido para acceder a la API
def marcar_notificacion_leida(id):
    """API: Marcar notificación como leída"""
    # Solo los admins deberían poder marcar como leída
    if not current_user.has_role('admin'):
        return jsonify({'success': False, 'error': 'Permiso denegado'}), 403
        
    notificacion = Notification.query.get(id)
    if notificacion:
        notificacion.marcar_leido()
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Notificación no encontrada'}), 404