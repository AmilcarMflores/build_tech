from flask import render_template, url_for

def crear_ticket():
    return render_template(
        "crear.html",
        title="Crear ticket"
    )

def list_ticket(tickets):
    return render_template(
        "list_tickets.html",
        tickets=tickets,
        title="Lista de tickets"
    )

def update_ticket_ini(ticket):
    return render_template(
        "actualizar_ini.html",
        title="Actualizar ticket",
        ticket=ticket
    )

def update_ticket_fin(ticket):
    return render_template(
        "actualizar_fin.html",
        title="Finalizar ticket",
        ticket=ticket
    )

def generate_ticket(ticket):
    return render_template(
        "generate_ticket.html",
        title="Ticket",
        ticket=ticket,
        download_url=url_for('mantenimiento.download_report', id=ticket.id_mantenimiento)
    )