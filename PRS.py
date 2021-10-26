from app import app, db
from app.models import User, Applicant


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Applicant': Applicant}


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    app.run(debug=True)