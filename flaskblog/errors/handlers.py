from flask import Blueprint, render_template


errors = Blueprint(name='errors', import_name=__name__)


@errors.app_errorhandler(code=404)
def error_404(error):
    return render_template(template_name_or_list='errors/404.html'), 404


@errors.app_errorhandler(code=403)
def error_404(error):
    return render_template(template_name_or_list='errors/403.html'), 403


@errors.app_errorhandler(code=500)
def error_404(error):
    return render_template(template_name_or_list='errors/500.html'), 500
