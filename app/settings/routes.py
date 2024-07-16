from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import settings_bp
from .forms import EditServerForm
from ..models import db, Server

@settings_bp.route('/', methods=['GET'])
@login_required
def settings():
    servers = Server.query.filter_by(owner=current_user).all()
    return render_template('settings/settings.html', servers=servers)

@settings_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_server(id=None):
    if id:
        server = Server.query.get_or_404(id)
        if server.owner != current_user:
            flash('You do not have permission to edit this server.')
            return redirect(url_for('settings.settings'))
    else:
        server = None

    form = EditServerForm(obj=server)
    
    if form.validate_on_submit():
        if server:
            form.populate_obj(server)
        else:
            server = Server()
            form.populate_obj(server)
            server.owner = current_user
            db.session.add(server)
        
        db.session.commit()
        flash('Server settings have been updated.')
        return redirect(url_for('settings.settings'))

    return render_template('settings/edit_server.html', form=form, server=server)

