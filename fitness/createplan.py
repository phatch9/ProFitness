from fitness import app, db
from flask_admin import Admin
from fitness.database import Plan
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink

create_plan = Admin (app=app, name="ProFitness", template_mode='bootstrap4', url='/admin')
create_plan.add_view(ModelView(Plan, db.session))
create_plan.add_link(MenuLink(name='Back to Main Page', url='/home'))
