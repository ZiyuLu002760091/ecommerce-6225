$startupScript = @'
#!/bin/sh
echo "Starting Django server..."
export DJANGO_SETTINGS_MODULE=config.settings
export PYTHONPATH=/usr/src/app
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
'@

$startupScript | Out-File -Encoding ASCII startup.sh