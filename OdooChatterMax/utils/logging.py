# your_module/utils/logging.py

def log_debug_message(
    env,
    message,
    level='info',
    name='OdooChatterMax',
    path='custom.debug',
    func='log_debug',
    line=0,
    dbname=None,
    commit=True
):
    try:
        env['ir.logging'].sudo().create({
            'name': name,
            'type': 'server',
            'dbname': dbname or env.cr.dbname,
            'level': level,
            'message': message,
            'path': path,
            'func': func,
            'line': line,
        })
        if commit:
            env.cr.commit()
    except Exception as e:
        print(f"[log_debug_message] Failed to log message: {e}")
