from flask import Blueprint, render_template, request, jsonify
from models.chat_model import ChatMessage, Notification
from models.mantenimiento_model import Mantenimiento

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat")
def chat_general():
    """Chat general del sistema"""
    return render_template("chat.html", title="Chat General")

@chat_bp.route("/chat/ticket/<int:ticket_id>")
def chat_ticket(ticket_id):
    """Chat específico de un ticket"""
    ticket = Mantenimiento.get_by_id(ticket_id)
    if not ticket:
        return "Ticket no encontrado", 404
    
    messages = ChatMessage.get_by_ticket(ticket_id)
    return render_template(
        "chat_ticket.html", 
        title=f"Chat - Ticket #{ticket_id}",
        ticket=ticket,
        messages=messages
    )

@chat_bp.route("/notificaciones")
def notificaciones():
    """Ver todas las notificaciones"""
    notificaciones = Notification.get_all()
    return render_template(
        "notificaciones.html",
        title="Notificaciones",
        notificaciones=notificaciones
    )

@chat_bp.route("/api/notificaciones/no-leidas")
def notificaciones_no_leidas():
    """API: Obtener notificaciones no leídas"""
    notificaciones = Notification.get_no_leidas()
    return jsonify({
        'count': len(notificaciones),
        'notificaciones': [n.to_dict() for n in notificaciones]
    })

@chat_bp.route("/api/notificaciones/<int:id>/marcar-leida", methods=["POST"])
def marcar_notificacion_leida(id):
    """API: Marcar notificación como leída"""
    notificacion = Notification.query.get(id)
    if notificacion:
        notificacion.marcar_leido()
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Notificación no encontrada'}), 404