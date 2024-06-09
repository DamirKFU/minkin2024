from flask import render_template
from flask_login import login_required
import sqlalchemy as sa
from app import db
from app.models import User
from app.main import bp



@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', title=_('Home'))


@bp.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.name == username))
    return render_template('user.html', user=user)

